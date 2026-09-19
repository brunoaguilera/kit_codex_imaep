# Trabajo de series temporales: IMAEP de Paraguay

Implementá una primera entrega académica reproducible sobre el **Indicador Mensual de Actividad Económica del Paraguay (IMAEP)** del Banco Central del Paraguay (BCP).

## Contexto y estado real de los archivos

La consigna actual pide **gráfica de la serie temporal y datos estadísticos básicos**. La imagen `referencias/flujo_series_temporales.jpg` muestra el flujo completo de estudio, pero en esta entrega solo hay que cubrir datos/contexto y exploración inicial. No implementes todavía pronósticos, ARIMA/SARIMA ni aprendizaje automático.

**Este kit NO contiene el histórico descargado.** ChatGPT verificó la página oficial y localizó su enlace XLSX el 18 de septiembre de 2026, pero no logró transferir el archivo a su entorno. No se inspeccionaron sus hojas ni se verificó la cobertura temporal. El script incluido descarga el original; la validación estadística debe realizarse después.

Tema propuesto: **«Análisis exploratorio de la actividad económica del Paraguay mediante el IMAEP mensual, 2016–2025»**.

## 1. Revisión y descarga

- Leé primero las instrucciones locales, `AGENTS.md`, README y las convenciones del repositorio, si existen. No modifiques otros proyectos, no elimines cambios del usuario y no hagas commits ni push.
- Trabajá en una carpeta independiente para esta tarea. No crees frontend, backend ni base de datos: alcanza con scripts y un informe.
- Ejecutá `python3 descargar_imaep.py`. Solo requiere biblioteca estándar de Python 3.10+ y acceso a Internet. El destino predeterminado es `data/raw/`.
- Si ya existe el original, preservalo, verificá su procedencia y reutilizalo; no descargues otra versión silenciosamente.
- Si la descarga falla, informá el error. No inventes, simules ni interpoles datos para suplirlo. Consultá el botón Descargar de la página oficial o solicitá el Excel manual cuando realmente sea necesario.

Fuente oficial:
https://www.bcp.gov.py/web/institucional/indicador-mensual-de-actividad-economica-del-paraguay-imaep-

Descarga localizada:
https://www.bcp.gov.py/documents/20117/2659103/Indicador%2BMensual%2Bde%2Bla%2BActividad%2BEcon%C3%B3mica%2Bdel%2BParaguay.xlsx/27688483-a192-9797-37f7-1f8b184bf430?t=1789069578102

Nota metodológica del BCP:
https://www.bcp.gov.py/documents/20117/0/Nota_Metod_IMAEP_%2014_06_18.pdf/0aa99738-45b8-49cd-ecd8-91a9c0e4fd1e?t=1741977277921

## 2. Selección de la serie y trazabilidad

Inspeccioná las hojas, encabezados, notas, fechas y unidades del Excel antes de programar la extracción. Documentá hoja, columna y rango utilizados; no supongas sus nombres.

Elegí el **nivel del IMAEP total, serie original**. No lo confundas con variaciones porcentuales, series sin agricultura/binacionales, índices sectoriales, series desestacionalizadas o ciclo-tendencia. La nota metodológica de referencia utiliza base 2014; confirmá en el archivo descargado su base exacta antes de escribir las unidades del informe.

El período objetivo es enero de 2016 a diciembre de 2025. Si está completo, son **120 observaciones mensuales esperadas**, no verificadas de antemano. Si no existe esa cobertura o la serie resulta ambigua, informá lo encontrado y no presentes otro período como si fuera el solicitado.

Preservá el original sin editar en `data/raw/`. Guardá la fuente, fecha real de descarga, hash SHA-256 y cualquier nota sobre datos preliminares o revisiones. Es una versión histórica consultada ahora, no necesariamente los valores que se publicaron originalmente en cada mes.

## 3. Preparación y controles de calidad

Generá `data/processed/imaep_2016_2025.csv` con columnas `fecha,imaep`, UTF-8, separador coma y punto decimal. `fecha` debe ser ISO `YYYY-MM-01`: el día 1 identifica el mes; **no significa frecuencia diaria**.

Ordená cronológicamente. Verificá tipos numéricos, valores finitos, duplicados, meses faltantes, continuidad mensual y extremos del período. No redondees antes de calcular. No rellenes ni elimines registros silenciosamente. Compará todos los valores del CSV con las celdas del Excel original y documentá su correspondencia.

Reportá controles y resultados en `outputs/calidad_datos.json`. Detené el análisis si una inconsistencia impide interpretar correctamente la serie.

## 4. Entrega solicitada

Generá mediante código, no copiando resultados a mano:

1. **Gráfica de líneas de la serie original**, con título, meses/años en el eje horizontal, unidad verificada en el vertical y fuente. Exportá `outputs/serie_imaep.png` en resolución legible.
2. **Estadísticas básicas**: cantidad válida y faltante, media, mediana, mínimo y máximo con todos sus meses si hay empate, rango, cuartiles Q1 y Q3, rango intercuartílico, varianza muestral y desviación estándar muestral. Indicá denominador `n-1` y método de cuantiles utilizado; redondeá solo la presentación. Exportá tabla CSV.
3. **Informe breve en español**, `outputs/informe.md`, con objetivo, fuente, definición, unidad, período, frecuencia, calidad de datos, gráfica, tabla y conclusión basada en resultados.

La interpretación debe distinguir hechos observables de hipótesis. No atribuyas cambios a pandemia, clima, políticas u otras causas sin evidencia adicional citada. Las estadísticas del nivel describen el conjunto del período; no prueban estacionariedad. No afirmes haber confirmado estacionalidad solo con la gráfica. El IMAEP es un indicador de actividad, no el valor del PIB mensual.

No agregues pruebas de estacionariedad, descomposición, ACF/PACF, modelos ni pronósticos en esta fase. Podrán constituir una ampliación posterior si la consigna lo exige.

## 5. Implementación y verificación

Usá Python y Matplotlib; preferí dependencias mínimas y un entorno aislado, respetando las reglas del repositorio. Registrá las versiones realmente instaladas, sin inventarlas. Un gráfico por figura y diseño sencillo. No se requiere una aplicación web.

Entregá un script ejecutable desde la raíz, instrucciones de instalación/ejecución, dependencias y pruebas. Probá al menos: cobertura esperada, ausencia de duplicados/faltantes, equivalencia CSV-original y consistencia `desviación_estándar² ≈ varianza`. Si hay un error real, no fuerces un PASS.

Implementá y ejecutá la solución cuando los datos estén disponibles. Terminá informando archivo fuente, serie seleccionada, período comprobado, cantidad real de observaciones, controles ejecutados, rutas de resultados, comandos reproducibles y cualquier limitación pendiente.
