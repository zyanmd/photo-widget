#!/usr/bin/env python3
import sys, os, re
from pathlib import Path

WIDGETS_DIR = Path.home() / ".config/omalauncher/widgets"
TEMPLATE = WIDGETS_DIR / "10-digital-clock.owl"

SAMPLE_DIR = Path.home() / "Pictures/Sample"
SAMPLE_PHOTOS = [
    str(SAMPLE_DIR / "3-sunset-lake.webp"),
    str(SAMPLE_DIR / "1-city-view.webp"),
    str(SAMPLE_DIR / "1-tree-tops.webp"),
    str(SAMPLE_DIR / "1-the-backwater.jpg"),
    str(SAMPLE_DIR / "2-meadow.webp"),
    str(SAMPLE_DIR / "5-zen-boat.webp"),
    str(SAMPLE_DIR / "1-cosmic.webp")
]

def get_duplicates():
    res = []
    for f in sorted(WIDGETS_DIR.glob("*-photo*.owl")):
        if f.name != "10-digital-clock.owl":
            res.append(f)
    return res

def get_next_index():
    nums = [10]
    for f in WIDGETS_DIR.glob("*.owl"):
        m = re.match(r"^(\d+)-", f.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1

def add_duplicates(count):
    if not TEMPLATE.exists():
        return
    template_content = TEMPLATE.read_text(encoding="utf-8")

    created = []
    for k in range(count):
        idx = get_next_index()
        dest = WIDGETS_DIR / f"{idx}-photo.owl"
        new_content = re.sub(r'widget\s+"[^"]+"', f'widget "photo-{idx}"', template_content, count=1)
        new_content = re.sub(r'order:\s*\d+', f'order: {idx}', new_content, count=1)
        sample = SAMPLE_PHOTOS[(idx - 11) % len(SAMPLE_PHOTOS)]
        new_content = re.sub(r'state activePhoto = "[^"]+"', f'state activePhoto = "{sample}"', new_content, count=1)
        
        dest.write_text(new_content, encoding="utf-8")
        created.append(dest.name)
    print(f"Created {len(created)} widgets: {created}")

def remove_duplicates():
    dups = get_duplicates()
    for f in dups:
        f.unlink(missing_ok=True)
        for d in [".check", ".errors", ".preview"]:
            (WIDGETS_DIR / d / f"{f.name}.txt").unlink(missing_ok=True)
            (WIDGETS_DIR / d / f"{f.name}.png").unlink(missing_ok=True)
            (WIDGETS_DIR / d / f"{f.name}.screen.png").unlink(missing_ok=True)
    print(f"Removed {len(dups)} duplicates")

def count_duplicates():
    print(len(get_duplicates()))

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "add"
    if action == "add":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        add_duplicates(count)
    elif action == "remove":
        remove_duplicates()
    elif action == "count":
        count_duplicates()
