#!/usr/bin/env python3
"""
Automated GitHub Repository Creator and Code Pusher for AcadAssist.
Target GitHub account: sehajpalsanchi12-source
"""
import os
import sys
import getpass
import subprocess
import urllib.request
import urllib.error
import json

TARGET_USERNAME = "sehajpalsanchi12-source"
REPO_NAME = "AcadAssist"
REPO_DESCRIPTION = "Official AcadAssist Platform for Lovely Professional University with 267 subjects, PYQ bank, PPT generator, and paywall"

def get_token() -> str:
    # 1. From environment
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token

    # 2. From ~/.env
    home_env = os.path.expanduser("~/.env")
    if os.path.exists(home_env):
        try:
            with open(home_env, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
        except Exception:
            pass

    # 3. Prompt user safely with hidden typing
    print("\n" + "=" * 60)
    print("  🔑 GitHub Authentication Required")
    print(f"  Target account: https://github.com/{TARGET_USERNAME}")
    print("=" * 60)
    print("If you don't have a token yet, generate one in 2 clicks:")
    print("👉 https://github.com/settings/tokens/new?scopes=repo&description=AcadAssist")
    print("-" * 60)
    try:
        token = getpass.getpass("Paste GitHub Token (typing will be hidden): ").strip()
    except Exception:
        token = sys.stdin.readline().strip()

    return token

def make_request(url: str, token: str, data: dict = None, method: str = "GET") -> tuple:
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AcadAssist-Pusher/1.0"
    }
    payload = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            res_body = res.read().decode("utf-8")
            return res.status, json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}
        return e.code, parsed

def main():
    print("=" * 60)
    print(f"  🚀 AcadAssist — Automated GitHub Repository Setup & Push")
    print(f"  Target: https://github.com/{TARGET_USERNAME}/{REPO_NAME}")
    print("=" * 60)

    token = get_token()
    if not token:
        print("❌ Error: No GitHub token provided. Aborting.")
        sys.exit(1)

    # 1. Verify user identity
    print("\n[1/4] Verifying GitHub token...")
    status, user_data = make_request("https://api.github.com/user", token)
    if status != 200:
        print(f"❌ Error authenticating with GitHub (HTTP {status}): {user_data.get('message', 'Invalid token')}")
        sys.exit(1)

    user_login = user_data.get("login", "")
    print(f"   ✓ Authenticated as: @{user_login} ({user_data.get('name', '')})")

    # 2. Check if repository exists or create it
    print(f"\n[2/4] Checking repository '{REPO_NAME}' on GitHub...")
    status, repo_data = make_request(f"https://api.github.com/repos/{user_login}/{REPO_NAME}", token)

    if status == 200:
        print(f"   ✓ Repository '{REPO_NAME}' already exists on GitHub.")
    elif status == 404:
        print(f"   Creating new repository '{REPO_NAME}' under @{user_login}...")
        create_payload = {
            "name": REPO_NAME,
            "description": REPO_DESCRIPTION,
            "private": False,
            "auto_init": False
        }
        create_status, create_res = make_request("https://api.github.com/user/repos", token, data=create_payload, method="POST")
        if create_status in [200, 201]:
            print(f"   ✓ Repository created successfully: {create_res.get('html_url')}")
        else:
            print(f"❌ Failed to create repository (HTTP {create_status}): {create_res.get('message')}")
            sys.exit(1)
    else:
        print(f"❌ Unexpected status {status}: {repo_data}")
        sys.exit(1)

    # 3. Configure git remote with authentication for the push
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"\n[3/4] Preparing Git remote at {project_root}...")
    auth_remote = f"https://{user_login}:{token}@github.com/{user_login}/{REPO_NAME}.git"
    clean_remote = f"https://github.com/{user_login}/{REPO_NAME}.git"

    subprocess.run(["git", "remote", "remove", "origin"], cwd=project_root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", auth_remote], cwd=project_root, check=True)

    # 4. Push main branch
    print(f"\n[4/4] Pushing code, curriculum, and PPT slide decks to GitHub...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_root)

    # Clean up token from git remote config for safety
    subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=project_root, check=True)

    if push_res.returncode == 0:
        print("\n" + "=" * 60)
        print("  🎉 SUCCESS! Your website has been pushed to GitHub!")
        print(f"  👉 Repository: https://github.com/{user_login}/{REPO_NAME}")
        print("=" * 60)
        print("\nNext step: Host it for free on Render.com in 1 click:")
        print("1. Go to https://dashboard.render.com -> New Web Service")
        print(f"2. Select {user_login}/{REPO_NAME}")
        print("3. Build: pip install -r requirements.txt")
        print("4. Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT")
        print("=" * 60 + "\n")
    else:
        print(f"\n❌ Git push failed with exit code {push_res.returncode}.")
        sys.exit(1)

if __name__ == "__main__":
    main()
