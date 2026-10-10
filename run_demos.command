#!/bin/bash
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:/Applications/Ollama.app/Contents/Resources:$PATH"
export PYTHONUNBUFFERED=1 TOKENIZERS_PARALLELISM=false
export TRANSFORMERS_VERBOSITY=error HF_HUB_DISABLE_PROGRESS_BARS=1
source "$HOME/.ecomgpt-venv/bin/activate"
mkdir -p screenshots outputs
printf "\e[8;46;100t"
sleep 1

clear
echo "Checking environment ..."
ollama --version
curl -s -m 5 http://localhost:11434/api/version >/dev/null || {
  echo "Starting Ollama ..."; nohup ollama serve >/dev/null 2>&1 & sleep 8; }
curl -s -m 5 http://localhost:11434/api/version >/dev/null && echo "Ollama running." || {
  echo "ERROR: Ollama unreachable."; exit 1; }
ollama list | grep -q "llama3.2" && echo "llama3.2 installed." || {
  echo "ERROR: llama3.2 missing."; exit 1; }
echo "Warming models ..."
python -c "
import utils, retrieval_module
utils.check_model(); utils.ask('Reply briefly.','hi'); retrieval_module._build()
print('ready')" 2>/dev/null || exit 1
sleep 2

exec > >(tee demos.log) 2>&1
shot () { sleep 2; screencapture -x -o "screenshots/$1"; }
EMAIL='Priya\nDelivery Issue\nI ordered a product last week but my package has not arrived yet and the tracking has not updated.\n8\n'

clear
printf '8\n' | python main.py
shot 01_home.png

clear
printf "1\n$EMAIL" | python main.py 2>/dev/null
shot 02_customer_email.png

clear
python intent_module.py 2>/dev/null
shot 03_intent_detection.png

clear
python retrieval_module.py 2>/dev/null
shot 04_similar_email.png

clear
python reply_module.py 2>/dev/null
shot 05_ai_reply.png

clear
python tone_module.py 2>/dev/null
shot 06_tone_improvement.png

clear
python summary_module.py 2>/dev/null
shot 07_summary.png

clear
printf '7\n8\n' | python main.py 2>/dev/null
shot 08_saved_reply.png

clear
echo "=== verification ==="
ls -l screenshots/
echo
wc -l outputs/generated_reply.txt
head -8 outputs/generated_reply.txt
echo
echo "DEMOS3_FINISHED_OK"
