# ForgeMind Poster

Fully automated Instagram poster for `@neiljverse`, running on a schedule via
GitHub Actions. Generates an AI image + caption, posts it to Instagram
automatically — no manual work once it's set up.

**Niches (rotate in order):** AI art → engineering motivation → tech gadgets.

**Cost: $0.** Image + caption generation runs on [Pollinations.ai](https://pollinations.ai)
(free, no signup, no API key). Hosting runs on GitHub Actions' free tier
(2,000 minutes/month, this uses a few minutes/day).

## How it works

1. A GitHub Actions workflow runs on a schedule (3x/day by default).
2. `scripts/generate_content.py` picks the next niche in rotation, generates
   an image and caption, saves them to `media/`.
3. The workflow commits the new image to the repo and pushes it — this makes
   it publicly reachable at a `raw.githubusercontent.com` URL, which
   Instagram's API requires (it fetches images by URL, not by upload).
4. `scripts/post_to_instagram.py` calls the Instagram Graph API to publish
   the post using that URL.

## One-time setup

### 1. Create a GitHub repository

The repo **must be public** — Instagram needs to fetch the image URL without
authentication, and `raw.githubusercontent.com` on a private repo requires a
token.

### 2. Push this code

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

### 3. Add repository secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**
and add:

| Secret name | Value |
|---|---|
| `IG_ACCESS_TOKEN` | Your Instagram long-lived access token |
| `IG_USER_ID` | `38049165204696767` |

(Values are already saved locally in `secrets/.env.local` — never commit
that file.)

### 4. Test it

Go to the **Actions** tab → **Auto-post to Instagram** → **Run workflow**
to trigger a manual test run instead of waiting for the schedule.

## Schedule

Default: 09:00, 14:00, 20:00 UTC daily. Edit the `cron` lines in
`.github/workflows/auto-post.yml` to change times or frequency.
[crontab.guru](https://crontab.guru) helps if you want to tweak the syntax.

## Maintenance: token refresh (important)

Instagram access tokens expire after ~60 days. Refresh before then:

```bash
IG_ACCESS_TOKEN=<current token> python scripts/refresh_token.py
```

Copy the new token into:
1. `secrets/.env.local` (local copy)
2. The `IG_ACCESS_TOKEN` GitHub repo secret (Settings → Secrets and
   variables → Actions)

Current token expires ~2026-10-14 (see `secrets/.env.local` for the note).

## Monetization

The automation itself just posts content — actually earning money needs a
couple of one-time manual steps on your end:

- **Affiliate links:** Instagram captions can't contain clickable links.
  Put your affiliate link (or a Linktree-style page with multiple links) in
  the **bio** of `neiljverse`, and captions already say "link in bio".
- **Instagram monetization (Reels bonuses etc.):** available through the
  **Professional dashboard → Monetization** as your account grows. No
  extra setup needed here — this is separate from the API.

## Customizing content

Edit `config/niches.py`:
- `image_prompts`: templates fed to the image generator per niche
- `captions`: pre-written caption variants per niche (randomly picked)
- `hashtags`: hashtag pool per niche (a random subset is used each post)

## Local testing

```bash
pip install -r requirements.txt
python scripts/generate_content.py
```

This generates an image + manifest in `media/` without posting anything —
safe to run repeatedly while testing.
