import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random, io

# ---------- Page setup ----------
st.set_page_config(page_title="Week 4 • Arts & Advanced Big Data", layout="wide")

# ---------- Blob function ----------
def layered_blob(xc, yc, base_r=1.0, wobble=0.25, spikes=150):
    ang = np.linspace(0, 2*np.pi, spikes)
    r = base_r * (1 + wobble * np.random.randn(spikes))
    x = xc + r * np.cos(ang)
    y = yc + r * np.sin(ang)
    return x, y

# ---------- Color palettes ----------
def pastel_palette():
    return [
        (0.95, 0.75, 0.75),
        (0.98, 0.85, 0.60),
        (0.85, 0.80, 0.95),
        (0.95, 0.90, 0.65),
        (0.75, 0.60, 0.90),
        (0.90, 0.70, 0.75),
    ]

def vivid_palette():
    return [
        (0.9, 0.4, 0.4),
        (1.0, 0.7, 0.3),
        (0.7, 0.6, 1.0),
        (0.5, 0.8, 0.5),
        (0.8, 0.3, 0.8),
        (0.3, 0.7, 1.0),
    ]

# ---------- Generate Poster ----------
def generate_poster(style, layers, palette_size, wobble, lx, ly, seed=None, edge=True, edge_color=(0, 0, 0, 0.3)):
    if seed:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 9))
    ax.axis("off")
    ax.set_facecolor((0.97, 0.97, 0.95))

    palette = pastel_palette() if style == "Pastel" else vivid_palette()
    palette = palette[:palette_size]

    for i in range(layers):
        color = random.choice(palette)
        cx = random.uniform(-3, 3)
        cy = random.uniform(-3, 3)
        r = random.uniform(1.2, 3.0)
        x, y = layered_blob(cx, cy, base_r=r, wobble=wobble)

        # simulate depth shading by light source
        intensity = 0.8 - 0.4 * np.hypot(cx - lx * 4, cy - ly * 4) / 5
        shaded = tuple(np.clip(np.array(color) * intensity, 0, 1)) + (0.85,)

        # glow / soft shadow
        ax.fill(x, y, color=shaded, lw=0.5, ec=edge_color if edge else None, zorder=i)
        ax.fill(x*0.97, y*0.97, color=(0, 0, 0, 0.08), lw=0)

    # Title text
    ax.text(0, 7.5, "Generative Poster", fontsize=28, weight="bold", color=(0.3, 0.3, 0.3), ha="center")
    ax.text(0, 6.9, "Week 4 • Arts & Advanced Big Data", fontsize=14, color=(0.6, 0.6, 0.6), ha="center")
    ax.text(0, -6.8, "3D-like • glow & depth edition", fontsize=10, color=(0.6, 0.6, 0.6), ha="center", style="italic")

    ax.set_xlim(-7, 7)
    ax.set_ylim(-8, 8)
    return fig


# ---------- Sidebar Controls ----------
with st.sidebar:
    st.header("🎨 Poster Settings")

    style = st.selectbox("Palette Style", ["Pastel", "Vivid"])
    layers = st.slider("Number of Layers", 5, 40, 20)
    palette_size = st.slider("Palette Size", 3, 6, 6)
    wobble = st.slider("Wobble Intensity", 0.05, 0.3, 0.15)
    lx = st.slider("Light Source X", 0.0, 1.0, 0.1)
    ly = st.slider("Light Source Y", 0.0, 1.0, 0.9)
    seed = st.number_input("Random Seed", min_value=0, step=1, value=0)
    
    st.subheader("Edge Mode")
    edge_option = st.radio("", ["Use Color", "No Edge"], index=0)
    edge_color = st.color_picker("Edge Color", "#555555")

    generate = st.button("🎨 Generate Poster")

# ---------- Main Layout ----------
st.title("✨ Interactive 3D Generative Poster")
st.write("Generate a poster with **distinct palette styles, lighting, gradient, and shadow effects.**")

# ---------- Generate Poster ----------
if generate:
    edge_bool = edge_option == "Use Color"
    ec_rgba = tuple(int(edge_color.lstrip("#")[i:i+2], 16)/255 for i in (0, 2, 4)) + (0.35,)
    fig = generate_poster(style, layers, palette_size, wobble, lx, ly,
                          seed if seed != 0 else None, edge=edge_bool, edge_color=ec_rgba)
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster (PNG)",
                       data=buf.getvalue(),
                       file_name="Week4_3DGenerativePoster.png",
                       mime="image/png")
else:
    st.info("Adjust the sliders and click **Generate Poster** to create your artwork.")
