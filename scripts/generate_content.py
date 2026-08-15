"""
Generates one image + caption for the next post in the niche rotation,
using Pollinations.ai - a free image/text generation API that needs no
signup, no API key, and no billing of any kind.

Output:
  media/<timestamp>.png       - the generated image
  media/<timestamp>.json      - manifest: {niche, caption, image_path}

Reads/updates:
  state/next_index.txt        - which niche comes next (rotation counter)

No API keys required.
"""

import json
import os
import random
import sys
import time
import urllib.parse

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.niches import pick_niche, pick_image_prompt, pick_hashtags, pick_caption

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "..", "media")
STATE_DIR = os.path.join(os.path.dirname(__file__), "..", "state")
STATE_FILE = os.path.join(STATE_DIR, "next_index.txt")

IMAGE_BASE_URL = "https://image.pollinations.ai/prompt"


def read_next_index() -> int:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)
    return 0


def write_next_index(index: int) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(index))


def generate_image(prompt: str, out_path: str, retries: int = 3) -> None:
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999)
    url = (
        f"{IMAGE_BASE_URL}/{encoded_prompt}"
        f"?width=1024&height=1024&nologo=true&seed={seed}"
    )
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            if "image" not in content_type:
                raise ValueError(f"Unexpected content-type: {content_type}")
            with open(out_path, "wb") as f:
                f.write(resp.content)
            return
        except Exception as e:  # noqa: BLE001 - retry on any transient failure
            last_error = e
            print(f"Image generation attempt {attempt} failed: {e}")
            time.sleep(5)
    raise SystemExit(f"Image generation failed after {retries} attempts: {last_error}")


def main():
    index = read_next_index()
    niche_key = pick_niche(index)
    image_prompt = pick_image_prompt(niche_key)

    print(f"[{index}] niche={niche_key}")
    print(f"Image prompt: {image_prompt}")

    os.makedirs(MEDIA_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_filename = f"{timestamp}.png"
    image_path = os.path.join(MEDIA_DIR, image_filename)

    generate_image(image_prompt, image_path)
    print(f"Saved image to {image_path}")

    caption_body = pick_caption(niche_key)
    hashtags = " ".join(pick_hashtags(niche_key))
    full_caption = f"{caption_body}\n\n{hashtags}"

    manifest = {
        "niche": niche_key,
        "caption": full_caption,
        "image_filename": image_filename,
        "created_at": timestamp,
    }
    manifest_path = os.path.join(MEDIA_DIR, f"{timestamp}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Saved manifest to {manifest_path}")

    write_next_index(index + 1)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"manifest_path=media/{timestamp}.json\n")
            f.write(f"image_filename={image_filename}\n")


if __name__ == "__main__":
    main()
