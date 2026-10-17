#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import re
import shutil
from pathlib import Path

HOME = Path.home()
CACHE_DIR = HOME / ".cache/omalauncher-photos"
THUMB_DIR = CACHE_DIR / "thumbs"
PICTURES_DIR = HOME / "Pictures"
SAMPLE_DIR = PICTURES_DIR / "Sample"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)
PICTURES_DIR.mkdir(parents=True, exist_ok=True)

EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def seed_sample_photos():
    """Seed sample photos from Omarchy themes if Pictures is empty."""
    if any(PICTURES_DIR.rglob("*." + ext.lstrip(".")) for ext in EXTS):
        return
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    themes_dir = HOME / ".local/share/omarchy/themes"
    if not themes_dir.exists():
        return
    candidates = list(themes_dir.glob("*/backgrounds/*"))
    for p in candidates:
        if p.is_file() and p.suffix.lower() in EXTS and not p.name.startswith("omarchy"):
            dest = SAMPLE_DIR / p.name
            if not dest.exists():
                try:
                    shutil.copy2(p, dest)
                except Exception:
                    pass
            if len(list(SAMPLE_DIR.iterdir())) >= 8:
                break

def clean_title(filename):
    stem = Path(filename).stem
    stem = re.sub(r"^[0-9]+[-_ ]*", "", stem)
    stem = re.sub(r"[-_]+", " ", stem)
    return stem.title()

def fmt_size(num_bytes):
    if num_bytes >= 1024 * 1024:
        return f"{num_bytes / (1024 * 1024):.1f} MB"
    return f"{num_bytes / 1024:.0f} KB"

def main():
    seed_sample_photos()

    # Search paths
    search_dirs = [
        PICTURES_DIR,
        HOME / "photos",
        Path("/sdcard/DCIM/Camera"),
        Path("/sdcard/Pictures"),
    ]

    images = []
    seen = set()
    for root in search_dirs:
        if root.exists():
            try:
                for p in root.rglob("*"):
                    if p.is_file() and p.suffix.lower() in EXTS and not p.name.startswith("."):
                        resolved = p.resolve()
                        if resolved not in seen:
                            seen.add(resolved)
                            images.append(p)
            except Exception:
                pass

    images.sort(key=lambda p: p.name.lower())

    # Try importing Pillow
    try:
        from PIL import Image
        has_pil = True
    except ImportError:
        has_pil = False

    items = []
    for i, p in enumerate(images):
        try:
            st = p.stat()
        except OSError:
            continue

        h = hashlib.md5(f"{p}:{st.st_mtime}:{st.st_size}".encode()).hexdigest()[:12]
        thumb_path = THUMB_DIR / f"{h}.jpg"
        w, h_dim = 0, 0

        if has_pil:
            if not thumb_path.exists():
                try:
                    with Image.open(p) as im:
                        w, h_dim = im.size
                        rgb = im.convert("RGB")
                        rgb.thumbnail((400, 400), Image.Resampling.BILINEAR)
                        rgb.save(thumb_path, "JPEG", quality=82)
                except Exception:
                    pass
            else:
                # Dim can be fetched or skipped
                pass

            if w == 0:
                try:
                    with Image.open(p) as im:
                        w, h_dim = im.size
                except Exception:
                    w, h_dim = 0, 0

        thumb_str = str(thumb_path) if thumb_path.exists() else str(p)

        folder_name = p.parent.name
        if p.parent == PICTURES_DIR:
            folder_name = "Pictures"

        items.append({
            "id": i,
            "name": clean_title(p.name),
            "file": p.name,
            "path": str(p),
            "thumb": thumb_str,
            "dim": f"{w}×{h_dim}" if w else "",
            "size": fmt_size(st.st_size),
            "folder": folder_name
        })

    out = {
        "count": len(items),
        "items": items
    }
    sys.stdout.write(json.dumps(out, separators=(",", ":")))

if __name__ == "__main__":
    main()
