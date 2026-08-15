"""
Publishes a previously generated image+caption to Instagram via the
Instagram Graph API (Instagram Login product - no Facebook Page needed).

Usage:
  python scripts/post_to_instagram.py media/<timestamp>.json

Requires env vars:
  IG_ACCESS_TOKEN     - long-lived Instagram access token
  IG_USER_ID          - Instagram-scoped user id (from graph.instagram.com/me)
  GITHUB_REPOSITORY   - "owner/repo" (auto-set inside GitHub Actions)
  GITHUB_REF_NAME     - branch name (auto-set inside GitHub Actions)

The image must already be pushed to GitHub and publicly reachable at
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<image path>
before this script runs - Instagram fetches the image itself, it is not
uploaded directly.
"""

import json
import os
import sys
import time

import requests

GRAPH_API_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.instagram.com/{GRAPH_API_VERSION}"


def build_raw_url(image_filename: str) -> str:
    repo = os.environ.get("GITHUB_REPOSITORY")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    if not repo:
        raise SystemExit(
            "GITHUB_REPOSITORY env var not set - this script expects to "
            "run inside a GitHub Actions workflow after the image has "
            "been committed and pushed."
        )
    return f"https://raw.githubusercontent.com/{repo}/{branch}/media/{image_filename}"


def create_media_container(ig_user_id: str, token: str, image_url: str, caption: str) -> str:
    resp = requests.post(
        f"{GRAPH_BASE}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": token,
        },
        timeout=60,
    )
    resp.raise_for_status()
    creation_id = resp.json()["id"]
    print(f"Created media container: {creation_id}")
    return creation_id


def wait_until_ready(creation_id: str, token: str, max_wait_seconds: int = 90) -> None:
    """Poll the container status until Instagram has finished fetching the image."""
    deadline = time.time() + max_wait_seconds
    while time.time() < deadline:
        resp = requests.get(
            f"{GRAPH_BASE}/{creation_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=30,
        )
        resp.raise_for_status()
        status = resp.json().get("status_code")
        print(f"Container status: {status}")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise SystemExit(f"Instagram failed to process the media container {creation_id}")
        time.sleep(5)
    raise SystemExit(f"Timed out waiting for media container {creation_id} to finish processing")


def publish_media(ig_user_id: str, token: str, creation_id: str) -> str:
    resp = requests.post(
        f"{GRAPH_BASE}/{ig_user_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": token,
        },
        timeout=60,
    )
    resp.raise_for_status()
    media_id = resp.json()["id"]
    print(f"Published post: {media_id}")
    return media_id


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/post_to_instagram.py <manifest.json>")

    manifest_path = sys.argv[1]
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    token = os.environ.get("IG_ACCESS_TOKEN")
    ig_user_id = os.environ.get("IG_USER_ID")
    if not token or not ig_user_id:
        raise SystemExit("IG_ACCESS_TOKEN and IG_USER_ID env vars must be set")

    image_url = build_raw_url(manifest["image_filename"])
    print(f"Image URL: {image_url}")
    print(f"Niche: {manifest['niche']}")
    print(f"Caption:\n{manifest['caption']}")

    creation_id = create_media_container(ig_user_id, token, image_url, manifest["caption"])
    wait_until_ready(creation_id, token)
    publish_media(ig_user_id, token, creation_id)


if __name__ == "__main__":
    main()
