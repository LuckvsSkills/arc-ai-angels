#!/bin/bash
set -a
source /home/prime/.openclaw/.env
set +a
cd /home/prime/arc_ai_angels/LITELLM
nohup /home/prime/litellm-env/bin/litellm --config config.yaml --port 4000 > /tmp/litellm.log 2>&1 &
echo "LiteLLM gestart PID: $!"
