#!/usr/bin/env python3
"""Render a Salesforce Diagrams spec (JSON) to SVG, following the Salesforce
Architects 'Standard Components' (Header, Cards, Connectors, Pills, Key).

Usage:
    python render_svg.py spec.json out.svg [--png out.png]

Spec format: see references/spec-format.md
"""
import json, sys, math, html, argparse

# ---------------------------------------------------------------- palette
NAVY = "#032D60"        # header title / description text
TEXT = "#181818"        # card text
BORDER = "#181818"      # outer card border (reference gallery style)
BORDER_SOFT = "#747474" # kit-of-parts gray-50 border (nested / secondary)
GRAY90 = "#E5E5E5"      # header band, footer band, title rule
GRAY80 = "#C9C9C9"
WHITE = "#FFFFFF"
FONT = "'Salesforce Sans', 'Inter', 'Helvetica Neue', Arial, sans-serif"

# Approximate brand colours for card/footer icon discs (see references/standard-components.md)
ICON_COLOURS = {
    "platform": "#032D60", "agentforce": "#032D60", "integration": "#032D60",
    "sales": "#0B827C", "service": "#A0094F", "marketing": "#DD7A01",
    "commerce": "#04844B", "data360": "#2E0B3B", "datacloud": "#2E0B3B",
    "industries": "#5A1BA9", "analytics": "#032D60", "tableau": "#032D60",
    "slack": "#4A154B", "mulesoft": "#00A0DF", "experience": "#1B5297",
    "external": "#3E3E3C", "sync": "#F38151", "async": "#6E9AE0",
}

def esc(s): return html.escape(str(s), quote=True)

def text_w(s, size, bold=False):
    return len(str(s)) * size * (0.58 if bold else 0.53)

def wrap(s, size, max_w, bold=False):
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, size, bold) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines or [""]

def colour(c, default=NAVY):
    if not c: return default
    return ICON_COLOURS.get(str(c).lower(), c)

# ---------------------------------------------------------------- primitives
def icon_disc(cx, cy, r, icon):
    """icon: str glyph or {glyph, colour}. Glyph = 1-3 chars (initials)."""
    if isinstance(icon, str): icon = {"glyph": icon}
    fill = colour(icon.get("colour") or icon.get("color"))
    g = esc(icon.get("glyph", ""))[:3]
    fs = r * (0.9 if len(g) <= 1 else 0.72 if len(g) == 2 else 0.58)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<text x="{cx}" y="{cy + fs*0.35}" font-size="{fs:.1f}" font-weight="700" '
            f'text-anchor="middle" fill="{WHITE}">{g}</text>')

def pill(cx, cy, label, dashed=False, size=13, numbered=False):
    if numbered:
        r = 12
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1.5"/>'
                f'<text x="{cx}" y="{cy+4.5}" font-size="13" font-weight="700" text-anchor="middle" fill="{TEXT}">{esc(label)}</text>')
    lines = str(label).split("\n")
    w = max(text_w(l, size, True) for l in lines) + 28
    h = 14 + len(lines) * (size + 3)
    x, y = cx - w/2, cy - h/2
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    out = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="{WHITE}" stroke="{BORDER}" stroke-width="1.5"{dash}/>'
    for i, l in enumerate(lines):
        ty = y + 7 + size + i*(size+3) - 2
        out += f'<text x="{cx:.1f}" y="{ty:.1f}" font-size="{size}" font-weight="700" text-anchor="middle" fill="{TEXT}">{esc(l)}</text>'
    return out

