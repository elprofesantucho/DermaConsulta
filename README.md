Markdown
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

Analiza imágenes dermatológicas y responde consultas clínicas mediante modelos multimodales de visión y lenguaje. Todo corre de forma **100% local, privada y offline** sin enviar datos a APIs externas, aprovechando la aceleración por hardware.

---

## 🐳 Imagen Base de Podman (Infraestructura de IA)

Para evitar la instalación manual de dependencias de cómputo pesado, el proyecto despliega la imagen oficial de Intel Analytics:

> **`docker.io/intelanalytics/ipex-llm-inference-cpp-xpu:latest`**

Esta imagen de contenedor ya incluye preinstalado todo lo necesario para ejecutar inferencia en la tarjeta gráfica:
* **Entorno C++ IPEX-LLM:** Aceleración optimizada para cuantización de modelos en GPUs Intel.
* **Soporte Level Zero / XPU:** Controladores nativos para la comunicación directa con el hardware `/dev/dri`.
* **Binarios de Ollama:** Servidor interno compilado y parcheado específicamente para la arquitectura Intel Arc.

---

## ⚙️ Hardware y Stack Técnico

| Componente | Especificación |
| :--- | :--- |
| **Procesador** | Intel Core Ultra 7 265KF |
| **Tarjeta Gráfica (GPU)** | Intel Arc B580 (Level Zero / XPU) |
| **Memoria RAM** | 64 GB |
| **Sistema Operativo** | Fedora Linux 43 |
| **Contenedores** | Podman |
| **Interfaz Web** | Streamlit (Python) |

---

## 📁 Estructura del Repositorio

```text

DermaConsulta/
├── app/
│   └── farmacia.py     # Aplicación principal de Streamlit
├── test_images/        # Imágenes de muestra para pruebas
├── lanzar_agente.sh    # Script de despliegue automatizado (Podman + GPU + App)
├── requirements.txt    # Librerías de Python requeridas
└── README.md           # Documentación

🚀 Guía de Inicio Rápido

1. Clonar e instalar entorno

Bash
git clone [https://github.com/elprofesantucho/DermaConsulta.git](https://github.com/elprofesantucho/DermaConsulta.git)

cd DermaConsulta
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

2. Ejecutar la aplicación

El script se encarga de descargar e instanciar la imagen de Podman asignándole la GPU Intel (/dev/dri) y arrancar la interfaz web automáticamente:

Bash
chmod +x lanzar_agente.sh
./lanzar_agente.sh
