<div align="center">
  <h1>🩺 DermaConsulta AI</h1>
  <p><b>Asistente dermatológico multimodal (texto e imagen) acelerado en hardware local Intel Arc.</b></p>

  <p>
    <img src="https://img.shields.io/badge/Fedora_Linux_43-357EC7?style=for-the-badge&logo=fedora&logoColor=white" alt="Fedora 43" />
    <img src="https://img.shields.io/badge/Intel_Arc_B580-0071C5?style=for-the-badge&logo=intel&logoColor=white" alt="Intel Arc B580" />
    <img src="https://img.shields.io/badge/Podman-892CA0?style=for-the-badge&logo=podman&logoColor=white" alt="Podman" />
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  </p>
</div>

---

## 📌 ¿Qué hace este proyecto?

Analiza imágenes dermatológicas y responde consultas clínicas mediante modelos multimodales de visión y lenguaje (`llama3.2-vision:11b`). Todo corre de forma **100% local, privada y offline** sin enviar datos a APIs externas, aprovechando la aceleración por GPU Intel Arc.

---

## 🧠 Arquitectura del Software y Pipeline de Inferencia

La aplicación (`app/farmacia.py`) implementa un **pipeline de análisis clínico en dos etapas (Guardrail Pattern)** para optimizar el uso de recursos y evitar diagnósticos erróneos:

1. **Etapa 1 — Filtro de Validación (Guardrail):**  
   Antes de generar un análisis pesado, se ejecuta una consulta con `temperature=0.0` y respuesta determinista binaria (`VALIDA` / `NO_VALIDA`). Si la imagen no muestra piel humana (por ejemplo, placas electrónicas, objetos o documentos), el sistema interrumpe el proceso y notifica al usuario.
2. **Etapa 2 — Expediente Dermatológico Especializado:**  
   Si la imagen es válida, se procesa bajo un System Prompt especializado que evalúa topografía, semiología cutánea y escalas clínicas (como GAGS o Cook), estructurando un **Expediente Médico** completo con diagnóstico sugerido y protocolo terapéutico.
3. **Control Dinámico de Hiperparámetros:**  
   Desde la interfaz es posible ajustar en tiempo real la `temperatura`, `Top-P`, `penalización de repetición` y el límite de `tokens` enviados al motor de inferencia.

---

## 🐳 Imagen Base de Podman (Infraestructura de IA)

Para evitar la instalación manual de controladores y dependencias de cómputo pesado, el proyecto despliega la imagen oficial de Intel Analytics:

> **`docker.io/intelanalytics/ipex-llm-inference-cpp-xpu:latest`**

Esta imagen de contenedor ya incluye preinstalado todo lo necesario para la **Intel Arc B580**:
* **Backend C++ IPEX-LLM:** Inferencia optimizada para cuantización de modelos en hardware Intel.
* **Soporte Level Zero / XPU:** Controladores nativos para comunicación directa con la GPU (`/dev/dri`).
* **Servidor Ollama Integrado:** Compilado y parcheado para aprovechar las unidades de cómputo XVE de Intel.

---

## ⚙️ Hardware y Stack Técnico

| Componente | Especificación |
| :--- | :--- |
| **Procesador** | Intel Core Ultra 7 265KF |
| **Tarjeta Gráfica (dGPU)** | Intel Arc B580 (Level Zero / XPU) |
| **Memoria RAM** | 64 GB |
| **Sistema Operativo** | Fedora Linux 43 |
| **Contenedores** | Podman |
| **Modelo Multimodal** | `llama3.2-vision:11b` |
| **Interfaz Web** | Streamlit (Python) |

---

## 📁 Estructura del Repositorio

```text
DermaConsulta/
├── app/
│   └── farmacia.py     # Aplicación principal de Streamlit y pipeline de inferencia
├── test_images/        # Muestras de imágenes para pruebas clínicas
├── lanzar_agente.sh    # Script de despliegue automatizado (Podman + GPU + App)
├── requirements.txt    # Librerías de Python requeridas
└── README.md           # Documentación del proyecto

🚀 Guía de Inicio Rápido

1. Clonar e instalar entorno

Bash
git clone [https://github.com/elprofesantucho/DermaConsulta.git](https://github.com/elprofesantucho/DermaConsulta.git)

cd DermaConsulta
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

2. Ejecutar la aplicación

El script se encarga de instanciar el contenedor en Podman con paso directo a la GPU Intel (/dev/dri) y arrancar la interfaz web automáticamente:

Bash
chmod +x lanzar_agente.sh
./lanzar_agente.sh