# ---------------------------------------------------------------- header
def render_header(spec, W):
    hd = spec.get("header", {})
    H = max(int(spec.get("_body_h", 600) * 0.10), hd.get("height", 0), 170)
    split = W * 0.42
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WHITE}"/>',
         f'<path d="M{split-60},0 H{W} V{H} H{split-60} C{split+40},{H*0.65} {split+40},{H*0.35} {split-60},0 Z" fill="{GRAY90}"/>']
    x, y = 40, 46
    if hd.get("logo"):
        o.append(f'<rect x="{x}" y="22" width="130" height="24" fill="#E16B8C"/>'
                 f'<text x="{x+65}" y="39" font-size="12" text-anchor="middle" fill="{NAVY}">{esc(hd["logo"])}</text>')
        y = 70
    ts = hd.get("title_size", 30)
    for i, l in enumerate(wrap(hd.get("title", "Diagram Title"), ts, split - 110)):
        y += ts + 4
        o.append(f'<text x="{x}" y="{y}" font-size="{ts}" fill="{NAVY}">{esc(l)}</text>')
    ds = max(ts // 2, 14)
    y += 8
    for l in wrap(hd.get("description", ""), ds, split - 110):
        y += ds + 7
        o.append(f'<text x="{x}" y="{y}" font-size="{ds}" fill="{NAVY}">{esc(l)}</text>')
    key = hd.get("key", [])
    cols = hd.get("key_columns") or max(1, min(4, math.ceil(len(key) / 3))) if key else 1
    rows = math.ceil(len(key) / cols) if key else 0
    H = max(H, y + 28, 44 + 20 + rows * 46)
    # rebuild band at final height
    o[0] = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WHITE}"/>'
    o[1] = f'<path d="M{split-60},0 H{W} V{H} H{split-60} C{split+40},{H*0.65} {split+40},{H*0.35} {split-60},0 Z" fill="{GRAY90}"/>'
    if key:
        kx, ky, kw, kh = split + 80, 22, W - split - 110, H - 44
        o.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" rx="10" fill="{WHITE}"/>')
        cw, rh = (kw - 30) / cols, (kh - 20) / rows
        for i, k in enumerate(key):
            cx = kx + 18 + (i % cols) * cw
            cy = ky + 14 + (i // cols) * rh + rh / 2
            if "line" in k:
                dash = ' stroke-dasharray="7 5"' if k["line"] == "dashed" else ' stroke-dasharray="2 4"' if k["line"] == "dotted" else ""
                o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+44}" y2="{cy}" stroke="{colour(k.get("colour"), BORDER)}" stroke-width="2"{dash}/>')
                lx = cx + 56
            else:
                o.append(icon_disc(cx + 16, cy, 15, k.get("icon", {"glyph": ""})))
                lx = cx + 40
            o.append(f'<text x="{lx}" y="{cy+5}" font-size="14" fill="{NAVY}">{esc(k.get("label",""))}</text>')
    return H, "".join(o)

# ---------------------------------------------------------------- cards
def card_min_h(c):
    nested = c.get("nested", False)
    fsz = c.get("title_size", 18 if not nested else 15)
    r = c.get("icon_r", 22)
    tx = c["x"] + 16 + (2*r + 14 if c.get("icon") else 0)
    tl = len(wrap(c.get("title", ""), fsz, c["x"] + c["w"] - tx - 12, True))
    top = (14 + 2*r + 4) if c.get("icon") else (34 if not nested else 30) + (tl-1)*(fsz+3) + 12
    asz = c.get("attr_size", 14)
    body = sum(len(wrap(a, asz, c["x"] + c["w"] - tx - 12)) * (asz + 7) + 3 for a in c.get("attributes", []))
    body = body + 14 if body else 10
    return top + body + (34 if c.get("footer") else 0) + (58 if c.get("footer_icons") else 0) + (6 if body > 10 else 0)

