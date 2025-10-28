import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import io
from colorsys import hsv_to_rgb

# ---------------------------------------
# Page config
# ---------------------------------------
st.set_page_config(page_title="Generative Poster v3", layout="wide")
st.title("Generative Abstract Poster v3")
st.markdown("**Interactive - Arts & Advanced Big Data**  \nAuto-refresh + Randomize button - Palette & Background themes")

# ---------------------------------------
# Palette utilities
# ---------------------------------------
def clamp01(x):
    return max(0.0, min(1.0, x))

def pastel_palette(k=6):
    cols = []
    for _ in range(k):
        r = random.uniform(0.65, 0.95)
        g = random.uniform(0.65, 0.95)
        b = random.uniform(0.65, 0.95)
        cols.append((r, g, b))
    return cols

def vibrant_palette(k=6):
    anchors = [
        (0.95, 0.30, 0.30),  # red
        (1.00, 0.65, 0.00),  # orange
        (0.20, 0.70, 0.30),  # green
        (0.20, 0.40, 0.95),  # blue
        (0.65, 0.25, 0.90),  # purple
        (0.95, 0.20, 0.60),  # magenta
    ]
    cols = []
    for i in range(k):
        r, g, b = anchors[i % len(anchors)]
        cols.append((clamp01(r + random.uniform(-0.05, 0.05)),
                     clamp01(g + random.uniform(-0.05, 0.05)),
                     clamp01(b + random.uniform(-0.05, 0.05))))
    return cols

def mono_palette(k=6):
    h = random.random()
    base = np.linspace(0.35, 0.95, k)
    cols = []
    for v in base:
        r, g, b = hsv_to_rgb(h, 0.4, v)
        cols.append((r, g, b))
    return cols

def random_palette(k=6):
    return [(random.random(), random.random(), random.random()) for _ in range(k)]

def pink_palette(k=6):
    cols = []
    for _ in range(k):
        r = random.uniform(0.9, 1.0)
        g = random.uniform(0.4, 0.75)
        b = random.uniform(0.6, 0.9)
        cols.append((r, g, b))
    return cols

def blue_palette(k=6):
    cols = []
    for _ in range(k):
        r = random.uniform(0.2, 0.5)
        g = random.uniform(0.4, 0.8)
        b = random.uniform(0.7, 1.0)
        cols.append((r, g, b))
    return cols

def green_palette(k=6):
    cols = []
    for _ in range(k):
        r = random.uniform(0.2, 0.5)
        g = random.uniform(0.6, 1.0)
        b = random.uniform(0.3, 0.7)
        cols.append((r, g, b))
    return cols

def get_palette(kind, k=6):
    if kind == "Pastel":
        return pastel_palette(k)
    if kind == "Vibrant":
        return vibrant_palette(k)
    if kind == "Mono":
        return mono_palette(k)
    if kind == "Random":
        return random_palette(k)
    if kind == "Pink":
        return pink_palette(k)
    if kind == "Blue":
        return blue_palette(k)
    if kind == "Green":
        return green_palette(k)
    return pastel_palette(k)

# ---------------------------------------
# Shapes
# ---------------------------------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def polygon(center=(0.5, 0.5), sides=6, r=0.3, wobble=0.1):
    angles = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(sides) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return np.append(x, x[0]), np.append(y, y[0])

def waves(center=(0.5, 0.5), r=0.3, points=400, frequency=6, wobble=0.05):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * np.sin(frequency * angles))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def rings(center=(0.5, 0.5), base_r=0.3, count=4, wobble=0.1):
    coords = []
    for i in range(count):
        r = base_r * (0.5 + i * 0.4)
        x, y = blob(center, r, 200, wobble)
        coords.append((x, y))
    return coords

