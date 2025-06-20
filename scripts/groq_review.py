import os
import requests
import glob
import time

# === Hardcoded tokens (⚠️ Not safe for production)
GITHUB_TOKEN = "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"
GROQ_API_KEY = "your_groq_api_key_here"  # Replace with actual key

# === Collect all source files (skip node_modules/.git)
files = glob.glob("**/*.*", recursive=True)
all_code = ""

for f in files:
    if not os.path.isfile(f):
        continue
    if "node_modules" in f or ".git" in f:
        continue
    try:
        content = open(f, errors='ignore').read()
        all_code += f"\n\n# File: {f}\n{content}"
        if len(all_code) > 60000:
            break  # Groq limit safe cap
    except:
        continue

# === Split into safe chunks
chunks = [all_code[i:i+12000] for i in range(0, len(all_code), 12000)]
responses = []

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a code security and quality reviewer. Highlight secrets, issues, and give clear suggestions."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(url, json=body, headers=headers)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

for chunk in chunks:
    try:
        response = ask_groq(chunk)
        responses.append(response)
        time.sleep(3)
    except Exception as e:
        responses.append(f"[Groq Error] {str(e)}")
        break

final_review = "\n\n".join(responses)

# Write to markdown file
with open("ai_review.md", "w") as f:
    f.write(final_review)

# === Determine Commit or PR URL
import subprocess
sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
repo = os.environ.get("GITHUB_REPOSITORY", "abhishekvarale/FTPT1998")
pr_api = f"https://api.github.com/repos/{repo}/commits/{sha}/pulls"

# Get PR URL (if exists)
pr_info = requests.get(pr_api, headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"})
pr_url = ""
if pr_info.ok and pr_info.json():
    pr_url = pr_info.json()[0]["issue_url"]

comment_body = {"body": final_review}

# === Comment
if pr_url:
    print("💬 Commenting on PR...")
    requests.post(f"{pr_url}/comments", headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=comment_body)
else:
    print("💬 Commenting on commit...")
    commit_url = f"https://api.github.com/repos/{repo}/commits/{sha}/comments"
    requests.post(commit_url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=comment_body)