def render_card(c, oy):
    x, y, w, h = c["x"], c["y"] + oy, c["w"], c["h"]
    nested = c.get("nested", False)
    sw = c.get("stroke_width", 1.5 if nested else 2.5)
    stroke = c.get("stroke", BORDER)
    fill = c.get("fill", WHITE)
    dash = {"dashed": ' stroke-dasharray="8 5"', "dotted": ' stroke-dasharray="2 4"'}.get(c.get("border"), "")
    if c.get("border") == "none": sw = 0
    rx = c.get("radius", 16 if not nested else 12)
    cid = "clip_" + c["id"]
    o = [f'<g id="{esc(c["id"])}">',
         f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>']
    fsz = c.get("title_size", 18 if not nested else 15)
    tx = x + 16
    ty = y + 34 if not nested else y + 30
    if c.get("icon"):
        r = c.get("icon_r", 22)
        o.append(icon_disc(x + 16 + r, y + 14 + r, r, c["icon"]))
        tx = x + 16 + 2*r + 14
        ty = y + 14 + r + fsz*0.35
    tlines = wrap(c.get("title", ""), fsz, x + w - tx - 12, True)
    ty -= (len(tlines) - 1) * (fsz + 3) / 2 if c.get("icon") else 0
    for i, l in enumerate(tlines):
        o.append(f'<text x="{tx}" y="{ty + i*(fsz+3):.1f}" font-size="{fsz}" font-weight="700" fill="{TEXT}">{esc(l)}</text>')
    rule_y = max(ty + (len(tlines)-1)*(fsz+3) + 12, (y + 14 + 2*c.get("icon_r", 22) + 4) if c.get("icon") and c.get("attributes") else 0)
    if c.get("title_rule", True):
        o.append(f'<line x1="{tx}" y1="{rule_y:.1f}" x2="{x+w}" y2="{rule_y:.1f}" stroke="{GRAY90}" stroke-width="3" clip-path="url(#{cid})"/>')
    ay = rule_y + 24
    asz = c.get("attr_size", 14)
    for a in c.get("attributes", []):
        for l in wrap(a, asz, x + w - tx - 12):
            o.append(f'<text x="{tx}" y="{ay:.1f}" font-size="{asz}" fill="{TEXT}">{esc(l)}</text>')
            ay += asz + 7
        ay += 3
    icons = c.get("footer_icons", [])
    icon_row = 58 if icons else 0
    if c.get("footer"):
        fy = y + h - icon_row - 34
        o.append(f'<rect x="{x}" y="{fy}" width="{w}" height="32" fill="{GRAY90}" clip-path="url(#{cid})"/>')
        o.append(f'<text x="{x+w/2}" y="{fy+21}" font-size="13" text-anchor="middle" fill="{TEXT}">{esc(c["footer"])}</text>')
    if icons:
        n, r = len(icons), 17
        gap = min(52, (w - 30) / max(n, 1))
        sx = x + w/2 - gap*(n-1)/2
        for i, ic in enumerate(icons):
            o.append(icon_disc(sx + i*gap, y + h - 30, r, ic))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
    o.append("</g>")
    return "".join(o)

# ---------------------------------------------------------------- connectors
def port(c, side, frac, oy):
    x, y, w, h = c["x"], c["y"] + oy, c["w"], c["h"]
    return {"left": (x, y + h*frac), "right": (x + w, y + h*frac),
            "top": (x + w*frac, y), "bottom": (x + w*frac, y + h)}[side]

def auto_sides(a, b):
    acx, acy = a["x"] + a["w"]/2, a["y"] + a["h"]/2
    bcx, bcy = b["x"] + b["w"]/2, b["y"] + b["h"]/2
    hgap = max(b["x"] - (a["x"]+a["w"]), a["x"] - (b["x"]+b["w"]))
    vgap = max(b["y"] - (a["y"]+a["h"]), a["y"] - (b["y"]+b["h"]))
    if hgap >= vgap:
        return ("right", "left") if bcx > acx else ("left", "right")
    return ("bottom", "top") if bcy > acy else ("top", "bottom")

def route(p1, s1, p2, s2, via=None):
    (x1, y1), (x2, y2) = p1, p2
    horiz = s1 in ("left", "right")
    if horiz and s2 in ("left", "right"):
        if abs(y1 - y2) < 0.5: return [p1, p2]
        mx = via if via is not None else (x1 + x2) / 2
        return [p1, (mx, y1), (mx, y2), p2]
    if not horiz and s2 in ("top", "bottom"):
        if abs(x1 - x2) < 0.5: return [p1, p2]
        my = via if via is not None else (y1 + y2) / 2
        return [p1, (x1, my), (x2, my), p2]
    return [p1, (x2, y1), p2] if horiz else [p1, (x1, y2), p2]

def arrowhead(p_from, p_to, col):
    (x1, y1), (x2, y2) = p_from, p_to
    a = math.atan2(y2 - y1, x2 - x1); L, Wd = 12, 5
    pts = [(x2, y2), (x2 - L*math.cos(a) + Wd*math.sin(a), y2 - L*math.sin(a) - Wd*math.cos(a)),
           (x2 - L*math.cos(a) - Wd*math.sin(a), y2 - L*math.sin(a) + Wd*math.cos(a))]
    return f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px,py in pts)}" fill="{col}"/>'

