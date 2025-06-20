import os
import requests
import time

GROQ_API_KEY = "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"
MODEL = "llama3-70b-8192"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def read_repo_files(limit=8000):
    chunks = []
    current = ""
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".py", ".java", ".html", ".yml", ".css", ".ts", ".json")):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        code_block = f"\n\n### File: {root}/{file}\n```{file.split('.')[-1]}\n{content}\n```"
                        if len(current) + len(code_block) > limit:
                            chunks.append(current)
                            current = code_block
                        else:
                            current += code_block
                except Exception:
                    continue
    if current:
        chunks.append(current)
    return chunks

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert DevSecOps AI. Review this repo code. Identify secrets, bad code, vulnerabilities, and suggest fixes clearly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    for _ in range(3):
        res = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if res.status_code == 429:
            print("⚠️ Rate limit hit. Retrying after 5s...")
            time.sleep(5)
        else:
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
    raise Exception("Failed after retries due to rate limits.")

if __name__ == "__main__":
    chunks = read_repo_files()
    full_output = "# 🤖 Groq AI Review\n"
    for idx, chunk in enumerate(chunks):
        print(f"🔍 Reviewing chunk {idx + 1}/{len(chunks)}...")
        response = ask_groq(chunk)
        full_output += f"\n\n### 🔎 Review Chunk {idx + 1}\n{response}"

    with open("ai_review.md", "w", encoding="utf-8") as f:
        f.write(full_output)
