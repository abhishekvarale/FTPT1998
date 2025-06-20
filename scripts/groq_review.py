import os
import requests

# Walk through repo and gather code content
def gather_code(base_path='.'):
    collected = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.yml', '.yaml', '.ts', '.go', '.html', '.css')):
                path = os.path.join(root, file)
                if path.startswith("./.git") or "node_modules" in path or path.startswith("./.github"):
                    continue
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    collected.append(f"\n### File: {path}\n```\n{content}\n```")
    return "\n".join(collected)[:12000]  # Keep input within safe token limit

def ask_groq(code_snippets):
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "You're a code reviewer and security expert. Review the following code for security risks, hardcoded secrets, bad practices, and suggest improvements with explanations."},
        {"role": "user", "content": code_snippets}
    ]

    payload = {
        "model": "llama3-8b-8192",
        "messages": messages
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

if __name__ == "__main__":
    print("🔍 Collecting repo code for Groq analysis...")
    snippet = gather_code()
    print("🧠 Asking Groq for code review...")
    result = ask_groq(snippet)
    print(result)
