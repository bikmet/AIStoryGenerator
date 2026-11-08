# backend/test_cf.py
import requests
from core.config import settings

acc = str(settings.CLOUDFLARE_ACCOUNT_ID).strip().strip('"').strip("'")
tok = str(settings.CLOUDFLARE_API_TOKEN).strip().strip('"').strip("'")

# Use one of the model names returned by Step 1, e.g. @cf/meta/llama-3-8b-instruct
model_name = "@cf/qwen/qwq-32b"

url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {tok}",
    "Content-Type": "application/json"
}
payload = {
    "model": model_name,
    "messages": [{"role": "user", "content": "Respond with: Ready"}],
    "max_tokens": 50
}

res = requests.post(url, headers=headers, json=payload, timeout=20)
print("Status:", res.status_code)
print("Response:", res.text)