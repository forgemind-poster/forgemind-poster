"""
Content niche definitions for ForgeMind Poster.

Each niche has:
- image_prompts: a list of prompt templates for the image generator.
  One is picked at random each run to keep the visual style varied
  within the niche.
- caption_style: instructions given to the caption-writing model.
- hashtags: a pool of relevant hashtags; a random subset is used each post.
"""

import random

NICHES = {
    "ai_art": {
        "label": "AI Art",
        "image_prompts": [
            "A surreal, dreamlike digital painting blending organic and "
            "mechanical forms, glowing neon circuitry patterns woven into "
            "natural shapes like trees or waves, cinematic lighting, highly "
            "detailed, trending digital art style, square composition",
            "An abstract futuristic cityscape at dusk rendered in a painterly "
            "digital art style, bioluminescent structures, reflective wet "
            "streets, dramatic sky, square composition",
            "A close-up portrait of a humanoid figure made of flowing liquid "
            "metal and light particles, dramatic rim lighting, dark "
            "background, hyper-detailed digital art, square composition",
            "A minimalist geometric composition exploring the fusion of "
            "nature and technology, soft gradient color palette, clean "
            "shapes, modern digital art poster style, square composition",
        ],
        "captions": [
            "Some ideas don't have words yet — just shapes, light, and "
            "color. This is one of them.\n\nMore pieces like this → link in bio.",
            "Made entirely by AI, guided by a human eye. Where art and "
            "algorithms meet.\n\nExplore more → link in bio.",
            "Not every piece needs a meaning — sometimes it just needs "
            "to be felt.\n\nSee the full collection → link in bio.",
            "A glimpse into a world that only exists because we asked a "
            "machine to dream.\n\nMore drops daily → link in bio.",
        ],
        "hashtags": [
            "#aiart", "#digitalart", "#generativeart", "#aiartcommunity",
            "#futuristicart", "#conceptart", "#artificialintelligence",
            "#aiartwork", "#surrealart", "#neonart", "#cyberpunkart",
            "#aigenerated",
        ],
    },
    "engineering_quote": {
        "label": "Engineering Motivation",
        "image_prompts": [
            "A bold minimalist motivational poster design with an inspiring "
            "quote about engineering and perseverance, clean sans-serif "
            "typography, blueprint grid background texture, dark navy and "
            "orange color scheme, professional graphic design, square "
            "composition, LEAVE SPACE FOR TEXT OVERLAY at center",
            "A dramatic photo-realistic scene of a lone engineer silhouette "
            "looking at a large mechanical structure or bridge at sunrise, "
            "cinematic wide shot, inspiring mood, square composition",
            "A close-up macro shot of gears, blueprints and technical "
            "drawings arranged aesthetically on a dark desk, dramatic "
            "side lighting, moody professional photography style, square "
            "composition",
        ],
        "captions": [
            "Every system that ever worked started as something that "
            "didn't.\n\nKeep iterating. Tools & resources → link in bio.",
            "The blueprint never survives first contact with reality — "
            "build anyway.\n\nMore for builders → link in bio.",
            "You don't need to see the whole staircase. Just take the "
            "next step.\n\nGear & resources → link in bio.",
            "Engineers don't avoid failure — they just fail faster than "
            "everyone else, on purpose.\n\nJoin the grind → link in bio.",
        ],
        "hashtags": [
            "#engineering", "#engineeringlife", "#engineeringstudent",
            "#mechanicalengineering", "#civilengineering",
            "#electricalengineering", "#stem", "#buildersofinstagram",
            "#motivation", "#engineeringmotivation", "#innovation",
            "#problemsolving",
        ],
    },
    "tech_gadget": {
        "label": "Tech Gadgets",
        "image_prompts": [
            "A sleek product photography style rendering of a futuristic "
            "consumer tech gadget (smart wearable, drone, or AI device) on "
            "a minimalist reflective surface, studio lighting, shallow "
            "depth of field, high-end tech advertisement look, square "
            "composition",
            "A flat-lay arrangement of modern tech gadgets and accessories "
            "on a clean desk setup, top-down view, soft natural light, "
            "aspirational tech lifestyle aesthetic, square composition",
            "A dramatic hero shot of a futuristic gadget floating with "
            "glowing light trails and particle effects, dark background, "
            "premium tech commercial photography style, square composition",
        ],
        "captions": [
            "The future doesn't arrive all at once — it shows up in "
            "pieces like this.\n\nSee what's new → link in bio.",
            "This is what \"someday\" tech looks like when someday is "
            "now.\n\nGrab similar gear → link in bio.",
            "Function meets form. This is what happens when engineers "
            "get creative.\n\nMore finds daily → link in bio.",
            "We're living in the future and most days it doesn't even "
            "look weird anymore.\n\nCheck it out → link in bio.",
        ],
        "hashtags": [
            "#techgadgets", "#technology", "#futuretech", "#gadgetlovers",
            "#innovation", "#techreview", "#smartgadgets", "#techlife",
            "#gadgetaddict", "#techtrends", "#cooltech", "#gearheads",
        ],
    },
}

NICHE_ORDER = ["ai_art", "engineering_quote", "tech_gadget"]


def pick_niche(sequence_index: int) -> str:
    """Rotate through niches in order so content stays varied across posts."""
    return NICHE_ORDER[sequence_index % len(NICHE_ORDER)]


def pick_image_prompt(niche_key: str) -> str:
    return random.choice(NICHES[niche_key]["image_prompts"])


def pick_hashtags(niche_key: str, count: int = 6) -> list:
    pool = NICHES[niche_key]["hashtags"]
    return random.sample(pool, min(count, len(pool)))


def pick_caption(niche_key: str) -> str:
    return random.choice(NICHES[niche_key]["captions"])
