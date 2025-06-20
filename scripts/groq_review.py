import os
import requests

# Hardcoded Groq API Key (you can replace with environment variable if needed)
GROQ_API_KEY = "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"

def read_all_code(directory="."):
    content = ""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".java", ".html", ".yml", ".ts", ".css", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        data = f.read()
                        content += f"\n\n### File: {path}\n```{file.split('.')[-1]}\n{data}\n```\n"
                except Exception:
                    pass
    return content[:12000]  # Limit to 12k tokens approx.

def ask_groq(code_summary):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a secure DevOps AI reviewing a full repository. Suggest improvements, detect secrets, bad indentation, poor structure, security issues, and dangerous patterns. Use clear, short Markdown feedback."
            },
            {
                "role": "user",
                "content": code_summary
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    all_code = read_all_code()
    suggestion = ask_groq(all_code)
    print("### 🤖 AI Review Suggestions\n")
    print(suggestion)
