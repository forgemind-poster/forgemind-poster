"""
Instagram long-lived access tokens expire after ~60 days and must be
refreshed before then (refreshing also resets the 60-day clock).

Run this locally every ~45-50 days:
  IG_ACCESS_TOKEN=<current token> python scripts/refresh_token.py

It prints the new token - copy it into the IG_ACCESS_TOKEN secret in your
GitHub repo settings (Settings > Secrets and variables > Actions).
"""

import os

import requests


def main():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Set IG_ACCESS_TOKEN to your current token first")

    resp = requests.get(
        "https://graph.instagram.com/refresh_access_token",
        params={"grant_type": "ig_refresh_token", "access_token": token},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    print("New token (valid ~60 days):")
    print(data["access_token"])
    print(f"Expires in {data['expires_in']} seconds (~{data['expires_in'] // 86400} days)")


if __name__ == "__main__":
    main()
