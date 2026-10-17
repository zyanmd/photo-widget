#!/usr/bin/env python3
import sys
import os
import re
import hashlib
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

CACHE_DIR = Path.home() / ".cache/omalauncher-photos"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
STATUS_FILE = CACHE_DIR / "status.txt"

USER_AGENT = "Mozilla/5.0 (Linux; Android 14; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

def set_status(msg: str):
    try:
        STATUS_FILE.write_text(msg, encoding="utf-8")
    except Exception:
        pass

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    
    # Prepend https:// if starts with www. or looks like domain without scheme
    if url.startswith("www."):
        url = "https://" + url
    elif not url.startswith("http://") and not url.startswith("https://") and not url.startswith("/") and not url.startswith("~"):
        if "." in url and not url.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
            url = "https://" + url

    # Google Drive share link -> direct download link
    gdrive_match = re.search(r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)", url)
    if gdrive_match:
        file_id = gdrive_match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    # Dropbox share link dl=0 -> dl=1
    if "dropbox.com" in url and "dl=0" in url:
        url = url.replace("dl=0", "dl=1")

    # Imgur single image page -> direct i.imgur.com link
    imgur_match = re.match(r"^https?://(?:www\.)?imgur\.com/([a-zA-Z0-9]{5,8})$", url)
    if imgur_match:
        return f"https://i.imgur.com/{imgur_match.group(1)}.jpg"

    return url

def extract_image_from_html(html_text: str, base_url: str) -> str:
    # Check for OpenGraph or Twitter card image
    m = re.search(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]+content=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\']', html_text, re.IGNORECASE)
    if m:
        img_url = m.group(1).strip()
        if img_url.startswith("//"):
            return "https:" + img_url
        if img_url.startswith("http://") or img_url.startswith("https://"):
            return img_url
    return ""

def download_file(url: str, dest_path: Path) -> bool:
    cmd = [
        "curl", "-sL", "-k",
        "-A", USER_AGENT,
        "--compressed",
        "--max-time", "20",
        "--retry", "2",
        "-o", str(dest_path),
        url
    ]
    res = subprocess.run(cmd, capture_output=True)
    return res.returncode == 0 and dest_path.exists() and dest_path.stat().st_size > 0

def resolve_photo(raw_val: str, fallback: str = "") -> str:
    raw_val = (raw_val or "").strip()
    fallback = (fallback or "").strip()

    if not raw_val:
        set_status("OK")
        return fallback

    # Check direct local file path
    expanded = Path(os.path.expanduser(raw_val))
    if expanded.is_file() and expanded.stat().st_size > 0:
        set_status("OK")
        return str(expanded.resolve())

    # Handle Android storage paths or plain filenames
    is_storage_path = (
        raw_val.startswith("/storage/") or
        raw_val.startswith("/sdcard/") or
        raw_val.startswith("content://") or
        (not raw_val.startswith("http://") and not raw_val.startswith("https://") and not raw_val.startswith("www.") and "/" not in raw_val and any(raw_val.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]))
    )

    if is_storage_path:
        fname = os.path.basename(raw_val)
        if fname:
            # Search strictly in user media directories (NEVER search ~/.cache or /root)
            search_roots = [
                Path.home() / "Pictures",
                Path.home() / "photos",
                Path.home() / "Downloads",
                Path.home() / ".local/share/omarchy/themes"
            ]
            
            # 1. Exact match in Pictures
            exact = Path.home() / "Pictures" / fname
            if exact.is_file() and exact.stat().st_size > 0:
                set_status("OK")
                return str(exact.resolve())

            # 2. Case-insensitive / recursive search in search roots
            for sdir in search_roots:
                if sdir.is_dir():
                    try:
                        for p in sdir.rglob("*"):
                            if p.is_file() and p.name.lower() == fname.lower() and p.stat().st_size > 0:
                                set_status("OK")
                                return str(p.resolve())
                    except Exception:
                        pass

            # Not found: provide clear error status and keep fallback so photo never vanishes
            set_status(f"File '{fname}' belum ada di ~/Pictures. Silakan salin file ke ~/Pictures via File Manager.")
            return fallback

        set_status("Path penyimpanan tidak valid.")
        return fallback

    # Handle web URLs
    url = normalize_url(raw_val)
    if not (url.startswith("http://") or url.startswith("https://")):
        set_status(f"Format URL atau path tidak dikenali: {raw_val}")
        return fallback

    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    temp_dest = CACHE_DIR / f"temp_{url_hash}.bin"
    final_dest = CACHE_DIR / f"img_{url_hash}.jpg"

    # If already cached and valid, return it
    if final_dest.exists() and final_dest.stat().st_size > 0:
        set_status("OK")
        return str(final_dest)

    # Download to temporary location
    if not download_file(url, temp_dest):
        temp_dest.unlink(missing_ok=True)
        set_status("Gagal mengunduh gambar dari URL. Periksa koneksi internet atau coba link lain.")
        return fallback

    # Check if downloaded file is HTML (e.g. webpage link)
    try:
        with open(temp_dest, "rb") as f:
            header = f.read(512).lower()
        if b"<!doctype html" in header or b"<html" in header:
            content = temp_dest.read_text(errors="ignore")
            og_url = extract_image_from_html(content, url)
            temp_dest.unlink(missing_ok=True)
            if og_url and og_url != url:
                return resolve_photo(og_url, fallback)
            set_status("URL tersebut adalah halaman web dan tidak ditemukan gambar foto (og:image).")
            return fallback
    except Exception:
        pass

    # Verify and convert using PIL
    if HAS_PIL:
        try:
            with Image.open(temp_dest) as img:
                # Handle orientation if EXIF present (crucial for smartphone photos)
                try:
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass

                # If has alpha channel or palette with transparency, save as PNG
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    png_dest = CACHE_DIR / f"img_{url_hash}.png"
                    img.save(png_dest, format="PNG", optimize=True)
                    temp_dest.unlink(missing_ok=True)
                    set_status("OK")
                    return str(png_dest)
                else:
                    # Convert to RGB and save as high-quality JPEG
                    rgb = img.convert("RGB")
                    rgb.save(final_dest, format="JPEG", quality=92, optimize=True)
                    temp_dest.unlink(missing_ok=True)
                    set_status("OK")
                    return str(final_dest)
        except Exception:
            pass

    # Fallback if PIL failed or not available: check magic bytes
    try:
        with open(temp_dest, "rb") as f:
            head = f.read(16)
        if head.startswith(b"\xff\xd8\xff"):
            temp_dest.rename(final_dest)
            set_status("OK")
            return str(final_dest)
        elif head.startswith(b"\x89PNG"):
            png_dest = CACHE_DIR / f"img_{url_hash}.png"
            temp_dest.rename(png_dest)
            set_status("OK")
            return str(png_dest)
        elif b"WEBP" in head:
            webp_dest = CACHE_DIR / f"img_{url_hash}.webp"
            temp_dest.rename(webp_dest)
            set_status("OK")
            return str(webp_dest)
    except Exception:
        pass

    temp_dest.unlink(missing_ok=True)
    set_status("File yang diunduh bukan gambar yang valid.")
    return fallback

def main():
    if len(sys.argv) < 2:
        print("")
        sys.exit(0)

    arg = sys.argv[1]
    fallback = sys.argv[2] if len(sys.argv) > 2 else ""
    result = resolve_photo(arg, fallback)
    print(result)

if __name__ == "__main__":
    main()
