# AI Agent Fine-tuning - Deployment Guide

**Project:** AI Agents Fine-tuning Prototype  
**Datum:** 5 maart 2025  
**Door:** Supreme Flux

---

## 📁 Bestanden

| Bestand | Beschrijving |
|---------|--------------|
| `train_agent.py` | Hoofd training script |
| `training_data.json` | 200 training voorbeelden |
| `setup_cloud.sh` | Cloud GPU setup script |
| `generate_training_data.py` | Data generator (optioneel) |

---

## 🚀 Quick Start - Cloud GPU

### Optie 1: RunPod (Aanbevolen)

1. **Ga naar** [runpod.io](https://runpod.io)

2. **Kies een pod:**
   - GPU: RTX 4090 of A100
   - Image: PyTorch 2.0+ (CUDA 12.1)
   - Minimaal: 24GB VRAM

3. **Deploy en connect:**
   ```bash
   # Upload files
   scp -r * root@<pod-ip>:/workspace/
   
   # SSH naar pod
   ssh root@<pod-ip>
   ```

4. **Start training:**
   ```bash
   cd /workspace
   bash setup_cloud.sh
   python3 train_agent.py
   ```

### Optie 2: Vast.ai

1. **Ga naar** [vast.ai](https://vast.ai)

2. **Filter:**
   - GPU: RTX 4090 / A100 / A40
   - CUDA: 12.0+
   - Max $1/uur

3. **Create instance** en volg zelfde stappen als RunPod

### Optie 3: Lambda Labs

1. **Ga naar** [lambdalabs.com](https://lambdalabs.com)

2. **Kies:** 1x A100 80GB (~$1.99/uur)

3. **SSH en run:**
   ```bash
   ssh ubuntu@<instance-ip>
   # Upload files en run setup
   ```

---

## 💰 Kosten Schatting

| Provider | GPU | Prijs/uur | Totale kosten (2 uur) |
|----------|-----|-----------|----------------------|
| RunPod | RTX 4090 | $0.69 | **$1.38** |
| RunPod | A100 40GB | $1.69 | **$3.38** |
| Vast.ai | RTX 4090 | $0.50-0.80 | **$1.00-1.60** |
| Lambda | A100 80GB | $1.99 | **$3.98** |

**Aanbeveling:** Start met RunPod RTX 4090 (~$1.40 totaal)

---

## ⚙️ Training Configuratie

Huidige instellingen in `train_agent.py`:

```python
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
LORA_R = 16
EPOCHS = 3
LEARNING_RATE = 2e-4
BATCH_SIZE = 1
```

**Verwachte trainingstijd:** 1-2 uur op RTX 4090

---

## 📊 Monitoring

Tijdens training zie je output zoals:

```
Step 100/600: loss=1.234
Step 200/600: loss=0.987
...
```

Loss moet dalen van ~3.0 naar ~0.5-1.0

---

## ✅ Na Training

Model wordt opgeslagen in:
```
./llama31_agent_model/final_adapter/
```

Bestanden:
- `adapter_config.json` - LoRA configuratie
- `adapter_model.safetensors` - Gewichten (~100MB)
- `tokenizer*.json` - Tokenizer files

---

## 🧪 Testen

```python
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer

model = AutoPeftModelForCausalLM.from_pretrained(
    "./llama31_agent_model/final_adapter"
)
tokenizer = AutoTokenizer.from_pretrained(
    "./llama31_agent_model/final_adapter"
)

# Test prompt
prompt = "<|user|>\nWat is 25 keer 4?\n<|assistant|>"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

---

## 🔧 Troubleshooting

### Out of Memory
- Verlaag `MAX_SEQ_LENGTH` naar 512
- Verlaag `BATCH_SIZE` naar 1 (al default)
- Gebruik A100 met 80GB

### Model niet gevonden
- Zorg dat je HuggingFace token hebt voor Llama 3.1
- Of gebruik `unsloth/Llama-3.1-8B` (geen token nodig)

### Training traag
- Gebruik A100 ipv RTX 4090
- Verhoog `BATCH_SIZE` als VRAM beschikbaar

---

## 📞 Support

Bij vragen: contact Supreme Flux
