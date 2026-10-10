#!/usr/bin/env python3
"""
Generate assets/identity-particle.gif

Kali dragon (particles) -> dissolve -> particle portrait -> hold -> dissolve -> Kali dragon.

One fixed population of particles is used for the whole loop. Each particle owns a
position on the logo, a position in the portrait and a position in a cloud, so the
motion you see is real particle movement, not a cross-fade.

Dependencies: Pillow, NumPy only.

Inputs (defaults, relative to the repository root):
    assets/kali-logo.png    Kali dragon logo as PNG (transparent background preferred)
    assets/portrait.jpg     your portrait (.jpg/.jpeg/.png), the higher resolution the better

Usage:
    python scripts/generate_identity_particle.py
    python scripts/generate_identity_particle.py --portrait-crop 120,40,800,800
    python scripts/generate_identity_particle.py --check-only      # portrait quality report only
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- configuration
SIZE = 420                 # output is SIZE x SIZE
N_PARTICLES = 6500
FPS = 16
SEED = 94956               # fixed seed -> reproducible output
FIELD = 0.80               # fraction of the canvas the logo/portrait occupies
BG = (10, 10, 11)          # near-black
SILVER = (232, 234, 236)
GREEN = (120, 170, 140)    # muted green, used only for a faint tint in the cloud

# phase durations in seconds (total must stay inside 6-10 s)
T_LOGO_HOLD = 1.2
T_DISSOLVE = 1.3
T_FORM = 1.7
T_PORTRAIT_HOLD = 1.8
T_DISSOLVE_2 = 1.2
T_RECON = 1.6


# ---------------------------------------------------------------- helpers
def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def ease_in_out(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * x * (x * (x * 6 - 15) + 10)  # smootherstep


def load_image(path: Path | None, url: str | None, label: str) -> Image.Image:
    if path is not None and path.exists():
        return Image.open(path)
    if url:
        print(f"[info] {label}: {path} not found, downloading {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "identity-particle/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - user supplied URL
            import io
            return Image.open(io.BytesIO(r.read()))
    sys.exit(f"[error] {label} not found at {path}. Provide the file or pass a URL option.")


def hilbert_index(x: np.ndarray, y: np.ndarray, order: int = 10) -> np.ndarray:
    """Hilbert curve index for integer grid coordinates (vectorised)."""
    n = 1 << order
    x = x.astype(np.int64).copy()
    y = y.astype(np.int64).copy()
    d = np.zeros_like(x)
    s = n // 2
    while s > 0:
        rx = ((x & s) > 0).astype(np.int64)
        ry = ((y & s) > 0).astype(np.int64)
        d += s * s * ((3 * rx) ^ ry)
        low = ry == 0
        flip = low & (rx == 1)
        x = np.where(flip, n - 1 - x, x)
        y = np.where(flip, n - 1 - y, y)
        x, y = np.where(low, y, x), np.where(low, x, y)
        s //= 2
    return d


# ---------------------------------------------------------------- logo
def logo_mask(img: Image.Image, invert: bool) -> np.ndarray:
    """Return float mask in [0,1] (1 = logo ink), square, padded."""
    img = img.convert("RGBA")
    arr = np.asarray(img).astype(np.float32) / 255.0
    alpha = arr[..., 3]
    if alpha.min() < 0.99:                       # real transparency -> use it
        mask = alpha
    else:                                        # opaque -> use luminance
        lum = arr[..., :3] @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
        mask = lum if invert else 1.0 - lum
        mask = np.clip((mask - mask.min()) / max(1e-6, mask.max() - mask.min()), 0, 1)
    ys, xs = np.where(mask > 0.1)
    if len(xs) == 0:
        sys.exit("[error] logo mask is empty; try --logo-invert")
    mask = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = mask.shape
    side = max(h, w)
    out = np.zeros((side, side), np.float32)
    out[(side - h) // 2:(side - h) // 2 + h, (side - w) // 2:(side - w) // 2 + w] = mask
    return out


def sample_logo(mask: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    """Particles uniformly on the logo ink, biased slightly toward edges for crisp outlines."""
    side = mask.shape[0]
    img = Image.fromarray((mask * 255).astype(np.uint8))
    img = img.resize((512, 512), Image.LANCZOS)
    m = np.asarray(img).astype(np.float32) / 255.0
    edge = np.asarray(img.filter(ImageFilter.FIND_EDGES)).astype(np.float32) / 255.0
    w = (m > 0.35).astype(np.float32) * (1.0 + 1.5 * edge)
    w = w.ravel()
    w /= w.sum()
    idx = rng.choice(w.size, size=n, p=w)
    ys, xs = np.divmod(idx, 512)
    pts = np.stack([xs, ys], 1).astype(np.float32) + rng.uniform(-0.5, 0.5, (n, 2))
    pts = pts / 512.0                                        # 0..1
    return (pts - 0.5) * FIELD * SIZE + SIZE / 2


# ---------------------------------------------------------------- portrait
def quality_report(img: Image.Image) -> list[str]:
    warnings: list[str] = []
    w, h = img.size
    print(f"[portrait] {w}x{h}px")
    if min(w, h) < 400:
        warnings.append(f"Low resolution ({w}x{h}). Facial detail will be thin; use >= 800 px on the short side.")
    g = np.asarray(img.convert("L")).astype(np.float32)
    # sharpness: variance of a Laplacian
    lap = (-4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:])
    sharp = float(lap.var())
    contrast = float(g.std())
    print(f"[portrait] sharpness(var Laplacian)={sharp:.1f}  contrast(std)={contrast:.1f}")
    if sharp < 25:
        warnings.append("Image looks soft/blurry; a particle portrait needs a sharp, in-focus face.")
    if contrast < 35:
        warnings.append("Low tonal contrast; use even, directional lighting and a plain background.")
    return warnings


def silhouette_mask(rgb: Image.Image) -> np.ndarray | None:
    """Head-and-shoulders mask (512x512 float in [0,1]) for photos with a fairly plain
    background. The background colour is estimated from the top and side borders (the
    bottom is skipped because shoulders reach it), pixels far from it are foreground,
    then the mask is cleaned with median/closing filters. Returns None when the result
    is implausible (so the caller can fall back to the elliptical vignette)."""
    a = np.asarray(rgb).astype(np.float32)
    b = 28
    border = np.concatenate([a[:b].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    dist = np.sqrt(((a - bg) ** 2).sum(-1))
    # Threshold relative to how much the background itself varies (noise/gradient). A global
    # method such as Otsu is deliberately avoided: it separates skin from everything else
    # and loses dark hair and clothing, which are exactly what the silhouette must keep.
    border_d = np.concatenate([dist[:b].ravel(), dist[:, :b].ravel(), dist[:, -b:].ravel()])
    thr = max(2.5 * float(np.percentile(border_d, 90)), 14.0)
    m = Image.fromarray(((dist > thr) * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MedianFilter(7))
    m = m.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))      # close small holes
    m = m.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))        # drop specks
    frac = float((np.asarray(m) > 127).mean())
    if not 0.15 <= frac <= 0.85:
        print(f"[warn] silhouette mask covers {frac:.0%} of the frame; ignoring it (background too busy?)")
        return None
    return np.asarray(m.filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255.0


def portrait_density(img: Image.Image, crop: tuple[int, int, int, int] | None,
                     invert: bool, silhouette: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Return (density map, luminance map), both 512x512 float32 in [0,1]."""
    img = ImageOps.exif_transpose(img).convert("RGB")
    if crop:
        x, y, w, h = crop
        img = img.crop((x, y, x + w, y + h))
    else:
        w, h = img.size
        s = min(w, h)
        img = img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    img = img.resize((512, 512), Image.LANCZOS)
    g = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    g = ImageOps.equalize(g)                                   # global tone spread
    lum = np.asarray(g).astype(np.float32) / 255.0
    # local contrast boost (unsharp) recovers facial structure from flat photos
    blur = np.asarray(g.filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255.0
    lum = np.clip(lum + 0.9 * (lum - blur), 0, 1)
    if invert:
        lum = 1.0 - lum
    edge = np.asarray(g.filter(ImageFilter.GaussianBlur(1.2)).filter(ImageFilter.FIND_EDGES)).astype(np.float32) / 255.0
    edge = np.clip(edge * 3.0, 0, 1)
    # soft elliptical vignette: keep the head, drop the corners
    yy, xx = np.mgrid[0:512, 0:512].astype(np.float32)
    r = np.sqrt(((xx - 256) / 236) ** 2 + ((yy - 250) / 252) ** 2)
    vignette = 1.0 - smoothstep((r - 0.82) / 0.18)
    sil = silhouette_mask(img) if silhouette else None
    if sil is not None:
        # keep head + shoulders, damp the background, and add a rim along the outline so
        # the silhouette itself is drawn in particles
        rim = np.asarray(Image.fromarray((sil * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)).astype(np.float32) / 255.0
        rim = np.clip(rim * 3.0, 0, 1)
        soft = 0.12 + 0.88 * sil
        # inside the silhouette add a small base density so dark hair/clothing still read
        density = (0.85 * lum ** 2.2 + 0.60 * edge + 0.22 * sil) * soft + 0.45 * rim
        density *= 1.0 - smoothstep((np.sqrt(((xx - 256) / 300) ** 2 + ((yy - 256) / 300) ** 2) - 0.9) / 0.1)
        return density.astype(np.float32), (lum * (0.35 + 0.65 * sil)).astype(np.float32)
    density = (0.85 * lum ** 2.2 + 0.60 * edge) * vignette
    return density.astype(np.float32), (lum * vignette).astype(np.float32)


def sample_portrait(density: np.ndarray, lum: np.ndarray, n: int,
                    rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    w = density.ravel().astype(np.float64) + 1e-9
    w /= w.sum()
    idx = rng.choice(w.size, size=n, p=w)
    ys, xs = np.divmod(idx, 512)
    pts = np.stack([xs, ys], 1).astype(np.float32) + rng.uniform(-0.5, 0.5, (n, 2))
    bright = lum[ys, xs]
    pts = pts / 512.0
    return (pts - 0.5) * FIELD * SIZE + SIZE / 2, bright


# ---------------------------------------------------------------- correspondence
def match(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Return permutation p so that a[i] pairs with b[p[i]] with spatial coherence.
    Both point sets are ordered along a Hilbert curve, then paired rank-to-rank."""
    def key(p: np.ndarray) -> np.ndarray:
        q = np.clip(((p - SIZE * (1 - FIELD) / 2) / (SIZE * FIELD)) * 1023, 0, 1023)
        return hilbert_index(q[:, 0], q[:, 1], order=10)
    oa = np.argsort(key(a), kind="stable")
    ob = np.argsort(key(b), kind="stable")
    perm = np.empty(len(a), np.int64)
    perm[oa] = ob
    return perm


# ---------------------------------------------------------------- animation
def build_cloud(logo: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """A diffuse spherical-ish cloud centred on the canvas."""
    n = len(logo)
    ang = rng.uniform(0, 2 * np.pi, n)
    rad = SIZE * 0.5 * np.sqrt(rng.uniform(0.05, 1.0, n)) * 0.98
    cloud = np.stack([np.cos(ang), np.sin(ang)], 1) * rad[:, None] + SIZE / 2
    return cloud.astype(np.float32)


def segment(a: np.ndarray, b: np.ndarray, u: float, delay: np.ndarray, swirl: np.ndarray,
            bend: np.ndarray, spread: float = 0.45) -> np.ndarray:
    """Particle positions part-way from a to b. Each particle starts at a different
    moment (delay) and takes a curved path (bend) so the motion reads as a flow."""
    local = (u - delay * spread) / (1.0 - spread)
    t = ease_in_out(local)[:, None]
    pos = a + (b - a) * t
    arc = np.sin(np.pi * np.clip(local, 0, 1))[:, None]
    d = b - a
    perp = np.stack([-d[:, 1], d[:, 0]], 1)
    return pos + perp * bend[:, None] * arc * 0.35 + swirl * arc * 10.0


def render(pos: np.ndarray, bright: np.ndarray) -> Image.Image:
    """Splat particles bilinearly onto a float canvas, add a soft glow, quantise."""
    canvas = np.zeros((SIZE, SIZE), np.float32)
    x = pos[:, 0] - 0.5
    y = pos[:, 1] - 0.5
    x0 = np.floor(x).astype(np.int64)
    y0 = np.floor(y).astype(np.int64)
    fx = (x - x0).astype(np.float32)
    fy = (y - y0).astype(np.float32)
    for dx, dy, wgt in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)),
                        (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        xi, yi = x0 + dx, y0 + dy
        ok = (xi >= 0) & (xi < SIZE) & (yi >= 0) & (yi < SIZE)
        np.add.at(canvas, (yi[ok], xi[ok]), (wgt * bright)[ok])
    sharp = np.clip(canvas * 1.15, 0, 1)
    glow = np.asarray(Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255.0
    lvl = np.clip(sharp + 0.55 * glow, 0, 1)
    idx = np.rint(lvl * 31).astype(np.uint8)         # 32 grey levels, one shared palette
    im = Image.fromarray(idx, "P")
    im.putpalette(palette())
    return im


def palette() -> list[int]:
    # One palette for every frame (no flicker): near-black -> silver, with a very faint
    # muted-green cast in the darkest mid-tones so the glow reads as "terminal", not grey.
    pal: list[int] = []
    for i in range(32):
        t = i / 31.0
        base = np.array(BG, np.float64) * (1 - t) + np.array(SILVER, np.float64) * t
        cast = 0.10 * np.sin(np.pi * t) ** 2          # peaks mid-scale, zero at both ends
        base = base * (1 - cast) + np.array(GREEN, np.float64) * cast
        pal += [int(round(c)) for c in base]
    pal += [0] * (768 - len(pal))
    return pal


def build_frames(logo_pts, portrait_pts, portrait_bright, rng) -> list[Image.Image]:
    n = len(logo_pts)
    perm = match(logo_pts, portrait_pts)
    p_pts = portrait_pts[perm]
    p_bright = portrait_bright[perm]
    cloud = build_cloud(logo_pts, rng)
    # second cloud (for the way back) is the first one rotated, so the return path differs
    c2 = (cloud - SIZE / 2)
    th = 0.9
    rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]], np.float32)
    cloud2 = c2 @ rot.T + SIZE / 2

    delay = rng.uniform(0, 1, n).astype(np.float32)
    swirl = rng.normal(0, 1, (n, 2)).astype(np.float32)
    bend = rng.normal(0, 1, n).astype(np.float32)
    phase = rng.uniform(0, 2 * np.pi, n).astype(np.float32)
    logo_b = np.clip(rng.normal(0.9, 0.08, n), 0.55, 1.0).astype(np.float32)
    cloud_b = np.full(n, 0.55, np.float32)
    p_b = (0.35 + 0.65 * p_bright).astype(np.float32)

    def hold(pts, k, t):
        return pts + np.stack([np.sin(t * 2.1 + phase), np.cos(t * 1.7 + phase)], 1) * k

    phases = [("logo", T_LOGO_HOLD), ("dissolve", T_DISSOLVE), ("form", T_FORM),
              ("portrait", T_PORTRAIT_HOLD), ("dissolve2", T_DISSOLVE_2), ("recon", T_RECON)]
    total = sum(d for _, d in phases)
    frames_n = int(round(total * FPS))
    frames: list[Image.Image] = []
    for f in range(frames_n):
        t = f / FPS
        acc = 0.0
        for name, dur in phases:
            if t < acc + dur or name == phases[-1][0]:
                u = (t - acc) / dur
                break
            acc += dur
        if name == "logo":
            pos, br = hold(logo_pts, 0.35, t), logo_b
        elif name == "dissolve":
            pos = segment(logo_pts, cloud, u, delay, swirl, bend)
            br = logo_b + (cloud_b - logo_b) * smoothstep(u)
        elif name == "form":
            pos = segment(cloud, p_pts, u, delay, swirl, bend)
            br = cloud_b + (p_b - cloud_b) * smoothstep(u)
        elif name == "portrait":
            pos, br = hold(p_pts, 0.30, t), p_b
        elif name == "dissolve2":
            pos = segment(p_pts, cloud2, u, delay, swirl, bend)
            br = p_b + (cloud_b - p_b) * smoothstep(u)
        else:  # recon
            pos = segment(cloud2, logo_pts, u, delay, swirl, bend)
            br = cloud_b + (logo_b - cloud_b) * smoothstep(u)
        frames.append(render(pos.astype(np.float32), br.astype(np.float32)))
    return frames


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--logo", type=Path, default=ROOT / "assets/kali-logo.png")
    ap.add_argument("--logo-url", default=None, help="optional PNG URL used only if --logo is missing")
    ap.add_argument("--logo-invert", action="store_true", help="logo is light on a dark opaque background")
    ap.add_argument("--portrait", type=Path, default=None, help="default: assets/portrait.{jpg,jpeg,png}")
    ap.add_argument("--portrait-url", default=None, help="optional image URL used only if no portrait file exists")
    ap.add_argument("--portrait-crop", default=None, help="x,y,w,h crop box in source pixels (square recommended)")
    ap.add_argument("--portrait-invert", action="store_true")
    ap.add_argument("--silhouette", action="store_true",
                    help="weight head+shoulders by an automatic silhouette mask (needs a fairly plain background)")
    ap.add_argument("--out", type=Path, default=ROOT / "assets/identity-particle.gif")
    ap.add_argument("--check-only", action="store_true", help="print portrait quality report and exit")
    ap.add_argument("--allow-low-quality", action="store_true", help="do not stop on portrait quality warnings")
    args = ap.parse_args()

    portrait_path = args.portrait
    if portrait_path is None:
        for ext in ("jpg", "jpeg", "png"):
            cand = ROOT / f"assets/portrait.{ext}"
            if cand.exists():
                portrait_path = cand
                break
    portrait = load_image(portrait_path, args.portrait_url, "portrait")
    warnings = quality_report(portrait)
    for w in warnings:
        print(f"[warn] {w}")
    if args.check_only:
        sys.exit(1 if warnings else 0)
    if warnings and not args.allow_low_quality:
        sys.exit("[stop] portrait quality is likely too low for a recognisable result. "
                 "Provide a better photo or re-run with --allow-low-quality.")

    crop = tuple(int(v) for v in args.portrait_crop.split(",")) if args.portrait_crop else None
    rng = np.random.default_rng(SEED)

    logo = load_image(args.logo, args.logo_url, "kali logo")
    l_pts = sample_logo(logo_mask(logo, args.logo_invert), N_PARTICLES, rng)
    dens, lum = portrait_density(portrait, crop, args.portrait_invert, args.silhouette)
    p_pts, p_bright = sample_portrait(dens, lum, N_PARTICLES, rng)

    frames = build_frames(l_pts, p_pts, p_bright, rng)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=int(1000 / FPS),
                   loop=0, optimize=False, disposal=1)
    kb = args.out.stat().st_size / 1024
    print(f"[done] {args.out}  {len(frames)} frames @ {FPS} fps = {len(frames) / FPS:.1f}s  {kb:.0f} KB")


if __name__ == "__main__":
    main()
