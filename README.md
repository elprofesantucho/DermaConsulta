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

Analiza imágenes de afecciones en la piel y responde consultas dermatológicas mediante modelos multimodales (LLM + Visión), ejecutando inferencias de forma local, privada y acelerada por GPU sin depender de APIs de terceros.

---

## ⚙️ Hardware y Tecnologías

| Componente | Especificación |
| :--- | :--- |
| **CPU** | Intel Core Ultra 7 265KF |
| **GPU (dGPU)** | Intel Arc B580 (Level Zero / XPU) |
| **RAM** | 64 GB |
| **S.O. / Contenedores** | Fedora Linux 43 + Podman |
| **Motor de IA** | IPEX-LLM (`ipex-llm-inference-cpp-xpu`) + Ollama |
| **Interfaz Web** | Python + Streamlit |

---

## 📁 Estructura del Repositorio

```text
DermaConsulta/
├── app/
│   └── farmacia.py     # Interfaz web interactiva (Streamlit)
├── test_images/        # Muestras para pruebas de inferencia visual
├── lanzar_agente.sh    # Script de despliegue (Podman + GPU + App)
├── requirements.txt    # Dependencias de Python
└── README.md
