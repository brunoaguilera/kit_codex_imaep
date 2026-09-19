# Análisis exploratorio del IMAEP mensual de Paraguay, 2016-2025

## Objetivo y fuente

Esta primera entrega describe el nivel mensual del Indicador Mensual de Actividad Económica del Paraguay (IMAEP) total, serie original, entre enero de 2016 y diciembre de 2025. El IMAEP ofrece una señal de corto plazo sobre la producción de bienes y servicios a precios constantes; no debe interpretarse como el valor del PIB mensual.

La fuente es el [Banco Central del Paraguay](https://www.bcp.gov.py/web/institucional/indicador-mensual-de-actividad-economica-del-paraguay-imaep-). Se usó el libro oficial `imaep_bcp_original.xlsx` (SHA-256 `7c413354fb6bbaf56b2797e33e72e33f3de91059a5a358e9e0c5dc15085c4c94`). El archivo corresponde a una versión histórica consultada para este trabajo: sus cifras pueden incorporar revisiones respecto de publicaciones anteriores.

## Serie seleccionada y unidad

- Hoja: `IMAEP`.
- Encabezado: `C9`, **IMAEP Serie Original**.
- Fechas y valores: `IMAEP!B274:C393`; fechas en la columna B y nivel en la columna C.
- Unidad: índice base 2014 = 100, según `IMAEP!B8`.
- Frecuencia: mensual. En el CSV, el día `01` solo identifica cada mes y no implica frecuencia diaria.
- Verificación cruzada: `IMAEP-apertura por sectores!B35:B154 y O35:O154`, encabezados `O9:O10` (**IMAEP / Serie Original**).

No se seleccionaron variaciones porcentuales, el IMAEP sin agricultura ni binacionales, sectores, serie ajustada ni tendencia-ciclo.

## Calidad de los datos

El período contiene **120 observaciones válidas** y **0 meses faltantes**. Comienza en 2016-01-01 y termina en 2025-12-01; no se detectaron fechas duplicadas, valores no numéricos ni valores no finitos. Los 120 registros del período tienen asterisco en el libro y el BCP los identifica como **cifras preliminares, sujetas a revisión**.

Todos los valores escritos en el CSV fueron releídos y comparados exactamente con las celdas del Excel. La segunda aparición de la serie en la hoja sectorial también coincide en los 120 meses. El detalle de cada correspondencia y de los controles está en [`calidad_datos.json`](calidad_datos.json).

## Serie temporal

![Serie temporal del IMAEP](serie_imaep.png)

La gráfica muestra fluctuaciones mensuales y niveles generalmente mayores hacia el final del período que al comienzo. El menor nivel observado fue **97.782** en **2020-04-01** y el mayor fue **158.480** en **2025-12-01**. Estas son descripciones del archivo; por sí solas no identifican causas ni prueban tendencia, estacionalidad o estacionariedad.

## Estadísticas básicas

| Estadística | Resultado |
|---|---:|
| Cantidad válida | 120 |
| Cantidad faltante | 0 |
| Media | 119.985 |
| Mediana | 118.846 |
| Mínimo | 97.782 (2020-04-01) |
| Máximo | 158.480 (2025-12-01) |
| Rango | 60.698 |
| Q1 | 111.540 |
| Q3 | 126.239 |
| Rango intercuartílico | 14.699 |
| Varianza muestral | 144.822 |
| Desviación estándar muestral | 12.034 |

La varianza y la desviación estándar son muestrales y usan denominador **n-1**. Q1 y Q3 se calcularon mediante cuantiles inclusivos con interpolación lineal, posición `(n-1)*p`. Los cálculos usan los valores completos del Excel; el redondeo a tres decimales es solo de presentación. La tabla reutilizable está en [`estadisticas_basicas.csv`](estadisticas_basicas.csv).

## Conclusión y alcance

En el conjunto 2016-2025, la media fue **119.985**, la mediana **118.846** y el 50 % central de los niveles se ubicó entre **111.540** y **126.239**. El rango total fue **60.698** puntos de índice. Estas medidas resumen niveles de una serie mensual preliminar; no constituyen un análisis causal ni un diagnóstico de estacionariedad.

Esta fase no incluye imputaciones, descomposición, ACF/PACF, pruebas de estacionariedad, modelos ni pronósticos.
