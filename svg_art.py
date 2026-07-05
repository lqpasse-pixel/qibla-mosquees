# -*- coding: utf-8 -*-
"""Génération d'illustrations SVG originales, 100 % locales et libres de droits.
Chaque mosquée reçoit : hero (crépuscule), nuit, aube, un médaillon-détail et un motif géométrique."""
import math

W, H = 1200, 700

def _stars(seed, n=60, ymax=340):
    pts, x = [], (seed * 97) % 1200
    for i in range(n):
        x = (x * 73 + 41 + i * 137) % W
        y = (x * 31 + i * 59) % ymax
        r = 0.8 + ((x + y) % 3) * 0.5
        o = 0.35 + ((x * y) % 50) / 100
        pts.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#f7ecd2" opacity="{o:.2f}"/>')
    return "".join(pts)

def _moon(x=980, y=120, r=42):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f6ecd0" opacity="0.95"/>'
            f'<circle cx="{x+16}" cy="{y-8}" r="{r-6}" fill="url(#sky)" opacity="0.92"/>')

def _sun(x=960, y=190, r=55, c="#f6d488"):
    halo = f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="{c}" opacity="0.18"/>'
    return halo + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.9"/>'

def _dome(cx, base, rw, rh, fill, finial="#d8b45a"):
    """Coupole bulbeuse + croissant."""
    top = base - rh
    d = (f'M {cx-rw} {base} C {cx-rw} {base-rh*0.85}, {cx-rw*0.55} {top}, {cx} {top} '
         f'C {cx+rw*0.55} {top}, {cx+rw} {base-rh*0.85}, {cx+rw} {base} Z')
    fin = (f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{top-22}" stroke="{finial}" stroke-width="3"/>'
           f'<circle cx="{cx}" cy="{top-26}" r="4.5" fill="{finial}"/>'
           f'<path d="M {cx} {top-40} a 8 8 0 1 0 6 13 a 6.4 6.4 0 1 1 -6 -13 Z" fill="{finial}"/>')
    return f'<path d="{d}" fill="{fill}"/>' + fin

def _minaret(cx, base, h, w, fill, style="pointe", finial="#d8b45a"):
    top = base - h
    body = f'<rect x="{cx-w/2}" y="{top+30}" width="{w}" height="{h-30}" fill="{fill}"/>'
    balcon = f'<rect x="{cx-w*0.95}" y="{top+34}" width="{w*1.9}" height="7" rx="3" fill="{fill}"/>'
    if style == "pointe":  # ottoman : fuseau pointu
        cap = f'<path d="M {cx-w*0.7} {top+32} L {cx} {top-26} L {cx+w*0.7} {top+32} Z" fill="{fill}"/>'
    elif style == "carre":  # maghrébin : tour carrée + lanternon
        body = f'<rect x="{cx-w/2}" y="{top}" width="{w}" height="{h}" fill="{fill}"/>'
        cap = (f'<rect x="{cx-w*0.32}" y="{top-26}" width="{w*0.64}" height="26" fill="{fill}"/>'
               f'<circle cx="{cx}" cy="{top-34}" r="6" fill="{finial}"/>'
               f'<circle cx="{cx}" cy="{top-46}" r="4.5" fill="{finial}"/>'
               f'<circle cx="{cx}" cy="{top-56}" r="3" fill="{finial}"/>')
        balcon = ""
    else:  # bulbe : petit dôme
        cap = _dome(cx, top + 32, w * 0.85, w * 1.15, fill, finial)
    return body + balcon + cap

def _girih(cell=120, stroke="#caa54a", op=0.5, sw=1.6):
    """Tuile étoile à 8 branches (khatam) répétable."""
    c = cell / 2
    pts = []
    for i in range(16):
        a = math.pi / 8 * i
        r = c * (0.86 if i % 2 == 0 else 0.36)
        pts.append(f"{c + r*math.cos(a):.1f},{c + r*math.sin(a):.1f}")
    star = f'<polygon points="{" ".join(pts)}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>'
    sq = (f'<rect x="{c*0.29:.1f}" y="{c*0.29:.1f}" width="{c*1.42:.1f}" height="{c*1.42:.1f}" fill="none" '
          f'stroke="{stroke}" stroke-width="{sw}" opacity="{op*0.7}" transform="rotate(45 {c} {c})"/>')
    return star + sq

def _pattern_def(pid, cell=120, stroke="#caa54a", op=0.5):
    return (f'<pattern id="{pid}" width="{cell}" height="{cell}" patternUnits="userSpaceOnUse">'
            f'{_girih(cell, stroke, op)}</pattern>')

