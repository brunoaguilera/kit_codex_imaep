#!/usr/bin/env python3
"""Descarga el Excel oficial del IMAEP. Requiere Python 3.10+ e Internet.

No analiza ni modifica los valores. No sobrescribe archivos existentes.
Uso: python3 descargar_imaep.py [--dest data/raw]
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

SOURCE_PAGE = (
    "https://www.bcp.gov.py/web/institucional/"
    "indicador-mensual-de-actividad-economica-del-paraguay-imaep-"
)
DOWNLOAD_URL = (
    "https://www.bcp.gov.py/documents/20117/2659103/"
    "Indicador%2BMensual%2Bde%2Bla%2BActividad%2BEcon%C3%B3mica%2Bdel%2BParaguay.xlsx/"
    "27688483-a192-9797-37f7-1f8b184bf430?t=1789069578102"
)
MAX_BYTES = 64 * 1024 * 1024


def validate_xlsx(content: bytes) -> None:
    """Distingue un XLSX real de una página de error; no valida los datos."""
    try:
        with ZipFile(io.BytesIO(content)) as archive:
            names = set(archive.namelist())
            if not {"[Content_Types].xml", "xl/workbook.xml"}.issubset(names):
                raise ValueError("La respuesta no contiene un libro XLSX válido.")
            if any(info.file_size > MAX_BYTES for info in archive.infolist()):
                raise ValueError("El XLSX contiene un componente demasiado grande.")
            if sum(info.file_size for info in archive.infolist()) > MAX_BYTES * 4:
                raise ValueError("El contenido descomprimido excede el límite previsto.")
            if archive.testzip() is not None:
                raise ValueError("El XLSX está dañado.")
    except BadZipFile as exc:
        raise ValueError("La respuesta no es un XLSX; podría ser una página de error.") from exc


def download(destination: Path) -> tuple[Path, Path]:
    output = destination / "imaep_bcp_original.xlsx"
    manifest_path = destination / "fuente_imaep.json"
    if output.exists() or manifest_path.exists():
        raise FileExistsError(
            "Ya existe el archivo o su manifiesto. Se conservaron sin cambios. "
            "Elegí otro directorio con --dest para descargar una nueva versión."
        )
    request = Request(DOWNLOAD_URL, headers={"User-Agent": "IMAEP-academic-download/1.0"})
    with urlopen(request, timeout=60) as response:
        final_url = response.geturl()
        host = (urlparse(final_url).hostname or "").lower()
        if host != "bcp.gov.py" and not host.endswith(".bcp.gov.py"):
            raise ValueError("La descarga redirigió fuera del dominio oficial del BCP.")
        content = response.read(MAX_BYTES + 1)
        last_modified = response.headers.get("Last-Modified")
        content_type = response.headers.get("Content-Type")
    if len(content) > MAX_BYTES:
        raise ValueError("La descarga excede el límite de 64 MiB.")
    validate_xlsx(content)
    manifest = {
        "institucion": "Banco Central del Paraguay",
        "indicador": "Indicador Mensual de Actividad Económica del Paraguay (IMAEP)",
        "pagina_fuente": SOURCE_PAGE,
        "url_descarga": DOWNLOAD_URL,
        "url_final": final_url,
        "fecha_descarga_utc": datetime.now(timezone.utc).isoformat(),
        "last_modified_http": last_modified,
        "content_type_http": content_type,
        "archivo": output.name,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "validacion_formato_xlsx": "OK",
        "validacion_datos": "PENDIENTE: inspeccionar hojas, columnas, unidad y cobertura",
        "periodo_objetivo": "2016-01 a 2025-12; pendiente de verificar en el archivo",
    }
    destination.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        handle.write(content)
    try:
        with manifest_path.open("x", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except Exception:
        output.unlink(missing_ok=True)
        raise
    return output, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    try:
        output, manifest = download(args.dest)
    except (HTTPError, URLError, OSError, ValueError) as exc:
        print(f"No se completó la descarga: {exc}")
        print("No se generaron datos sustitutos ni estimados.")
        print(f"Descarga manual desde la página oficial: {SOURCE_PAGE}")
        return 1
    print(f"Excel original: {output.resolve()}")
    print(f"Registro de procedencia: {manifest.resolve()}")
    print("El formato XLSX fue verificado; el contenido estadístico sigue pendiente de revisión.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
