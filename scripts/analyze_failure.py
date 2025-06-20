import requests
import logging

# === Config ===
API_KEY = "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"
MODEL_NAME = "llama3-70b-8192"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# === Dummy Log to Send ===
DUMMY_LOG = """
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.1:compile
Compilation failure:
src/main/java/com/example/Service.java:[10,8] cannot find symbol
  symbol:   class List
  location: class com.example.Service
"""

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ask_groq(logs):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a DevOps expert. Explain the CI failure log below, suggest fixes, and tell if retry is safe."},
            {"role": "user", "content": logs}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        logging.info("📤 Sending request to Groq API...")
        response = requests.post(API_URL, headers=headers, json=body)
        response.raise_for_status()
        logging.info("✅ Groq API returned a response.")
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Groq API request failed: {e}")
        if e.response is not None:
            logging.error(f"Response Content: {e.response.text}")
        return "Failed to fetch explanation from AI."

def main():
    logging.info("🚀 CI Helper Script Started...")
    explanation = ask_groq(DUMMY_LOG)
    print("\n🧠 === CI/CD Failure Explanation ===\n")
    print(explanation)

if __name__ == "__main__":
    main()
