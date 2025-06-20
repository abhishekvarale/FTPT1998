import os
import requests
import logging

API_KEY = "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"
MODEL = "llama3-70b-8192"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ALLOWED_EXT = (".js", ".ts", ".py", ".java", ".yml", ".yaml", ".env", ".json", ".sh")

def collect_repo_content():
    contents = []
    for root, _, files in os.walk("."):
        if ".git" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith(ALLOWED_EXT):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        data = f.read()
                        if len(data.strip()) > 0:
                            contents.append(f"# File: {os.path.join(root, file)}\n{data[:2000]}")
                except Exception as e:
                    logging.warning(f"Could not read {file}: {e}")
    return "\n\n".join(contents)[:15000]  # keep within token limit

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a cybersecurity and code quality expert. Reply in clear markdown."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Groq API failed: {e}")
        return "Failed to fetch AI response."

def main():
    logging.info("🔍 Collecting repo files...")
    repo_data = collect_repo_content()

    logging.info("🤖 Sending repo content to Groq...")
    prompt = f"""
Analyze the following codebase and configuration files for:
1. Secret leaks (keys, tokens, passwords)
2. Misconfigurations or hardcoded credentials
3. General security risks or poor patterns
4. Suggestions to improve code quality or structure

Respond in markdown format with:
- 🔐 Detected Secrets
- ⚠️ Security Issues
- 💡 Code Enhancements
- ✅ Suggested Fixes
---

{repo_data}
    """
    result = ask_groq(prompt)
    print(result)

if __name__ == "__main__":
    main()