# ---------------------------------------------------------------- silhouettes
def _profil(art, sil, ground, gold):
    """Retourne le SVG de la silhouette selon le profil architectural."""
    p = art["profil"]; base = 560
    dc = art.get("dome_couleur", sil)
    s = []
    if p == "kaaba":
        s.append(f'<rect x="80" y="{base-380}" width="1040" height="380" fill="{sil}" opacity="0.25" rx="8"/>')
        for i in range(9):
            x = 110 + i * 110
            s.append(f'<path d="M {x} {base} L {x} {base-120} Q {x+40} {base-175} {x+80} {base-120} L {x+80} {base} Z" fill="{sil}" opacity="0.55"/>')
        for cx in (140, 420, 780, 1060):
            s.append(_minaret(cx, base - 120, 300, 26, sil, "bulbe", gold))
        s.append(f'<rect x="530" y="{base-210}" width="140" height="210" fill="#111318"/>')
        s.append(f'<rect x="530" y="{base-150}" width="140" height="16" fill="{gold}"/>')
        s.append(f'<rect x="576" y="{base-118}" width="48" height="118" fill="{gold}" opacity="0.85"/>')
    elif p in ("classique", "ottoman", "moghol", "caire"):
        nd = art.get("domes", 3); nm = art.get("minarets", 2)
        mstyle = "pointe" if p == "ottoman" else "bulbe"
        s.append(f'<rect x="240" y="{base-150}" width="720" height="150" fill="{sil}"/>')
        for i in range(7):
            x = 268 + i * 98
            s.append(f'<path d="M {x} {base} L {x} {base-88} Q {x+32} {base-128} {x+64} {base-88} L {x+64} {base} Z" fill="{ground}" opacity="0.9"/>')
        if p == "ottoman":
            s.append(_dome(600, base - 150, 190, 150, sil, gold))
            for cx, rw in ((440, 95), (760, 95), (330, 60), (870, 60)):
                s.append(_dome(cx, base - 148, rw, rw * 0.8, sil, gold))
        else:
            dome_fill = dc
            s.append(_dome(600, base - 150, 150, 170, dome_fill, gold))
            if nd >= 3:
                s.append(_dome(400, base - 150, 100, 115, dome_fill, gold))
                s.append(_dome(800, base - 150, 100, 115, dome_fill, gold))
            if nd >= 5:
                s.append(_dome(285, base - 150, 62, 72, dome_fill, gold))
                s.append(_dome(915, base - 150, 62, 72, dome_fill, gold))
        pos = {1:[150], 2:[150,1050], 3:[120,600,1080], 4:[110,235,965,1090], 6:[70,170,270,930,1030,1130]}.get(nm, [150,1050])
        for cx in pos:
            s.append(_minaret(cx, base, 420 if p == "ottoman" else 360, 22, sil, mstyle, gold))
    elif p == "marocain":
        s.append(f'<rect x="300" y="{base-130}" width="620" height="130" fill="{sil}"/>')
        for i in range(6):
            x = 330 + i * 96
            s.append(f'<path d="M {x} {base} L {x} {base-70} Q {x+30} {base-112} {x+60} {base-70} L {x+60} {base} Z" fill="{ground}" opacity="0.9"/>')
        s.append(f'<path d="M 300 {base-130} L 920 {base-130} L 920 {base-150} L 300 {base-150} Z" fill="{gold}" opacity="0.6"/>')
        s.append(_minaret(600, base, 470, 74, sil, "carre", gold))
        s.append(f'<rect x="566" y="{base-330}" width="68" height="60" fill="{gold}" opacity="0.35"/>')
        if art.get("mer"):
            s.append(f'<rect x="0" y="{base}" width="{W}" height="60" fill="{ground}" opacity="0.6"/>')
    elif p == "arcade":
        for row, (y0, hh, op) in enumerate([(base, 130, 0.95), (base-130, 110, 0.8)]):
            for i in range(11):
                x = 90 + i * 96
                col = "#b8493f" if (i + row) % 2 == 0 else "#e8ddc8"
                s.append(f'<path d="M {x} {y0} L {x} {y0-hh+34} A 34 34 0 0 1 {x+68} {y0-hh+34} L {x+68} {y0} Z" fill="none" stroke="{col}" stroke-width="9" opacity="{op}"/>')
        s.append(_minaret(600, base - 240, 250, 60, sil, "carre", gold))
    elif p == "banco":
        s.append(f'<path d="M 200 {base} L 220 {base-190} L 1000 {base-190} L 1020 {base} Z" fill="{sil}"/>')
        for cx in (330, 600, 870):
            s.append(f'<path d="M {cx-52} {base-190} L {cx-38} {base-370} Q {cx} {base-400} {cx+38} {base-370} L {cx+52} {base-190} Z" fill="{sil}"/>')
            s.append(f'<ellipse cx="{cx}" cy="{base-392}" rx="9" ry="12" fill="#f2e6c8"/>')
            for ty in range(4):
                y = base - 350 + ty * 42
                s.append(f'<line x1="{cx-30}" y1="{y}" x2="{cx-46}" y2="{y}" stroke="{ground}" stroke-width="5"/>')
                s.append(f'<line x1="{cx+30}" y1="{y}" x2="{cx+46}" y2="{y}" stroke="{ground}" stroke-width="5"/>')
        for i in range(14):
            x = 245 + i * 55
            s.append(f'<path d="M {x} {base-190} L {x+9} {base-225} L {x+18} {base-190} Z" fill="{sil}"/>')
    elif p == "tente":
        s.append(f'<path d="M 350 {base} L 600 {base-330} L 850 {base} Z" fill="{sil}"/>')
        s.append(f'<path d="M 440 {base} L 600 {base-330} L 760 {base} Z" fill="#f0ead9" opacity="0.22"/>')
        s.append(f'<path d="M 560 {base} L 600 {base-330} L 640 {base} Z" fill="{gold}" opacity="0.5"/>')
        for cx in (250, 330, 870, 950):
            s.append(f'<path d="M {cx-9} {base} L {cx-4} {base-390} L {cx} {base-420} L {cx+4} {base-390} L {cx+9} {base} Z" fill="{sil}"/>')
    elif p == "spirale":
        s.append(f'<rect x="280" y="{base-170}" width="640" height="170" fill="{sil}"/>')
        for i in range(8):
            x = 306 + i * 76
            s.append(f'<path d="M {x} {base-170} l 22 -26 l 22 26 Z" fill="{sil}"/>')
        s.append(_dome(760, base - 170, 80, 90, art.get("dome_couleur", sil), gold))
        cx, ty = 430, base - 470
        s.append(f'<path d="M {cx-58} {base} L {cx-30} {ty} L {cx+30} {ty} L {cx+58} {base} Z" fill="{sil}"/>')
        for i in range(6):  # rampe hélicoïdale
            y = base - 60 - i * 66
            wl = 56 - i * 7.5
            s.append(f'<path d="M {cx-wl} {y} Q {cx} {y-24} {cx+wl-8} {y-34}" fill="none" stroke="{gold}" stroke-width="5" opacity="0.85"/>')
        s.append(f'<rect x="{cx-16}" y="{ty-34}" width="32" height="34" fill="{sil}"/>')
    elif p == "forteresse":
        s.append(f'<rect x="240" y="{base-170}" width="720" height="170" fill="{sil}"/>')
        for i in range(9):
            x = 262 + i * 78
            s.append(f'<rect x="{x}" y="{base-196}" width="40" height="26" fill="{sil}"/>')
        for cx in (320, 560, 800):  # contreforts
            s.append(f'<path d="M {cx-24} {base} L {cx-12} {base-170} L {cx+12} {base-170} L {cx+24} {base} Z" fill="{ground}" opacity="0.8"/>')
        s.append(_dome(880, base - 170, 62, 66, art.get("dome_couleur", "#e8e0cf"), gold))
        cx = 360; s.append(f'<rect x="{cx-46}" y="{base-470}" width="92" height="300" fill="{sil}"/>')
        s.append(f'<rect x="{cx-34}" y="{base-540}" width="68" height="70" fill="{sil}"/>')
        s.append(_dome(cx, base - 540, 30, 34, art.get("dome_couleur", "#e8e0cf"), gold))
    elif p == "persan":
        gd = art.get("grand_dome")
        s.append(f'<rect x="330" y="{base-190}" width="540" height="190" fill="{sil}"/>')
        # iwan : grand portail
        s.append(f'<path d="M 500 {base} L 500 {base-260} Q 600 {base-330} 700 {base-260} L 700 {base} Z" fill="{sil}"/>')
        s.append(f'<path d="M 528 {base} L 528 {base-240} Q 600 {base-296} 672 {base-240} L 672 {base} Z" fill="{ground}"/>')
        s.append(f'<path d="M 552 {base} L 552 {base-216} Q 600 {base-262} 648 {base-216} L 648 {base} Z" fill="{gold}" opacity="0.4"/>')
        rw = 170 if gd else 130
        s.append(_dome(600, base - 250 if gd else base - 190, rw, rw * 0.92, art.get("dome_couleur", sil), gold))
        if art.get("vitraux"):
            for i, c in enumerate(("#d84f6a", "#e8a04f", "#4f8ad8", "#5fb87a", "#b85fd8")):
                x = 356 + i * 42
                s.append(f'<path d="M {x} {base-40} L {x} {base-120} Q {x+15} {base-140} {x+30} {base-120} L {x+30} {base-40} Z" fill="{c}" opacity="0.9"/>')
    elif p == "pagode":
        s.append(f'<rect x="300" y="{base-120}" width="600" height="120" fill="{sil}"/>')
        s.append(f'<path d="M 270 {base-120} Q 600 {base-165} 930 {base-120} L 900 {base-150} Q 600 {base-192} 300 {base-150} Z" fill="{sil}"/>')
        cx = 600
        for i in range(3):  # pagode octogonale à 3 niveaux
            y = base - 190 - i * 95
            w2 = 120 - i * 26
            s.append(f'<rect x="{cx-w2/2}" y="{y-58}" width="{w2}" height="58" fill="{sil}"/>')
            s.append(f'<path d="M {cx-w2/2-34} {y-58} Q {cx} {y-88} {cx+w2/2+34} {y-58} L {cx+w2/2+14} {y-80} Q {cx} {y-104} {cx-w2/2-14} {y-80} Z" fill="{sil}"/>')
        s.append(f'<line x1="{cx}" y1="{base-482}" x2="{cx}" y2="{base-514}" stroke="{gold}" stroke-width="4"/>')
        s.append(f'<circle cx="{cx}" cy="{base-518}" r="6" fill="{gold}"/>')
    return "".join(s)

