import os, time, requests, glob

GROQ_KEY = os.environ['GROQ_API_KEY']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
API = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(prompt: str):
    resp = requests.post(API, json={
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": 512,
        "service_tier": "auto"
    }, headers={"Authorization": f"Bearer {GROQ_KEY}"})
    if resp.status_code == 429:
        wait = int(resp.headers.get("Retry-After", 5))
        time.sleep(wait)
        return ask_groq(prompt)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def main():
    files = glob.glob("**/*.*", recursive=True)
    chunks = []
    current = ""
    for f in files:
        txt = open(f, errors='ignore').read()
        if len(current) + len(txt) > 10000:
            chunks.append(current)
            current = ""
        current += f"\n\n=== File: {f} ===\n{txt[:5000]}"
    if current: chunks.append(current)

    summary = ""
    for i, chunk in enumerate(chunks):
        summary += f"\n\n--- Chunk {i+1}/{len(chunks)} ---\n"
        summary += ask_groq(
            "Review this code for secrets, security risks, code hygiene, style issues. Suggest fixes.\n" + chunk
        )[:2000]
    print(summary.strip())

if __name__ == "__main__":
    main()
