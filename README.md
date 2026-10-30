# Diseño de completación y productividad de pozos no convencionales en Vaca Muerta

Proyecto final del curso de Ciencia de Datos — **EnergIA Digital 2026**.
**Desarrollado por:** Carolina Bailon Trujillo — *Junior Data Analyst*

Trabajo individual. Las decisiones de alcance, criterio y metodología las definí y justifiqué a lo largo del análisis; me apoyé en herramientas de IA como copiloto, y lo documento al final de este README.

## El problema

Un pozo no convencional no produce por sí solo: la roca de Vaca Muerta tiene el petróleo atrapado adentro y hay que agrietarla. Para eso se perfora un tramo horizontal de varios kilómetros y se bombea agua con arena a alta presión, en decenas de etapas sucesivas. La arena queda trabando las fracturas para que no se cierren.

Ese conjunto de decisiones —cuán largo es el tramo horizontal, cuántas etapas, cuánta arena y cuánta agua por etapa— es el **diseño de completación**, y concentra buena parte del costo de terminar el pozo. La operadora lo define antes de saber cuánto va a producir: una vez bombeada, la arena no se recupera. Sobreinvertir es plata enterrada; subinvertir deja petróleo en el subsuelo.

## Objetivo

Estimar **cuánto petróleo va a producir un pozo en su primer año a partir de las decisiones de diseño que se toman antes de fracturarlo**, y entender cómo cambió ese diseño en la última década.

Es un problema de **aprendizaje supervisado**, y lo abordo de las dos formas. Como **regresión**, prediciendo los metros cúbicos de petróleo acumulados en los primeros 12 meses. Y como **clasificación**, prediciendo si el pozo va a superar la producción típica. No son la misma pregunta con otra cara: se miden distinto y, como demuestro, no dan el mismo resultado.

Sobre el final doy vuelta la pregunta y saco la variable objetivo de la ecuación: con **aprendizaje no supervisado** pregunto si los pozos se agrupan solos en tipos de diseño, sin decirle al algoritmo cuánto produjo ninguno.

## Datos

Tres datasets abiertos de la Secretaría de Energía, todos incluidos en el repositorio:

| Fuente | Contenido | Período | Registros |
|---|---|---|---|
| **Datos de fractura de pozos (Adjunto IV)** | Una fila por operación de fractura: longitud de rama, etapas, arena, agua, etc. | 2009 → 2026 | 4.890 |
| **Producción de pozos de gas y petróleo** | Una fila por pozo y mes: producción de petróleo y gas | 2006 → 2026 | 136.380 |
| **Listado de pozos** | Coordenadas, cota y profundidad de cada pozo | — | 2.282 |

## Alcance elegido

**Pozos horizontales con rama de al menos 500 m.** El dataset original mezcla dos poblaciones que no son comparables: los verticales convencionales y los horizontales no convencionales. Tras la limpieza, el alcance se define en **2.603 pozos**.

## Estructura del repositorio

```text
vaca-muerta-predictive-analytics/
├── README.md
├── requirements.txt
├── data/
│   ├── fractura_adjunto_iv.csv       # dataset original del portal
│   ├── produccion_filtrada.csv.gz    # producción mensual
│   ├── pozos_ubicacion.csv           # coordenadas y cota
│   └── processed/
│       └── pozos_analitico.csv       # dataset limpio autogenerado
├── docs/
│   └── presentacion.pdf              # diapositivas de defensa
├── src/
│   └── utils.py                      # funciones compartidas de estilo y carga
└── notebooks/
    ├── 01_eda_preentrega2.ipynb           # exploración, limpieza y feature engineering
    ├── 02_modelado_preentrega3.ipynb      # regresión predictiva
    ├── 03_clasificacion_preentrega3.ipynb # clasificación binaria
    └── 04_clustering_preentrega4.ipynb    # descubrimiento de familias de diseño

```

## Cómo reproducir

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

```

Los cuatro notebooks corren de punta a punta de forma autocontenida.

## Resultados del Modelado (Regresión)

**Modelo elegido: Random Forest.** Evaluado sobre los pozos fracturados en 2024-2025, con entrenamiento exclusivo en pozos anteriores:

| Modelo | MAE (m³) | R² | Mejora vs Referencia |
| --- | --- | --- | --- |
| Referencia (mediana) | 14.138 | -0,180 | — |
| Regresión Lineal (Ridge) | 10.814 | 0,240 | 23% |
| **Random Forest** | **10.596** | **0,263** | **25%** |

### El hallazgo central: la partición importa más que el modelo

El mismo modelo evaluado con una partición aleatoria da un **R² de 0,52** (el doble). La validación aleatoria infla el resultado porque le deja ver al modelo pozos contemporáneos. Como el diseño en Vaca Muerta cambió muchísimo, **la métrica temporal (R² 0,26) es la única honesta** para predecir pozos futuros.

## Resultados de la Clasificación

| Modelo | Exactitud | Precisión | Sensibilidad | F1 | ROC-AUC |
| --- | --- | --- | --- | --- | --- |
| Regresión Logística | 0,735 | 0,747 | 0,929 | 0,828 | 0,742 |
| **Random Forest** | **0,750** | **0,773** | 0,899 | **0,831** | **0,744** |

**Hallazgo:** Tomar el modelo de regresión (Notebook 02) y comparar su predicción contra el umbral funciona mejor que entrenar un clasificador puro (AUC 0,791 vs 0,744). Binarizar el objetivo tira información valiosa.

## Resultados del Clustering

Descubrí cuatro familias históricas de diseño usando solo variables de intensidad operativa:

1. **Intensivo moderno (2024):** 2.800 m rama, 48 etapas, 24,8 m³/m agua.
2. **Intermedio (2020):** 2.256 m rama, 29 etapas, 18,4 m³/m agua.
3. **Arena importada (2016):** 1.244 m rama, 15 etapas, 90% arena importada.
4. **Baja intensidad (2017):** 1.017 m rama, 7 etapas.

## Conclusión Técnica y de Negocio

1. **Alargar la rama es la palanca más grande.** Por cada 900m adicionales, se asocian 7.400 m³ extra de petróleo.
2. **Apretar las etapas suma; más arena ya no tanto.** Fracturar más denso aporta valor, pero la intensidad de arena muestra rendimientos decrecientes.
3. **Validación realista:** Si un modelo se va a usar para diseñar pozos el año que viene, debe evaluarse con particiones temporales estrictas, de lo contrario reportará el doble de precisión de la real.

---

*Nota sobre uso de IA: Utilicé IA generativa como copiloto para sintaxis de pandas, scikit-learn y optimización de visualizaciones Plotly. Las decisiones metodológicas, justificaciones de negocio, ingeniería de variables y definición de alcance fueron de auditoría y autoría exclusivamente humana.*

```