# ---------------------------------------------------------------- scènes
def scene(art, mode="hero"):
    c1, c2, c3 = art["ciel"]
    if mode == "nuit":
        c1, c2, c3 = "#0a1026", "#152046", "#2b3a6b"
    elif mode == "aube":
        c1, c2, c3 = "#2b2340", "#8a5a6a", "#f2c98f"
    sil = "#12141c" if mode != "aube" else "#1c1826"
    ground = "#0c0e14"
    gold = "#d8b45a"
    sky_extra = _stars(hash(art["profil"]) % 999) + (_moon() if mode == "nuit" else "")
    if mode == "hero":
        sky_extra = _stars(hash(art["profil"]) % 999, 30, 220) + _sun(960, 210, 50, c3)
    if mode == "aube":
        sky_extra = _sun(240, 250, 62, "#f6d9a0")
    mer = ""
    if art.get("mer"):
        mer = (f'<rect x="0" y="580" width="{W}" height="120" fill="{c2}" opacity="0.45"/>'
               f'<g opacity="0.35">' + "".join(
                   f'<line x1="{80+i*140}" y1="{600+ (i%3)*24}" x2="{170+i*140}" y2="{600+(i%3)*24}" stroke="#f2e6c8" stroke-width="2"/>'
                   for i in range(8)) + "</g>")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{c1}"/><stop offset="0.62" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/>
