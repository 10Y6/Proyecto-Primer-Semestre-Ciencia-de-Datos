# 🍛 La Inflación en el Plato: Análisis de Precios en La Habana (2024-2025)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Data](https://img.shields.io/badge/Datos_Reales-In_Situ-red?style=for-the-badge&logo=google-maps&logoColor=white)

> **Proyecto de Primer Semestre - Ciencia de Datos**

## 📖 ¿De qué va esto?

Todos sabemos que las cosas están caras, pero... ¿qué tan caras? ¿Cuánto poder de compra hemos perdido realmente?

Este proyecto nace de la necesidad de la ciudad de La Habana, más allá de lo que dicen las noticias. No me limité a buscar tablas de Excel en internet; salí a la calle a buscar los precios reales. El objetivo fue rastrear cómo ha cambiado el costo de la vida en La Habana desde Enero de 2024 hasta Noviembre de 2025.

Aquí respondo preguntas como:
*   ¿Es verdad que si el dólar baja, la comida baja? (Spoiler: No siempre).
*   ¿Cuánto cuesta hoy el plato más humilde: un arroz con huevo?
*   ¿Para cuánto le da el salario a un maestro?

## 🏗️ ¿De dónde saqué los datos?

Para que esto fuera serio, tuve que mezclar tres fuentes distintas:

1.  **🏛️ Lo Oficial (ONEI):** Procesé los informes de la Oficina Nacional de Estadística para tener una línea base y saber los salarios promedio.
2.  **🌐 Lo Digital (Scraping):**
    *   Monitoricé la tasa del dólar informal (El Toque).
    *   Analicé grupos de compra-venta en redes sociales (Facebook) procesando capturas de pantalla de ofertas reales.
3.  **📍 La Calle (Trabajo de Campo):**
    *   Esto fue lo más duro. Durante Noviembre de 2025, visité físicamente **más de 20 mercados** en La Habana (MIPYMES, bodegones privados) para anotar precios y tomar evidencia fotográfica.
    *   *Lugares como:* Mercado de 23 y 4, Bodegón de Águila, Mercado Toledo, Lo D' Yona, etc.

## 📊 Lo que encontré (Visualizaciones)

Todo el análisis está contado paso a paso en el notebook `story.ipynb`, pero aquí te adelanto lo más interesante:

*   **El Índice "Congrís con Huevo":** Creé mi propio índice económico basado en el costo de una ración de arroz, frijoles, huevo y aceite.
*   **La Resistencia a Bajar:** Demostré con datos que cuando el dólar sube, los precios de la comida suben disparados, pero cuando el dólar baja, los precios bajan lentísimo o se quedan igual.
*   **El Caos de los Precios:** Clasifiqué qué productos son más estables y cuáles son mas caóticos, hablando de precios.

## 📂 Sobre los Datos crudos y el Peso del Repo

Aquí viene un detalle importante. Como te imaginarás, las fotos de los mercados, las capturas de pantalla de los grupos y los PDFs de la ONEI pesan muchísimo.

Para no hacer este repositorio gigante e imposible de descargar, **he subido toda esa evidencia cruda a Google Drive**.

*   **¿Necesitas descargar eso para correr el código?** **NO.**
    El repositorio ya incluye los archivos `.json` procesados, así que puedes clonar esto y ejecutar los notebooks sin problemas.
*   **¿Quieres auditar que los datos son reales?**
    Entonces sí, aquí tienes el enlace a la carpeta con toda la evidencia original:

[![Google Drive](https://img.shields.io/badge/Google_Drive-Ver_Evidencia-0F9D58?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/drive/folders/1GCjTfHnapiiVgJq7zwdOQ-_-d3yBR0bH?usp=sharing)

## 🗂️ Estructura del Proyecto

```text
├── data_in_situ/            # 📍 Módulo de recolección de datos físicos
│   ├── db_in_situ.json      # Base de datos procesada de los mercados
│   ├── main.py              # Script principal de entrada de datos manual
│   ├── models.py            # Funciones para añadir datos al .json
│   └── product_manager.py   # Funciones para gestionar y guardar productos
│
├── data_online/             # 🌐 Módulo de datos de redes sociales
│   ├── db_online.json       # Base de datos procesada de ofertas online
│   ├── data_fill.py         # Funciones gestionar los productos
│   ├── main.py              # Script de ejecución principal
│   └── models.py            # Funciones para crear y añadir al .json
│
├── data_onei/               # 🏛️ Datos oficiales procesados
│   ├── min_max_prices.json  # Rangos de precios históricos (ONEI)
│   └── salary_median.json   # Datos de salarios por sector
│
├── data_eltoque/            # 💵 Datos de la tasa de cambio no oficial del dólar
│   ├── api_raw.json         # .json obtenido de la API en el momento de ejecucion del script
│   ├── db_exch_rate.json    # Histórico limpio de la tasa del dólar
│   └── eltoque_scraper.py   # Script para obtener la tasa diaria en un periodo de 2 años
│
├── Functions.py             # 🛠️ Librería de utilidades (limpieza, normalización,carga y estadísticas)
├── visualizations.py        # 📊 Para generar los 5 gráficos principales (Plotly)
├── story.ipynb              # 🌟 NOTEBOOK PRINCIPAL (Narrativa y Resultados)
└── Readme.md                # Documentación del proyecto
```
**Autor:** Alejandro Manuel de la Torre Almarales

*Hecho con escasas horas de sueño y bastantes caminatas bajo el sol de La Habana.*