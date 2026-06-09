# Cuneiform Sex Estimator 📈 🦴

¡Bienvenido al **Cuneiform Sex Estimator**! Esta es una aplicación web interactiva desarrollada en **Python** con **Streamlit**, diseñada para la estimación del sexo biológico a partir de las dimensiones de los huesos cuneiformes del pie (Medial, Intermedio y Lateral). 

El sistema permite procesar archivos masivos de datos (ficheros Excel) de forma automatizada, aplicando modelos matemáticos previamente validados y estandarizados según parámetros poblacionales de entrenamiento.

Realizado por: **Esteban Arroyo**

---

## 🔬 Respaldos e Indicadores del Modelo

Para garantizar la consistencia de las estimaciones, cualquier dato nuevo es normalizado automáticamente mediante el método *Z-score* utilizando la media ($\bar{x}$) y desviación estándar ($s$) fijas del conjunto de calibración original (*training dataset*).

El sistema cuenta con 4 modelos predictivos basados en regresión logística:
1. **All of the cuneiform bones:** Modelo global ponderado utilizando variables de los tres huesos.
2. **Medial Cuneiform:** Optimizado exclusivamente para el cuneiforme medial.
3. **Intermediate Cuneiform:** Optimizado para el cuneiforme intermedio.
4. **Lateral Cuneiform:** Optimizado para el cuneiforme lateral.

La clasificación final utiliza una función sigmoide:
* $P(\text{Sexo}) \ge 0.5 \rightarrow$ **Female** (Femenino)
* $P(\text{Sexo}) < 0.5 \rightarrow$ **Male** (Masculino)

---

## 🛠️ Características de la Aplicación

* **Carga de Archivos:** Soporte para archivos Excel (`.xlsx`, `.xls`).
* **Validación de Columnas:** Comprobación automática de variables requeridas antes de realizar el cálculo para evitar errores de ejecución.
* **Procesamiento en Bloque:** Permite calcular las estimaciones de múltiples individuos al mismo tiempo.
* **Vista Previa en Tiempo Real:** Visualización instantánea de los resultados en la interfaz antes de la descarga.
* **Exportación de Datos:** Descarga directa de los resultados consolidados en un nuevo fichero Excel que incluye los valores $Y$ calculados, las probabilidades y la asignación final de sexo.

---

## 📊 Requisitos del Archivo de Entrada (Excel)

Para que los modelos funcionen correctamente, el archivo de Excel cargado debe contener las variables métricas correspondientes en sus columnas (respetando las mayúsculas). Dependiendo del modelo a elegir, el sistema buscará:

| Modelo Seleccionado | Variables Requeridas en el Excel |
| :--- | :--- |
| **All of the cuneiform bones** | `HM`, `LM2`, `HM3`, `LMN2` |
| **Medial Cuneiform** | `HM` |
| **Intermediate Cuneiform** | `LM2`, `HM2`, `LMN2` |
| **Lateral Cuneiform** | `LM3`, `HM3` |

---

## 📄 Licencia

Este proyecto es de uso libre con fines educativos. Si lo modificas, agradeceré que menciones la fuente original.

---

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

▶️ Uso local Para ejecutar el dashboard en tu entorno local:

```bash
streamlit run main.py
```

---

## 🌐 Versión en línea

El proyecto lo puedes visualizar en el siguiente link:
👉 [Enlace al dashboard en Streamlit Cloud](https://cueiformapp-esteban2021.streamlit.app/)

---

## 👨‍💻 Autor

Esteban Arroyo
Desarrollado con ❤️ usando Streamlit