</linearGradient>
{_pattern_def("g1", 120, "#e8d9a8", 0.10)}
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#g1)"/>
{sky_extra}
{_profil(art["art"] if "art" in art else art, sil, ground, gold)}
<rect x="0" y="560" width="{W}" height="140" fill="{ground}"/>
{mer}
<rect x="0" y="556" width="{W}" height="4" fill="{gold}" opacity="0.55"/>
</svg>'''

def medaillon(art):
    """Détail : médaillon géométrique aux couleurs de la mosquée."""
    c1, c2, c3 = art["ciel"]
    rings = []
    for i, (r, col, sw) in enumerate([(300, "#d8b45a", 3), (255, c3, 2), (210, "#d8b45a", 2)]):
        rings.append(f'<circle cx="600" cy="350" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="0.8"/>')
    rays = []
    for i in range(16):
        a = math.pi / 8 * i
        rr = 300 if i % 2 == 0 else 170
        rays.append(f"{600 + rr*math.cos(a):.0f},{350 + rr*math.sin(a):.0f}")
    star = f'<polygon points="{" ".join(rays)}" fill="{c2}" stroke="#d8b45a" stroke-width="3" opacity="0.92"/>'
    inner = []
    for i in range(8):
        a = math.pi / 4 * i + math.pi / 8
        inner.append(f'<circle cx="{600 + 118*math.cos(a):.0f}" cy="{350 + 118*math.sin(a):.0f}" r="16" fill="#d8b45a" opacity="0.85"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" role="img">
<defs><radialGradient id="bg" cx="0.5" cy="0.5" r="0.75">
<stop offset="0" stop-color="{c2}"/><stop offset="1" stop-color="{c1}"/></radialGradient>
{_pattern_def("g2", 100, "#e8d9a8", 0.08)}</defs>
<rect width="1200" height="700" fill="url(#bg)"/><rect width="1200" height="700" fill="url(#g2)"/>
{"".join(rings)}{star}
<circle cx="600" cy="350" r="92" fill="{c1}" stroke="#d8b45a" stroke-width="3"/>
{"".join(inner)}
<circle cx="600" cy="350" r="34" fill="#d8b45a"/>
</svg>'''

def motif(art):
    c1, c2, _ = art["ciel"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" role="img">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
{_pattern_def("g3", 175, "#d8b45a", 0.9)}</defs>
<rect width="1200" height="700" fill="url(#bg)"/>
<rect width="1200" height="700" fill="url(#g3)"/>
</svg>'''
