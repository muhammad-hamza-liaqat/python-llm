import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = os.getenv("HF_MODEL", "distilgpt2")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Use MPS on Mac if available, else CPU
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
model.to(device)

def call_huggingface_chat(prompt: str, max_length: int = 150) -> str:
    if not prompt:
        raise ValueError("Prompt is required")

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.95,
            top_k=50
        )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text