def render_connector(cn, cards, oy):
    a, b = cards[cn["from"]], cards[cn["to"]]
    s1, s2 = auto_sides(a, b)
    s1, s2 = cn.get("from_side", s1), cn.get("to_side", s2)
    p1 = port(a, s1, cn.get("from_port", 0.5), oy)
    p2 = port(b, s2, cn.get("to_port", 0.5), oy)
    if cn.get("straight") and s1 in ("left","right"): p2 = (p2[0], p1[1])
    if cn.get("straight") and s1 in ("top","bottom"): p2 = (p1[0], p2[1])
    pts = route(p1, s1, p2, s2, cn.get("via"))
    col = colour(cn.get("colour"), BORDER)
    dash = {"dashed": ' stroke-dasharray="7 5"', "dotted": ' stroke-dasharray="2 4"'}.get(cn.get("style"), "")
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o = [f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"{dash}/>']
    arrow = cn.get("arrow", "end")
    if arrow in ("end", "both"): o.append(arrowhead(pts[-2], pts[-1], col))
    if arrow in ("start", "both"): o.append(arrowhead(pts[1], pts[0], col))
    label, step = cn.get("label"), cn.get("step")
    if label or step is not None:
        segs = list(zip(pts, pts[1:]))
        i = max(range(len(segs)), key=lambda k: math.dist(*segs[k]))
        (sx, sy), (ex, ey) = segs[i]
        t = cn.get("label_pos", 0.5)
        cx, cy = sx + (ex - sx)*t, sy + (ey - sy)*t
        o.append(pill(cx, cy, step if step is not None else label, dashed=bool(dash), numbered=step is not None))
    return "".join(o)

# ---------------------------------------------------------------- swimlanes / timeline
def render_lanes(spec, W, oy):
    tl = spec.get("timeline")
    if not tl: return ""
    o = []
    lx, lw = tl.get("x", 40), tl.get("label_w", 100)
    cols, lanes = tl["columns"], tl["lanes"]
    cx0 = lx + lw; cw = (W - 40 - cx0) / len(cols); hh = tl.get("header_h", 70)
    top = oy + tl.get("y", 0)
    total_h = sum(l["h"] for l in lanes)
    for i, c in enumerate(cols):
        fill = "#F3F4F6" if i % 2 else WHITE
        o.append(f'<rect x="{cx0+i*cw:.1f}" y="{top}" width="{cw:.1f}" height="{hh+total_h}" fill="{fill}" stroke="#7A7A85" stroke-width="1"/>')
        o.append(f'<text x="{cx0+i*cw+cw/2:.1f}" y="{top+hh/2+6}" font-size="16" font-weight="700" text-anchor="middle" fill="{TEXT}">{esc(c)}</text>')
    ly = top + hh
    for l in lanes:
        o.append(f'<rect x="{lx}" y="{ly}" width="{W-40-lx}" height="{l["h"]}" fill="none" stroke="#7A7A85" stroke-width="1"/>')
        o.append(f'<text x="{lx+lw/2}" y="{ly+l["h"]/2+5}" font-size="15" font-weight="700" text-anchor="middle" fill="#3E3E3C">{esc(l["label"])}</text>')
        ly += l["h"]
    return "".join(o)

# ---------------------------------------------------------------- main
def render(spec):
    W = spec.get("width", 1400)
    cards = {c["id"]: c for c in spec.get("cards", [])}
    for c in cards.values():
        need = card_min_h(c)
        if not c.get("children_fit") and c["h"] < need:
            print(f"warning: card '{c['id']}' grown from h={c['h']} to h={need:.0f} to fit content; check for overlaps", file=sys.stderr)
            c["h"] = math.ceil(need)
    body_h = max([c["y"] + c["h"] for c in cards.values()] + [0]) + 40
    if spec.get("timeline"):
        t = spec["timeline"]; body_h = max(body_h, t.get("y", 0) + t.get("header_h", 70) + sum(l["h"] for l in t["lanes"]) + 40)
    spec["_body_h"] = body_h
    head_h, head_svg = render_header(spec, W)
    oy = head_h + spec.get("header_gap", 40)
    H = oy + body_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}" font-family="{FONT}">',
             f'<title>{esc(spec.get("header",{}).get("title",""))}</title>',
             f'<desc>{esc(spec.get("header",{}).get("description",""))}</desc>',
             f'<rect width="{W}" height="{H:.0f}" fill="{WHITE}"/>', head_svg, render_lanes(spec, W, oy)]
    # containers first (cards that others reference as parent / or flagged), then nested, then connectors on top
    order = sorted(cards.values(), key=lambda c: (c.get("layer", 1 if c.get("nested") else 0)))
    parts += [render_card(c, oy) for c in order]
    parts += [render_connector(cn, cards, oy) for cn in spec.get("connectors", [])]
    parts.append("</svg>")
    return "".join(parts)

def write_png(svg, svg_path, png_path, width=1600):
    """Rasterise with the first available tool. Returns True on success."""
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=png_path, output_width=width)
        return True
    except (ImportError, OSError):  # OSError: cairosvg installed but Cairo DLL missing (common on Windows)
        pass
    import shutil, subprocess
    candidates = [
        ("rsvg-convert", ["-w", str(width), "-o", png_path, svg_path]),
        ("inkscape", [svg_path, "--export-type=png", f"--export-filename={png_path}", f"--export-width={width}"]),
    ]
    for exe, args in candidates:
        path = shutil.which(exe)
        if path and subprocess.run([path] + args, capture_output=True).returncode == 0:
            return True
    return False

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out"); ap.add_argument("--png")
    a = ap.parse_args()
    # Explicit UTF-8: Windows defaults to cp1252 and fails on characters like "→".
    with open(a.spec, encoding="utf-8") as f:
        svg = render(json.load(f))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {a.out}")
    if a.png:
        if write_png(svg, a.out, a.png):
            print(f"wrote {a.png}")
        else:
            print("PNG not written: no SVG rasteriser found. Install one of:\n"
                  "  pip install cairosvg   (on Windows also needs the GTK/Cairo runtime)\n"
                  "  rsvg-convert (librsvg) or Inkscape on PATH\n"
                  f"The SVG at {a.out} is complete and can be opened in a browser.",
                  file=sys.stderr)
            sys.exit(2)
