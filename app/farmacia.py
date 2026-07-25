import streamlit as st
import ollama
import time
from PIL import Image
import io

st.set_page_config(
    page_title="DermaConsulta | María Cris",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0b0b0b; color: #e5e5e5; }
    h1 { color: #f5c518 !important; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 0.2rem; }
    .subtitle { color: #a3a3a3; font-size: 1.05rem; margin-bottom: 1.5rem; }
    .report-box {
        background-color: #111111;
        border-left: 4px solid #f5c518;
        padding: 1.5rem 1.75rem;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.92rem;
        line-height: 1.55;
        color: #e5e5e5;
    }
    .disclaimer {
        background-color: #1a1a1a;
        border: 1px solid #333;
        padding: 0.9rem 1.1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #a3a3a3;
        margin-top: 1.2rem;
    }
    [data-testid="stSidebar"] {
        background-color: #0f0f0f;
        border-right: 1px solid #2a2a2a;
    }
    .stButton > button {
        background-color: #f5c518;
        color: #111;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.55rem 1.2rem;
    }
    .stButton > button:hover {
        background-color: #e0b40f;
        color: #111;
    }
</style>
""", unsafe_allow_html=True)

# ---------- PROMPT DE VALIDACIÓN ----------
PROMPT_VALIDACION = """Tu única tarea es clasificar la imagen.

Responde con UNA SOLA PALABRA:

VALIDA
o
NO_VALIDA

Reglas:
- Escribe VALIDA solo si la imagen muestra claramente una cara humana o piel humana.
- En CUALQUIER otro caso escribe NO_VALIDA (objetos, placas electrónicas, circuitos, manos sujetando objetos, carteles, texto, paisajes, animales, ropa, herramientas, etc.).

Ejemplos:
- Foto de una cara → VALIDA
- Foto de una mejilla con granos → VALIDA
- Foto de una placa electrónica → NO_VALIDA
- Foto de una mano sosteniendo un objeto → NO_VALIDA
- Foto de un documento → NO_VALIDA

No describas la imagen.
No expliques.
No agregues puntuación ni texto extra.
Solo escribe: VALIDA o NO_VALIDA
"""

# ---------- PROMPT DERMATOLÓGICO ----------
PROMPT_DERMATOLOGICO = """[MODO: MÉDICO DERMATÓLOGO ESPECIALISTA]
Eres un experto en diagnóstico visual. Tu prioridad es la precisión en el grado de severidad.

[REGLA DE ESCANEO]: Antes de responder, analiza toda el área visible. Si hay múltiples lesiones, NO las trates como eventos aislados, sino como un cuadro clínico sistémico. Si hay más de 10 lesiones inflamatorias, clasifica automáticamente como Grado II o superior.

- Evita redundancias: si describes un signo vascular (como eritema o congestión) en la sección de 'Signos Vasculares', NO lo repitas en la sección de 'Configuración' o 'Cadena de Razonamiento'.
- Cada dato debe aparecer en su sección técnica correspondiente una sola vez.

1. ANÁLISIS TOPOGRÁFICO: Identificación anatómica precisa (Región malar, cigomática, mandibular, frontal).
2. SEMIOLOGÍA CUTÁNEA: Describe la morfología (Mácula, Pápula, Pústula, Nódulo, Quiste, Vesícula).
3. CRITERIOS DE VALIDACIÓN:
   - Determina si es un proceso Inflamatorio (Acné, Rosácea, Dermatitis).
   - Determina si es un proceso Pigmentario (Melasma, Léntigo).
   - Determina si hay signos de Alerta (Lesiones sospechosas, Nevus atípicos).

FORMATO MÉDICO DE SALIDA:

# EXPEDIENTE DERMATOLÓGICO

## LOCALIZACIÓN ANATÓMICA
[Detalle preciso]

## CRITERIOS DE OBSERVACIÓN
[Análisis profundo: Describe la densidad de las lesiones por cm² y el compromiso de la barrera cutánea]

## HALLAZGOS SEMIOLÓGICOS
- **Tipo de Lesión:** [Clasificación médica]
- **Configuración:** [Agrupada, lineal, difusa, confluente]
- **Signos Vasculares:** [Eritema activo, congestión vascular]

## DIAGNÓSTICO MÉDICO SUGERIDO
[Nombre clínico exacto y grado de severidad según escala GAGS o Cook]

## PROTOCOLO FARMACOLÓGICO/TERAPÉUTICO
- **Tópico:** [Ej: Peróxido de Benzilo 5% + Clindamicina 1% si hay pústulas]
- **Sistémico:** [Ej: Doxiciclina 100mg/día si el grado es II o III]
- **Mantenimiento:** [Uso de Syndets y Fotoprotección no comedogénica]

## ADVERTENCIA MÉDICA PROFESIONAL
Este reporte es una asistencia por IA. Se requiere validación por un médico colegiado.

[FIN DEL EXPEDIENTE]
"""

with st.sidebar:
    st.markdown("### Parámetros del modelo")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.10, 0.05)
    top_p = st.slider("Top-P", 0.1, 1.0, 0.70, 0.05)
    repeat_penalty = st.slider("Penalización de repetición", 1.0, 2.0, 1.85, 0.05)
    max_tokens = st.slider("Máximo de tokens", 300, 1500, 900, 50)

    st.markdown("---")
    st.markdown("**Modelo**  \n`llama3.2-vision:11b`")
    st.markdown("**Cliente**  \nMaría Cris")
    st.caption("Especialización en Ciencia de Datos")

st.markdown("<h1>DermaConsulta</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Asistente de segunda opinión dermatológica · Salón María Cris</p>', unsafe_allow_html=True)

if "expediente" not in st.session_state:
    st.session_state.expediente = None
if "latencia" not in st.session_state:
    st.session_state.latencia = None

col_izq, col_der = st.columns([1, 1.25], gap="large")

with col_izq:
    st.markdown("#### Registro fotográfico")
    archivo = st.file_uploader(
        "Seleccione una imagen (JPG / PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if archivo is not None:
        imagen = Image.open(archivo)
        st.image(imagen, use_container_width=True)

        if st.button("Generar análisis", use_container_width=True):
            buffer = io.BytesIO()
            imagen.save(buffer, format="JPEG")
            img_bytes = buffer.getvalue()

            inicio = time.time()

            with st.spinner("Validando imagen..."):
                try:
                    # --- Validación ---
                    validacion = ollama.chat(
                        model="llama3.2-vision:11b",
                        messages=[{
                            "role": "user",
                            "content": PROMPT_VALIDACION,
                            "images": [img_bytes]
                        }],
                        options={
                            "temperature": 0.0,
                            "top_p": 0.3,
                            "num_predict": 8,
                            "stop": ["\n"]
                        }
                    )

                    raw = validacion["message"]["content"].strip().upper()
                    respuesta_val = raw.replace(".", "").replace(",", "").strip()

                    es_valida = (
                        respuesta_val == "VALIDA"
                        or respuesta_val.startswith("VALIDA")
                    ) and len(respuesta_val) < 15

                    if not es_valida:
                        st.session_state.expediente = (
                            "IMAGEN NO VÁLIDA PARA ANÁLISIS DERMATOLÓGICO.\n\n"
                            "No se identifica una zona cutánea facial o corporal adecuada.\n"
                            "Por favor cargue una fotografía clara de la zona a evaluar."
                        )
                        st.session_state.latencia = time.time() - inicio
                    else:
                        # --- Análisis con tu estructura original ---
                        with st.spinner("Generando expediente dermatológico..."):
                            analisis = ollama.chat(
                                model="llama3.2-vision:11b",
                                messages=[{
                                    "role": "user",
                                    "content": PROMPT_DERMATOLOGICO,
                                    "images": [img_bytes]
                                }],
                                options={
                                    "temperature": temperature,
                                    "top_p": top_p,
                                    "repeat_penalty": repeat_penalty,
                                    "num_predict": max_tokens,
                                    "stop": ["[FIN DEL EXPEDIENTE]"]
                                }
                            )
                            st.session_state.expediente = analisis["message"]["content"]
                            st.session_state.latencia = time.time() - inicio

                except Exception as e:
                    st.error(f"Error de comunicación con el modelo: {e}")
                    st.session_state.expediente = None

with col_der:
    st.markdown("#### Resultado del análisis")

    if st.session_state.expediente:
        st.markdown(
            f'<div class="report-box">{st.session_state.expediente}</div>',
            unsafe_allow_html=True
        )
        if st.session_state.latencia is not None:
            st.caption(f"Tiempo de procesamiento: {st.session_state.latencia:.2f} s")
    else:
        st.info("Cargue una fotografía clínica para iniciar el análisis.")

st.markdown("""
<div class="disclaimer">
<strong>Aviso importante</strong><br>
Este sistema utiliza un modelo de visión multimodal con fines de asistencia y segunda opinión.
No reemplaza la evaluación clínica presencial ni el criterio de un médico colegiado.
</div>
""", unsafe_allow_html=True)
