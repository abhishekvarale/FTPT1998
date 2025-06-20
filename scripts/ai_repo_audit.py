import os
import requests


API_KEY = "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"
MODEL = "llama3-70b-8192"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def collect_code_files():
    included_exts = (".js", ".ts", ".py", ".java", ".sh", ".env", ".yml", ".yaml", ".json")
    collected = []
    for root, _, files in os.walk("."):
        if any(ignored in root for ignored in [".git", "node_modules", "__pycache__"]):
            continue
        for file in files:
            if file.endswith(included_exts):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().strip()
                        if content:
                            collected.append(f"# File: {filepath}\n{content[:1000]}")
                except Exception:
                    continue
    return "\n\n".join(collected)[:15000]  # keep within token budget

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior DevSecOps engineer and cybersecurity auditor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    files_data = collect_code_files()

    prompt = f"""
You are an expert code security auditor.

Go through the following repository contents and:
- 🔐 Detect any secrets like tokens, passwords, or API keys
- ⚠️ Find insecure configurations (e.g., exposed `.env`, open S3 buckets, missing auth)
- 💡 Suggest meaningful improvements in code quality and security
- ❌ Highlight critical risks
- ✅ Format results in markdown using appropriate emojis

Here is the code snapshot:
{files_data}
    """

    result = ask_groq(prompt)
    print(result)

if __name__ == "__main__":
    main()
