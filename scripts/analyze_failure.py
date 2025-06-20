import requests
import logging

API_KEY = "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"
MODEL = "llama3-70b-8192"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Dummy error log (replace with real log later)
DUMMY_LOG = """
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.1:compile
Compilation failure:
src/main/java/com/example/Service.java:[10,8] cannot find symbol
  symbol:   class List
  location: class com.example.Service
"""

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior DevOps and security engineer. Reply in clear markdown format."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Groq API request failed: {e}")
        return "Failed to fetch AI response."

def main():
    logging.info("🚀 Starting Groq AI Copilot")

    logging.info("🔍 Getting failure explanation...")
    root_cause = ask_groq(f"Explain this CI build failure and how to fix it:\n{DUMMY_LOG}")

    logging.info("⚙️ Getting code enhancement suggestions...")
    enhancements = ask_groq("Suggest code improvements and best practices for a Java Maven project.")

    logging.info("🔐 Checking for potential security issues...")
    threats = ask_groq("List possible security risks and hardening tips for CI/CD pipelines in Java/Maven projects.")

    result = f"""\
### ❌ Root Cause & Fix
{root_cause.strip()}

---

### ⚙️ Code Enhancements
{enhancements.strip()}

---

### 🔐 Security Threats & Suggestions
{threats.strip()}
"""
    print(result)

if __name__ == "__main__":
    main()
