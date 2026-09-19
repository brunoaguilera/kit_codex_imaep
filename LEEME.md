# Primera entrega — IMAEP de Paraguay

Entrega académica reproducible sobre el nivel mensual del **IMAEP total, serie original**, para enero de 2016 a diciembre de 2025. Incluye extracción, controles de calidad, CSV limpio, estadísticas descriptivas, gráfica e informe. No incluye modelos ni pronósticos.

## Fuente y selección

- Fuente: Banco Central del Paraguay (BCP).
- Original preservado: `data/raw/imaep_bcp_original.xlsx`.
- SHA-256: `7c413354fb6bbaf56b2797e33e72e33f3de91059a5a358e9e0c5dc15085c4c94`.
- Hoja y celdas: `IMAEP!B274:C393`; fecha en B y `IMAEP Serie Original` en C.
- Unidad confirmada en el libro: índice base 2014 = 100.
- Los 120 registros del período tienen asterisco: cifras preliminares, sujetas a revisión.

El archivo de la raíz `Indicador Mensual de la Actividad Económica del Paraguay.xlsx`, aportado por el usuario, se conservó intacto. Su hash coincide exactamente con la copia de `data/raw/`.

## Instalación y ejecución

Requiere Python 3.10 o posterior. Para regenerar DOCX y PDF también se necesitan `pandoc` y `xelatex`. Desde la raíz:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analizar_imaep.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python generar_documentos.py
```

El análisis no descarga ni modifica el Excel. Para usar otra copia explícita:

```bash
.venv/bin/python analizar_imaep.py --input "/ruta/al/archivo.xlsx"
```

Si el original todavía no existe, se puede intentar primero:

```bash
python3 descargar_imaep.py
```

El descargador no sobrescribe archivos existentes. En esta ejecución, el BCP respondió `HTTP 403` por una verificación de Cloudflare; el binario se obtuvo después desde la misma página oficial mediante una sesión gráfica y se comprobó contra el archivo aportado por el usuario.

Página oficial: https://www.bcp.gov.py/web/institucional/indicador-mensual-de-actividad-economica-del-paraguay-imaep-

## Resultados

- `data/processed/imaep_2016_2025.csv`: 120 observaciones, UTF-8, coma y punto decimal.
- `outputs/calidad_datos.json`: controles y correspondencia de cada fila CSV con su celda Excel.
- `outputs/serie_imaep.png`: gráfica temporal.
- `outputs/estadisticas_basicas.csv`: tabla estadística.
- `outputs/informe.md`: informe breve en español.
- `analizar_imaep.py`: generación reproducible de todos los resultados.
- `tests/test_analizar_imaep.py`: cobertura, continuidad, duplicados, equivalencia y consistencia estadística.
- `docs/trabajo_practico_imaep.docx`: trabajo práctico editable con datos e imágenes.
- `docs/trabajo_practico_imaep.pdf`: versión PDF del mismo trabajo práctico.
- `docs/imaep_colab.ipynb`: notebook para Google Colab con datos, controles, estadísticas e imágenes.
- `generar_documentos.py`: generación reproducible de los documentos mediante Pandoc y XeLaTeX.

Los resultados se regeneran sobrescribiendo únicamente los archivos derivados. El Excel original no se altera. Ante una inconsistencia de fechas, tipos, cobertura o equivalencia, el script detiene el análisis y deja el error en `outputs/calidad_datos.json`; no imputa ni elimina datos silenciosamente.