# ---------------------------------------
# Backgrounds
# ---------------------------------------
def set_background(ax, bg_mode):
    if bg_mode == "Off-white":
        ax.set_facecolor((0.98, 0.98, 0.97))
        return "dark"
    if bg_mode == "Light gray":
        ax.set_facecolor((0.92, 0.92, 0.92))
        return "dark"
    if bg_mode == "Dark":
        ax.set_facecolor((0.08, 0.08, 0.08))
        return "light"
    if bg_mode == "Gradient":
        gradient = np.linspace(0.95, 0.75, 512).reshape(-1, 1)
        grad_img = np.dstack([gradient, gradient, gradient])
        ax.imshow(grad_img, extent=[0, 1, 0, 1], origin="lower", zorder=-10)
        ax.set_facecolor((1, 1, 1, 0))
        return "dark"
    ax.set_facecolor((1, 1, 1))
    return "dark"

# ---------------------------------------
# Draw poster
# ---------------------------------------
def draw_poster(shape_type="Blob", n_layers=8, wobble=0.15, palette_kind="Pastel", bg_mode="Off-white", seed=None):
    if seed not in (None, "", 0):
        try:
            seed = int(seed)
            random.seed(seed)
            np.random.seed(seed)
        except:
            pass

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis("off")

    text_color_mode = set_background(ax, bg_mode)
    cols = get_palette(palette_kind, 6)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        color = random.choice(cols)
        alpha = random.uniform(0.25, 0.6)

        if shape_type == "Blob":
            x, y = blob((cx, cy), rr, wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))
        elif shape_type == "Polygon":
            x, y = polygon((cx, cy), sides=random.randint(3, 8), r=rr, wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))
        elif shape_type == "Waves":
            x, y = waves((cx, cy), rr, frequency=random.randint(4, 8), wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))
        elif shape_type == "Rings":
            for x, y in rings((cx, cy), rr, count=random.randint(2, 4), wobble=wobble):
                ax.plot(x, y, color=color, alpha=alpha, lw=2)

    txt_color = (0.95, 0.95, 0.95) if text_color_mode == "light" else (0.1, 0.1, 0.1)
    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight="bold", transform=ax.transAxes, color=txt_color)
    ax.text(0.05, 0.91, "Interactive - Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes, color=txt_color)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# ---------------------------------------
# Sidebar controls
# ---------------------------------------
with st.sidebar:
    st.header("Controls")
    shape = st.selectbox("Shape Type", ["Blob", "Polygon", "Waves", "Rings"])
    layers = st.slider("Number of Layers", 1, 20, 8, 1)
    wobble = st.slider("Wobble Intensity", 0.01, 0.5, 0.15, 0.01)
    palette_kind = st.selectbox("Palette", ["Pastel", "Vibrant", "Mono", "Random", "Pink", "Blue", "Green"])
    bg_mode = st.selectbox("Background", ["Off-white", "Light gray", "Dark", "Gradient"])
    seed_in = st.text_input("Seed (optional, int)", value="")
    if "reroll" not in st.session_state:
        st.session_state.reroll = 0
    if st.button("Generate Random Poster"):
        st.session_state.reroll += 1

if seed_in.strip() == "":
    effective_seed = st.session_state.reroll if st.session_state.reroll > 0 else None
else:
    try:
        base = int(seed_in)
    except:
        base = None
    effective_seed = None if base is None else base + st.session_state.reroll

# ---------------------------------------
# Layout & render
# ---------------------------------------
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### Basic Functions")
    st.markdown("""
- Auto-refresh when any control changes  
- Randomize with the button for a fresh composition  
- Palette: Pastel / Vibrant / Mono / Random / Pink / Blue / Green  
- Background: Off-white / Light gray / Dark / Gradient  
- Shapes: Blob / Polygon / Waves / Rings  
- Download the result as PNG
""")

with col_right:
    fig = draw_poster(shape, layers, wobble, palette_kind, bg_mode, seed=effective_seed)
    st.pyplot(fig, use_container_width=True)

# ---------------------------------------
# Download section
# ---------------------------------------
png_bytes = io.BytesIO()
fig.savefig(png_bytes, format="png", dpi=300, bbox_inches="tight")
st.download_button(
    "Download Poster as PNG",
    data=png_bytes.getvalue(),
    file_name="poster.png",
    mime="image/png",
)

st.markdown("---")
st.caption(f"Palette: {palette_kind} | Background: {bg_mode} | Shape: {shape} | Layers: {layers} | Wobble: {wobble:.2f} | Reroll: {st.session_state.reroll}")
