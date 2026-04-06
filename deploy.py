#!/usr/bin/env python3
"""
Nurse Visit Sheet — Deploy Script
Usage: python3 deploy.py /path/to/new-version.zip

Pushes updated files to GitHub via API.
Netlify auto-deploys on every commit (~30 seconds to live).

Setup (one time):
  1. Create a GitHub personal access token at:
     https://github.com/settings/tokens → Generate new token (classic)
     Scopes needed: repo (full)
  2. Set GITHUB_TOKEN and GITHUB_REPO below
"""

import sys
import os
import zipfile
import base64
import json
import urllib.request
import urllib.error

# ── CONFIG — edit these ───────────────────────────────────────────────────────
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
GITHUB_REPO  = "YOUR_USERNAME/nurse-visit-sheet"   # e.g. "jsmith/nurse-visit-sheet"
BRANCH       = "main"
# ─────────────────────────────────────────────────────────────────────────────

API = "https://api.github.com"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "User-Agent": "nurse-visit-deploy",
}

def gh(method, path, body=None):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  GitHub API error {e.code}: {e.read().decode()}")
        return None

def get_sha(filepath):
    result = gh("GET", f"/repos/{GITHUB_REPO}/contents/{filepath}?ref={BRANCH}")
    return result.get("sha") if result and "sha" in result else None

def push_file(filepath, content_bytes, message):
    encoded = base64.b64encode(content_bytes).decode()
    sha = get_sha(filepath)
    body = {
        "message": message,
        "content": encoded,
        "branch": BRANCH,
    }
    if sha:
        body["sha"] = sha
    result = gh("PUT", f"/repos/{GITHUB_REPO}/contents/{filepath}", body)
    if result:
        action = "Updated" if sha else "Created"
        print(f"  ✓ {action}: {filepath}")
    else:
        print(f"  ✗ Failed: {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 deploy.py /path/to/new-version.zip")
        sys.exit(1)

    zip_path = sys.argv[1]
    if not os.path.exists(zip_path):
        print(f"Error: file not found: {zip_path}")
        sys.exit(1)

    if GITHUB_TOKEN == "YOUR_GITHUB_TOKEN":
        print("Error: set GITHUB_TOKEN and GITHUB_REPO in this script first.")
        sys.exit(1)

    print(f"\n🚀 Deploying Nurse Visit Sheet")
    print(f"   Repo:   {GITHUB_REPO}")
    print(f"   Branch: {BRANCH}")
    print(f"   Zip:    {zip_path}\n")

    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
        # Strip leading folder name if present (e.g. "nvs-deploy/index.html" → "index.html")
        prefix = names[0] if names[0].endswith('/') else ''

        for name in names:
            if name.endswith('/'):
                continue  # skip directories
            filepath = name[len(prefix):] if prefix and name.startswith(prefix) else name
            if not filepath:
                continue
            content = zf.read(name)
            push_file(filepath, content, f"Deploy: update {filepath}")

    print(f"\n✅ Done! Netlify will auto-deploy in ~30 seconds.")
    print(f"   Check: https://app.netlify.com\n")

if __name__ == "__main__":
    main()
