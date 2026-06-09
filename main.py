import streamlit as st
import pandas as pd
#import pandas.api.types as ptypes
import numpy as np
import io

# --- PARÁMETROS FIJOS DE NORMALIZACIÓN (TRAINING) ---
MEDIAS = {'HM': 30.95896, 'LM2': 17.85075, 'HM2': 21.04104, 'HM3': 23.63433, 'LM3': 23.25746, 'LMN2': 19.11791}
SD     = {'HM': 2.479274,  'LM2': 1.410260, 'HM2': 1.927296,  'HM3': 2.008594,  'LM3': 2.173607, 'LMN2': 15.791907}

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cuneiform calculator", page_icon="📈", layout="wide")

# --- FUNCION DE OPTIMIZACIÓN ---
@st.cache_data
def cargar_datos(archivo):
    """Carga el archivo Excel y lo mantiene en memoria cache."""
    return pd.read_excel(archivo)

def to_excel(df):
    """Convierte el DataFrame en un archivo Excel en memoria para la descarga."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Estimación')
    return output.getvalue()

# --- FUNCION SIGMOIDE ---
def sigmoid(Y):
    return 1 / (1 + np.exp(-Y))

# --- INICIALIZACIÓN DE LA SESIÓN (SESSION STATE) ---
if "df_resultado" not in st.session_state:
    st.session_state.df_resultado = None

# --- PANEL PRINCIPAL ---
st.markdown("""
    <div style="background-color: #5F9EA0; padding: 12px; border-radius: 0px 0px 10px 10px; position: relative;">
        <h3 style="color: white; text-align: center; margin: 0;">Cuneiform calculator</h3>
        <p style="color: white; font-size: 12px; position: absolute; bottom: 4px; left: 15px; margin: 0;">
            By: Esteban Arroyo
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div>
        <p style="color: black; font-size: 16px; padding: 12px">
            There are four equations that make it possible to estimate an individual’s sex using measurements of the cuneiform bones, which are described and shown in the paper titled "<spam><b>Sexual dimorphism in the cuneiform bones from a Chilean subactual osteological series</b></spam>"  (Alvarez, Isabela; Saldías, Eduardo; Arroyo, Esteban; Retamal, Rodrigo). All measurements must be in milimeters.
        </p>
        <p style="color: black; font-size: 16px; padding-left: 12px; padding-right:12px">
            The Excel file must have at least the following variables with this nomenclature as their names
        </p>
        <ul style="color: black; font-size: 16px; padding-left: 20px; padding-right:12px"">
            <li>HM</li>
            <li>HM2</li>
            <li>HM3</li>
            <li>LM2</li>
            <li>LM3</li>
            <li>LMN2</li>
        </ul>
        <p style="color: black; font-size: 16px; padding-left: 12px; padding-right:12px">
            Likewise, the Excel file must be clean and contain no missing or "Not Available" (NA) value.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🔍 Select your Excel file")
    archivo = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    st.write("---")

   
# --- LÓGICA DE PROCESAMIENTO ---
if archivo is not None:
    df_base = cargar_datos(archivo)

    # Render en el panel principal de la vista previa de entrada
    st.markdown("### 🔎 Data preview")
    st.dataframe(df_base.head(), use_container_width=True)
    st.write("---")

    with st.sidebar:
        opciones = {
            "All of the cuneiform bones": ['HM', 'LMN2'],
            "Medial Cuneiform": ['HM'],
            "Intermediate Cuneiform": ['LM2', 'HM2', 'LMN2'],
            "Lateral Cuneiform": ['LM3', 'HM3']
        }

        st.write("What do you want to do?")
        tipo_calculo = st.selectbox("Estimation with...:", ["Choose one..."] + list(opciones.keys()))
    
     
    if tipo_calculo != "Choose one...":
        variables_requeridas = opciones[tipo_calculo]
        # Verificar si las columnas necesarias existen en el Excel subido
        columnas_presentes = all(col in df_base.columns for col in variables_requeridas)
        if not columnas_presentes:
            st.error(f"❌ The Excel file does not contain the columns required for this model: {variables_requeridas}")
        else:
            with st.sidebar:
                st.success(f"✓ Columns detected for: {tipo_calculo}")
                # Procesar el cálculo directamente al presionar el botón
                if st.button("🛠️ Calculate Estimate"):
                    # 1) Extraer y Normalizar variables
                    df_filtrado = df_base[variables_requeridas].astype(float)
                    # Convertimos los diccionarios a Series de pandas mapeadas por columna
                    medias_series = pd.Series(MEDIAS)
                    sd_series = pd.Series(SD)
                    # Normalización usando los parámetros fijos del conjunto de entrenamiento
                    df_norm = (df_filtrado - medias_series) / sd_series
                    # 2) Selección del modelo estadístico y cálculo de Y
                    if tipo_calculo == "All of the cuneiform bones":
                        #y = -0.9632 + (-0.8997 * df_norm['AM']) + (-2.2791 * df_norm['HM']) + (0.5753 * df_norm['LM2']) + (-0.6781 * df_norm['HM3']) + (0.4159 * df_norm['LMN2'])
                        y = -0.1361 + (-2.4374 * df_norm['HM']) + (0.3875 * df_norm['LMN2'])
                    elif tipo_calculo == "Medial Cuneiform":
                        y = -0.1176 + (-2.3256 * df_norm['HM'])
                    elif tipo_calculo == "Intermediate Cuneiform":
                        y = -0.08882 + (-0.67539 * df_norm['LM2']) + (-1.13979 * df_norm['HM2']) + (0.52643 * df_norm['LMN2'])  
                    elif tipo_calculo == "Lateral Cuneiform":
                        y = -0.07016 + (-0.67515 * df_norm['LM3']) + (-1.03755 * df_norm['HM3'])
                    
                    # 3) Probabilidad y 4) Clasificación
                    probabilidades = sigmoid(y)
                    clasificacion = np.where(probabilidades >= 0.5, "Female", "Male")
                    # Construir dataframe final combinando los datos originales con los resultados
                    df_final = df_base.copy()
                    df_final['Y_score'] = y
                    df_final['Probability'] = probabilidades
                    df_final['Estimated_Sex'] = clasificacion
                    # Guardar en el Session State para que persista al renderizar
                    st.session_state.df_resultado = df_final
    else:
        #st.warning("👈 Please select a model from the menu in the sidebar to continue.")
        st.session_state.df_resultado = None


    # --- MOSTRAR RESULTADOS Y DESCARGA ---
    if st.session_state.df_resultado is not None:
        st.markdown("### 📶 Estimation results")

        # Mostrar las últimas columnas añadidas (Y, probabilidad, sexo) junto al ID si existe
        st.dataframe(st.session_state.df_resultado, use_container_width=True)

        # Generar archivo Excel binario
        excel_data = to_excel(st.session_state.df_resultado)

        st.markdown("### 💾 Download the File")

        st.download_button(
                label="📥 Download results as Excel",
                data=excel_data,
                file_name=f"estimacion_{tipo_calculo.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
    elif tipo_calculo == "Choose one...":
        st.warning("👈 Please select a model from the menu in the sidebar to continue.")

else:
    st.session_state.df_resultado = None
    st.warning("👈 Please upload an Excel file in the sidebar to get started.")





# streamlit run main.py