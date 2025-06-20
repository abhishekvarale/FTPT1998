import os
import requests

def get_error_logs():
    with open("logs/error.log", "r") as file:
        return file.read()[:3000]  # Limit input for the model

def ask_groq(logs):
    api_key = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a DevOps expert. Explain this CI/CD log failure in simple terms, and suggest fixes."},
            {"role": "user", "content": logs}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    logs = get_error_logs()
    explanation = ask_groq(logs)
    print("=== CI Failure Explanation ===\n")
    print(explanation)

if __name__ == "__main__":
    main()
