import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, logging

logging.set_verbosity_error()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NAME = os.getenv("HF_MODEL", "distilgpt2")
LOCAL_MODEL_PATH = os.path.join(BASE_DIR, "llm", "models", MODEL_NAME.split("/")[-1])

os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=LOCAL_MODEL_PATH)

try:
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        cache_dir=LOCAL_MODEL_PATH,
        use_safetensors=True  # prefer safetensors
    )
except Exception as e:
    print(f"[Warning] Failed to load safetensors: {e}")
    print("Falling back to regular .bin weights...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        cache_dir=LOCAL_MODEL_PATH
    )

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def call_huggingface_chat(prompt: str, max_new_tokens: int = 150):

    if not prompt:
        raise ValueError("Prompt is required")

    result = generator(prompt, max_new_tokens=max_new_tokens)
    return result[0]["generated_text"]
