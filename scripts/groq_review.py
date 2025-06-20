import os
import requests

API_KEY = "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"
MODEL = "llama3-70b-8192"

def collect_code():
    collected = []
    for root, _, files in os.walk("."):
        if any(ignored in root for ignored in [".git", "node_modules", "__pycache__"]):
            continue
        for file in files:
            if file.endswith((".js", ".ts", ".py", ".java", ".go", ".yml", ".yaml", ".sh", ".env", ".html", ".css", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().strip()
                        if content:
                            collected.append(f"# {path}\n{content[:1000]}")
                except:
                    continue
    return "\n\n".join(collected)[:15000]

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert DevSecOps and code quality reviewer."},
            {"role": "user", "content": prompt}
        ]
    }
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    code = collect_code()
    prompt = f"""
Review the following codebase for:
- 🔐 security issues
- ❌ secrets exposed
- 💩 bad indentation or formatting
- ⚠️ dangerous configs or open .env values
- 💡 code improvement suggestions

Keep the response clear. Start your response with a header: `🧠 AI Code Review Summary`

Code:
{code}
"""
    result = ask_groq(prompt)
    print(result)
