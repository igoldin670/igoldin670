"""Original profile artwork. Run after installing requirements-assets.txt."""

import re
from html import escape
from pathlib import Path

import cairosvg

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def svg(width, height, title, body, animated=False):
    style = (
        """<style>
.signal { animation: travel 6s linear infinite; }
@keyframes travel { from { stroke-dashoffset: 0; } to { stroke-dashoffset: -100; } }
@media (prefers-reduced-motion: reduce) { .signal { animation: none; stroke-dasharray: none; opacity: .5; } }
</style>"""
        if animated
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(title)}. Original illustration for Isaac Goldin's GitHub profile.</desc>
<defs><linearGradient id="background" x2="1" y2="1"><stop stop-color="#0b1221"/><stop offset="1" stop-color="#192941"/></linearGradient><linearGradient id="accent"><stop stop-color="#5eead4"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>
{style}<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="22" fill="url(#background)" stroke="#33435b"/>
<g font-family="Arial,Helvetica,sans-serif">{body}</g></svg>\n'''


def text(x, y, value, size=20, color="#cbd5e1", weight=400, spacing=0, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}">{escape(value)}</text>'


def hero(mobile=False):
    width, height = (560, 300) if mobile else (1120, 310)
    if mobile:
        points = [(405, 190), (475, 180), (520, 225), (455, 270), (380, 255)]
        body = text(32, 47, "BUILD · MEASURE · EXPLAIN", 12, "#5eead4", 700, 2)
        body += text(29, 113, "Isaac Goldin", 52, "#f1f5f9", 700)
        body += text(32, 157, "From the math to the model.", 24)
        body += text(32, 215, "LANGUAGE MODELS", 12, "#a5b4cc", spacing=1.1)
        body += text(32, 239, "RECOMMENDERS · APPLIED ML", 12, "#a5b4cc", spacing=1.1)
    else:
        points = [
            (798, 80),
            (930, 49),
            (1050, 110),
            (913, 165),
            (1040, 259),
            (794, 251),
        ]
        body = text(60, 60, "BUILD · MEASURE · EXPLAIN", 14, "#5eead4", 700, 3)
        body += text(55, 146, "Isaac Goldin", 76, "#f1f5f9", 700)
        body += text(60, 200, "From the math to the model.", 32)
        body += text(
            60,
            258,
            "LANGUAGE MODELS  /  RECOMMENDERS  /  APPLIED ML",
            15,
            "#a5b4cc",
            spacing=1,
        )
    path = "M" + "L".join(f"{x},{y}" for x, y in points) + "Z"
    body += f'<path d="{path}" fill="none" stroke="#7486aa" stroke-width="1.5" opacity=".38"/>'
    body += f'<path d="M{points[0][0]},{points[0][1]}L{points[3][0]},{points[3][1]}L{points[1][0]},{points[1][1]}" fill="none" stroke="#7486aa" opacity=".3"/>'
    body += f'<path class="signal" d="{path}" pathLength="100" fill="none" stroke="#5eead4" stroke-width="2.8" stroke-dasharray="12 88" stroke-dashoffset="0" stroke-linecap="round"/>'
    for i, (x, y) in enumerate(points):
        body += f'<circle cx="{x}" cy="{y}" r="{7 if i == 3 else 5}" fill="{"#5eead4" if i % 2 == 0 else "#a78bfa"}"/>'
    body += f'<path d="M28,{height - 3}H{width - 28}" stroke="url(#accent)" stroke-width="3"/>'
    return svg(width, height, "Isaac Goldin. From the math to the model.", body, True)


def workflow(label, stages, mobile=False, loop=False):
    width, height = (560, 370) if mobile else (1120, 238 if loop else 198)
    body = text(32 if mobile else 40, 34, label, 12, "#94a3b8", 700, 2)
    for i, (title, detail) in enumerate(stages):
        color = ["#5eead4", "#a78bfa", "#5eead4"][i]
        x, y, w, h = (
            (32, 52 + i * 103, 496, 78) if mobile else (40 + i * 364, 59, 312, 95)
        )
        body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#121f32" stroke="{color}" stroke-opacity=".65"/>'
        body += text(
            x + w / 2, y + 33, title, 24 if mobile else 25, color, 700, anchor="middle"
        )
        body += text(x + w / 2, y + 59, detail, 18, anchor="middle")
        if i < 2:
            if mobile:
                cy = y + h + 9
                body += f'<path d="M280,{cy}v10m-4,-4l4,4l4,-4" fill="none" stroke="#8293ad" stroke-width="2"/>'
            else:
                sx = x + w + 12
                body += f'<path d="M{sx},106h27m-6,-5l6,5l-6,5" fill="none" stroke="#8293ad" stroke-width="2"/>'
    if loop and not mobile:
        body += '<path d="M924,165v18H196v-18m-5,6l5,-6l5,6" fill="none" stroke="#5eead4" stroke-opacity=".7" stroke-width="1.7"/>'
        body += text(
            560,
            214,
            "Fresh student responses after each update",
            16,
            "#94a3b8",
            anchor="middle",
        )
    return svg(width, height, " → ".join(s[0] for s in stages), body)


def main():
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        banner = hero(mobile)
        (ASSETS / f"banner{suffix}.svg").write_text(banner)
        # Export an intentional still frame for reduced-motion picture sources.
        still = re.sub(r"<style>.*?</style>", "", banner, flags=re.S)
        cairosvg.svg2png(
            bytestring=still.encode(),
            write_to=str(ASSETS / f"banner{suffix}-static.png"),
        )
    illustrations = [
        (
            "distillation",
            "01 / LANGUAGE MODEL RESEARCH",
            [
                ("Sample", "Student writes a response"),
                ("Score", "Frozen teacher gives guidance"),
                ("Update", "Only the student learns"),
            ],
            True,
        ),
        (
            "music",
            "02 / RECOMMENDATION SYSTEMS",
            [
                ("Listening events", "Clean + build interactions"),
                ("ALS", "Learn user and song factors"),
                ("Top-10 songs", "Evaluate ranking quality"),
            ],
            False,
        ),
        (
            "calorie",
            "03 / APPLIED MACHINE LEARNING",
            [
                ("User inputs", "Prepare useful features"),
                ("Model pipeline", "Train + save the estimator"),
                ("Streamlit app", "Explore calorie estimates"),
            ],
            False,
        ),
    ]
    for name, label, stages, loop in illustrations:
        for mobile in (False, True):
            (ASSETS / f"{name}{'-mobile' if mobile else ''}.svg").write_text(
                workflow(label, stages, mobile, loop)
            )
    print("Rendered 8 original SVGs and 2 static PNG alternatives.")


if __name__ == "__main__":
    main()
