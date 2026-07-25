#!/bin/bash
DIR_PROYECTO="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR_PROYECTO"

echo "📍 Ubicación del proyecto: $DIR_PROYECTO"

podman rm -f ollama-arc 2>/dev/null

echo "🚀 Arrancando motor Ollama en Intel Arc..."
podman run -d \
  --name ollama-arc \
  --device /dev/dri:/dev/dri \
  --group-add keep-groups \
  --security-opt label=disable \
  -v ~/.ollama:/root/.ollama:Z \
  -v "$DIR_PROYECTO":/app/proyecto:Z \
  -p 11434:11434 \
  -e OLLAMA_HOST=0.0.0.0 \
  -e DEVICE=Arc \
  -e OLLAMA_INTEL_GPU=true \
  -e OLLAMA_NUM_GPU=999 \
  -e ZES_ENABLE_SYSMAN=1 \
  -e ONEAPI_DEVICE_SELECTOR=level_zero:0 \
  docker.io/intelanalytics/ipex-llm-inference-cpp-xpu:latest \
  sh -c 'mkdir -p /llm/ollama && cd /llm/ollama && init-ollama && exec ./ollama serve'

echo "⏳ Esperando 5s a que el servicio inicialice..."
sleep 5

if [ -f "$DIR_PROYECTO/env/bin/activate" ]; then
    source "$DIR_PROYECTO/env/bin/activate"
    python3 -m streamlit run "$DIR_PROYECTO/app/farmacia.py"
else
    echo "⚠️ No se encontró virtualenv en ./env. Ejecutando..."
    python3 -m streamlit run "$DIR_PROYECTO/app/farmacia.py"
fi
