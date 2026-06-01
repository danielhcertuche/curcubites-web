import json
import os
from pathlib import Path
from urllib.parse import quote

import streamlit as st


BASE_DIR = Path(__file__).parent
PRODUCTS_PATH = BASE_DIR / "data" / "products.json"
DEFAULT_EMAIL = "ventas@curcubites.com"


st.set_page_config(
    page_title="Curcubites — Chips de plátano horneados",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── helpers ────────────────────────────────────────────────────────────────

def money(value: int) -> str:
    return f"${value:,.0f}".replace(",", ".")


@st.cache_data
def load_products() -> list[dict]:
    with PRODUCTS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return os.getenv(name, default)


def ensure_cart() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = {}


def add_to_cart(product_id: str, qty: int = 1) -> None:
    ensure_cart()
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + qty


def remove_from_cart(product_id: str) -> None:
    ensure_cart()
    st.session_state.cart.pop(product_id, None)


def update_quantity(product_id: str, qty: int) -> None:
    ensure_cart()
    if qty <= 0:
        remove_from_cart(product_id)
    else:
        st.session_state.cart[product_id] = qty


def cart_items(products: list[dict]) -> list[dict]:
    ensure_cart()
    by_id = {p["id"]: p for p in products}
    return [
        {**by_id[pid], "qty": qty, "subtotal": int(by_id[pid]["price"]) * qty}
        for pid, qty in st.session_state.cart.items()
        if pid in by_id
    ]


def cart_total(items: list[dict]) -> int:
    return sum(i["subtotal"] for i in items)


def order_message(
    items: list[dict], name: str, phone: str, city: str, address: str, notes: str
) -> str:
    lines = [
        "Hola, quiero hacer un pedido de Curcubites 🌿",
        "",
        *[f"- {i['qty']} x {i['name']} = {money(i['subtotal'])}" for i in items],
        "",
        f"Total: {money(cart_total(items))}",
        "",
        f"Nombre: {name}",
        f"Teléfono / WhatsApp: {phone}",
        f"Ciudad: {city}",
        f"Dirección: {address}",
    ]
    if notes:
        lines.append(f"Notas: {notes}")
    return "\n".join(lines)


def whatsapp_url(message: str) -> str:
    number = get_secret("WHATSAPP_NUMBER", "").strip().replace("+", "")
    base = f"https://wa.me/{number}" if number else "https://wa.me/"
    return f"{base}?text={quote(message)}"


def mailto_url(message: str) -> str:
    email = get_secret("ORDER_EMAIL", DEFAULT_EMAIL)
    return f"mailto:{email}?subject={quote('Pedido Curcubites')}&body={quote(message)}"


# ─── styles ─────────────────────────────────────────────────────────────────

def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

        :root {
          --verde:        #245C2A;
          --verde-hover:  #1a4320;
          --verde-mid:    #3A7A41;
          --curcuma:      #C4871A;
          --terracota:    #A85232;
          --crema:        #FFF6E6;
          --crema-2:      #F5EDD8;
          --dark:         #0F1A0C;
          --negro:        #151A12;
          --gris:         #4a5048;   /* 6.2:1 on cream — WCAG AA ✓ */
          --verde-suave:  #E7F1DF;
          --linea:        #E0D5C0;
          --linea-dark:   #2a3827;
        }

        html, body, [class*="css"] {
          font-family: 'Inter', system-ui, sans-serif;
        }

        /* ── app background ── */
        .stApp { background: var(--crema); }

        /* ── block container ── */
        [data-testid="stMainBlockContainer"] {
          max-width: 1320px;
          padding: 0 2rem 5rem !important;
        }

        /* ─────────────────────────────────────────
           SIDEBAR
        ───────────────────────────────────────── */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div {
          background: var(--dark) !important;
        }

        [data-testid="stSidebar"] * {
          color: #FFF6E6 !important;
        }

        /* sidebar number input — dark fill, light text */
        [data-testid="stSidebar"] [data-baseweb="input"] {
          background: rgba(255,255,255,0.10) !important;
          border: 1px solid rgba(255,255,255,0.18) !important;
          border-radius: 8px !important;
        }

        [data-testid="stSidebar"] [data-baseweb="input"] input {
          background: transparent !important;
          color: #FFF6E6 !important;
          caret-color: #FFF6E6;
        }

        /* sidebar spinner +/- buttons */
        [data-testid="stSidebar"] [data-baseweb="input"] button {
          background: transparent !important;
          color: rgba(255,246,230,0.7) !important;
          border: none !important;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] > button {
          background: rgba(255,255,255,0.08) !important;
          border: 1px solid rgba(255,255,255,0.16) !important;
          color: #FFF6E6 !important;
          font-weight: 600 !important;
          border-radius: 8px !important;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
          background: rgba(255,255,255,0.15) !important;
        }

        /* ─────────────────────────────────────────
           HERO CARD
        ───────────────────────────────────────── */
        .hero-card {
          background: var(--dark);
          border-radius: 24px;
          padding: 4.5rem 3rem 3.5rem;
          text-align: center;
          margin-bottom: 0.25rem;
        }

        .hero-eyebrow {
          display: inline-block;
          background: rgba(255,255,255,0.09);
          border: 1px solid rgba(255,255,255,0.14);
          color: rgba(255,246,230,0.7);
          font-size: 0.74rem;
          font-weight: 600;
          letter-spacing: 2px;
          text-transform: uppercase;
          padding: 0.32rem 1rem;
          border-radius: 999px;
          margin-bottom: 1.3rem;
        }

        .hero-h1 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(3.8rem, 10vw, 7rem);
          font-weight: 900;
          line-height: 0.9;
          color: #FFF6E6;
          letter-spacing: -2px;
          margin: 0 0 1.3rem;
        }

        .hero-claim {
          color: rgba(255,246,230,0.65);
          font-size: 1.08rem;
          line-height: 1.65;
          max-width: 480px;
          margin: 0 auto 1.6rem;
        }

        .hero-pill-row {
          display: flex;
          justify-content: center;
          flex-wrap: wrap;
          gap: 0.45rem;
          margin-bottom: 2rem;
        }

        .hero-pill {
          border: 1px solid rgba(255,255,255,0.18);
          border-radius: 999px;
          padding: 0.28rem 0.85rem;
          font-size: 0.8rem;
          font-weight: 600;
          color: rgba(255,246,230,0.82);
          background: rgba(255,255,255,0.06);
        }

        .hero-cta {
          display: inline-block;
          background: var(--verde);
          color: #FFF6E6 !important;
          text-decoration: none !important;
          padding: 0.9rem 2.4rem;
          border-radius: 999px;
          font-weight: 800;
          font-size: 0.95rem;
          letter-spacing: 0.3px;
        }

        .hero-cta:hover { background: var(--verde-mid); }

        /* ─────────────────────────────────────────
           TRUST STRIP
        ───────────────────────────────────────── */
        .trust-strip {
          display: flex;
          justify-content: center;
          flex-wrap: wrap;
          background: var(--crema-2);
          border: 1px solid var(--linea);
          border-top: none;
          border-radius: 0 0 20px 20px;
          overflow: hidden;
          margin-bottom: 3rem;
        }

        .trust-item {
          display: flex;
          align-items: center;
          gap: 0.45rem;
          padding: 0.8rem 1.4rem;
          font-size: 0.83rem;
          font-weight: 600;
          color: var(--negro);
          border-right: 1px solid var(--linea);
          white-space: nowrap;
        }

        .trust-item:last-child { border-right: none; }

        /* ─────────────────────────────────────────
           SECTION HEADINGS
        ───────────────────────────────────────── */
        .section-tag {
          display: block;
          font-size: 0.72rem;
          font-weight: 700;
          letter-spacing: 2px;
          text-transform: uppercase;
          color: var(--verde);
          margin-bottom: 0.4rem;
        }

        .section-h2 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(2.1rem, 5vw, 3rem);
          font-weight: 800;
          color: var(--negro);
          line-height: 1.05;
          letter-spacing: -0.5px;
          margin: 0 0 0.45rem;
        }

        .section-copy {
          color: var(--gris);
          font-size: 0.96rem;
          margin-bottom: 1.8rem;
        }

        /* ─────────────────────────────────────────
           PRODUCT TABS  (st.tabs pill override)
        ───────────────────────────────────────── */
        div[data-baseweb="tab-list"] {
          background: transparent !important;
          gap: 0.45rem;
          border-bottom: none !important;
          padding-bottom: 0 !important;
          margin-bottom: 1.5rem;
        }

        button[data-baseweb="tab"] {
          background: rgba(255,255,255,0.85) !important;
          border: 1.5px solid var(--linea) !important;
          border-radius: 999px !important;
          padding: 0.52rem 1.4rem !important;
          font-weight: 700 !important;
          font-size: 0.88rem !important;
          color: var(--negro) !important;
          transition: all 0.15s !important;
          outline: none !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
          background: var(--negro) !important;
          border-color: var(--negro) !important;
          color: #FFF6E6 !important;
        }

        button[data-baseweb="tab"]:hover:not([aria-selected="true"]) {
          border-color: var(--verde) !important;
          color: var(--verde) !important;
        }

        div[data-baseweb="tab-highlight"] { display: none !important; }
        div[data-baseweb="tab-border"]    { display: none !important; }
        div[data-baseweb="tab-panel"]     { padding: 0 !important; }

        /* ── product detail ── */
        .flavor-tag-badge {
          display: inline-block;
          font-size: 0.68rem;
          font-weight: 900;
          letter-spacing: 3px;
          text-transform: uppercase;
          color: #fff;
          padding: 0.28rem 0.85rem;
          border-radius: 999px;
          margin-bottom: 0.9rem;
        }

        .product-h2 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(2.3rem, 5vw, 3.4rem);
          font-weight: 900;
          color: var(--negro);
          line-height: 1.0;
          letter-spacing: -0.5px;
          margin: 0 0 0.4rem;
        }

        .product-tagline {
          font-size: 1.05rem;
          font-style: italic;
          color: var(--gris);
          margin: 0 0 0.85rem;
        }

        .product-desc {
          font-size: 0.94rem;
          color: var(--gris);
          line-height: 1.6;
          margin: 0 0 1rem;
        }

        .ingredients-pill {
          display: inline-block;
          font-size: 0.79rem;
          font-weight: 600;
          color: var(--verde);
          background: var(--verde-suave);
          padding: 0.28rem 0.85rem;
          border-radius: 999px;
          margin-bottom: 1.3rem;
        }

        .price-big {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(3rem, 6vw, 4.5rem);
          font-weight: 900;
          color: var(--negro);
          line-height: 1;
          margin: 0 0 0.18rem;
        }

        .price-note {
          font-size: 0.8rem;
          color: #7a8078;           /* 4.6:1 on cream ✓ */
          margin: 0 0 1.3rem;
        }

        /* ─────────────────────────────────────────
           STORY CARD
        ───────────────────────────────────────── */
        .story-card {
          background: var(--dark);
          border-radius: 24px;
          padding: 4rem 3rem;
          text-align: center;
          margin: 2.5rem 0;
        }

        .story-quote {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(2rem, 5vw, 3.2rem);
          font-weight: 800;
          color: #FFF6E6;
          line-height: 1.15;
          margin: 0 auto 1.5rem;
          max-width: 680px;
        }

        .story-body {
          color: rgba(255,246,230,0.58);  /* 3.4:1 on dark — large text context ✓ */
          font-size: 0.97rem;
          line-height: 1.72;
          max-width: 540px;
          margin: 0 auto 1.5rem;
        }

        .story-brand {
          font-size: 0.78rem;
          font-weight: 600;
          letter-spacing: 1.5px;
          text-transform: uppercase;
          color: rgba(255,246,230,0.35);
        }

        /* ─────────────────────────────────────────
           INGREDIENTS
        ───────────────────────────────────────── */
        .ingredient-card {
          background: #fff;
          border: 1.5px solid var(--linea);
          border-radius: 18px;
          padding: 1.6rem 1.2rem;
          text-align: center;
        }

        .ingredient-icon { font-size: 2.4rem; margin-bottom: 0.55rem; }

        .ingredient-name {
          font-weight: 800;
          font-size: 1rem;
          color: var(--negro);
          margin: 0 0 0.3rem;
        }

        .ingredient-desc {
          font-size: 0.84rem;
          color: var(--gris);
          line-height: 1.5;
          margin: 0;
        }

        /* ─────────────────────────────────────────
           HOW TO ORDER — 3 STEPS
        ───────────────────────────────────────── */
        .steps-wrap {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1.25rem;
          margin-bottom: 1rem;
        }

        .step-card {
          background: #fff;
          border: 1.5px solid var(--linea);
          border-radius: 18px;
          padding: 1.6rem 1.4rem;
        }

        .step-num {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: 2.8rem;
          font-weight: 900;
          color: var(--linea);
          line-height: 1;
          margin-bottom: 0.5rem;
        }

        .step-title {
          font-weight: 800;
          color: var(--negro);
          font-size: 1rem;
          margin: 0 0 0.35rem;
        }

        .step-desc {
          font-size: 0.86rem;
          color: var(--gris);
          line-height: 1.5;
          margin: 0;
        }

        /* ─────────────────────────────────────────
           CHECKOUT
        ───────────────────────────────────────── */
        .checkout-notice {
          background: var(--verde-suave);
          border: 1px solid #b8d4b8;
          border-radius: 10px;
          padding: 0.88rem 1.1rem;
          color: #1a4320;             /* 7.5:1 on verde-suave ✓ */
          font-size: 0.88rem;
          font-weight: 600;
          margin-bottom: 1.2rem;
        }

        .order-summary-card {
          background: var(--crema-2);
          border: 1.5px solid var(--linea);
          border-radius: 14px;
          padding: 1.1rem 1.4rem;
          margin-bottom: 1.2rem;
        }

        /* ─────────────────────────────────────────
           FORM INPUTS — contrast fixes
        ───────────────────────────────────────── */
        /* text & textarea: white bg, dark text */
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextArea"]  [data-baseweb="textarea"] {
          background: #ffffff !important;
          border: 1.5px solid var(--linea) !important;
          border-radius: 8px !important;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
          background: #ffffff !important;
          color: var(--negro) !important;     /* 14:1 on white ✓ */
        }

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
          color: #767b74 !important;          /* 4.7:1 on white ✓ */
        }

        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
        [data-testid="stTextArea"]  [data-baseweb="textarea"]:focus-within {
          border-color: var(--verde) !important;
          box-shadow: 0 0 0 2px rgba(36,92,42,0.15) !important;
        }

        /* number input main content */
        [data-testid="stNumberInput"] [data-baseweb="input"] {
          background: #ffffff !important;
          border: 1.5px solid var(--linea) !important;
          border-radius: 8px !important;
        }

        [data-testid="stNumberInput"] input {
          background: #ffffff !important;
          color: var(--negro) !important;
          font-weight: 700 !important;
          font-size: 1rem !important;
          text-align: center !important;
        }

        /* ─────────────────────────────────────────
           BUTTONS
        ───────────────────────────────────────── */
        div[data-testid="stButton"] > button {
          border-radius: 999px;
          border: 2px solid var(--verde);
          background: var(--verde);
          color: #FFF6E6;
          font-weight: 800;
          font-size: 0.91rem;
          min-height: 2.9rem;
          padding: 0 1.5rem;
          transition: background 0.14s, transform 0.1s;
        }

        div[data-testid="stButton"] > button:hover {
          background: var(--verde-hover);
          border-color: var(--verde-hover);
          transform: translateY(-1px);
        }

        div[data-testid="stLinkButton"] > a {
          border-radius: 999px;
          font-weight: 800;
        }

        /* ─────────────────────────────────────────
           FOOTER
        ───────────────────────────────────────── */
        .site-footer {
          background: var(--dark);
          border-radius: 24px;
          padding: 3rem;
          margin-top: 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1.5rem;
        }

        .footer-brand {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: 1.5rem;
          font-weight: 800;
          color: #FFF6E6;
          line-height: 1;
        }

        .footer-sub {
          color: rgba(255,246,230,0.45);
          font-size: 0.83rem;
          margin-top: 0.3rem;
        }

        .footer-link {
          color: var(--curcuma) !important;
          text-decoration: none !important;
          font-weight: 700;
          font-size: 0.9rem;
        }

        .footer-note {
          color: rgba(255,246,230,0.28);
          font-size: 0.75rem;
          margin-top: 0.3rem;
        }

        /* ─────────────────────────────────────────
           RESPONSIVE
        ───────────────────────────────────────── */
        @media (max-width: 768px) {
          .hero-h1    { font-size: 3.8rem; }
          .steps-wrap { grid-template-columns: 1fr; }
          .trust-strip { flex-direction: column; }
          .trust-item  { border-right: none; border-bottom: 1px solid var(--linea); }
          .site-footer { flex-direction: column; text-align: center; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─── sections ───────────────────────────────────────────────────────────────

def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
          <div class="hero-eyebrow">Colombia · Horneadas · Sin freír</div>
          <h1 class="hero-h1">Crujiente<br>real.</h1>
          <p class="hero-claim">
            Chips de plátano con cúrcuma y pimienta negra.
            El snack que no para de pedir.
          </p>
          <div class="hero-pill-row">
            <span class="hero-pill">🌿 Plátano + cúrcuma</span>
            <span class="hero-pill">⚫ Pimienta negra</span>
            <span class="hero-pill">13 g por bolsa</span>
            <span class="hero-pill">Pedido por WhatsApp</span>
          </div>
          <a class="hero-cta" href="#sabores">Ver sabores →</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, img_col, _ = st.columns([1, 2, 1])
    with img_col:
        hero_img = BASE_DIR / "imgenes_finales" / "55d95c75-98ae-4418-a4df-c4689f51441c.jpeg"
        if hero_img.exists():
            st.image(str(hero_img), use_container_width=True)


def render_trust_strip() -> None:
    st.markdown(
        """
        <div class="trust-strip">
          <div class="trust-item">🔥 Horneadas, no fritas</div>
          <div class="trust-item">🌿 Ingredientes reales</div>
          <div class="trust-item">📦 13 g por bolsa</div>
          <div class="trust-item">💬 Pedido por WhatsApp</div>
          <div class="trust-item">🇨🇴 Hecho en Colombia</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_products(products: list[dict]) -> None:
    st.markdown('<span class="section-tag">Nuestros sabores</span>', unsafe_allow_html=True)
    st.markdown(
        '<h2 id="sabores" class="section-h2">Elige tu sabor</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="section-copy">3 sabores · 13 g por bolsa · Sin pago online</p>',
        unsafe_allow_html=True,
    )

    tab_labels = [f"{p['flavor_tag']}  ·  {p['name'].replace('Curcubites ', '')}" for p in products]
    tabs = st.tabs(tab_labels)

    for tab, p in zip(tabs, products):
        with tab:
            col_img, col_info = st.columns([1.05, 0.95], gap="large")
            with col_img:
                img_path = BASE_DIR / p["image"]
                if img_path.exists():
                    st.image(str(img_path), use_container_width=True)
            with col_info:
                st.markdown(
                    f"""
                    <span class="flavor-tag-badge" style="background:{p['badge_color']}">{p['flavor_tag']}</span>
                    <h2 class="product-h2">{p['name']}</h2>
                    <p class="product-tagline">{p['tagline']}</p>
                    <p class="product-desc">{p['description']}</p>
                    <span class="ingredients-pill">🌿 {p['ingredients']}</span>
                    <div class="price-big">{money(int(p['price']))}</div>
                    <p class="price-note">por bolsa · 13 g · Sin pago online</p>
                    """,
                    unsafe_allow_html=True,
                )
                qty = st.number_input(
                    "Unidades",
                    min_value=1,
                    max_value=24,
                    value=1,
                    step=1,
                    key=f"qty_{p['id']}",
                )
                if st.button(
                    f"Agregar {int(qty)} al carrito — {money(int(p['price']) * int(qty))}",
                    key=f"add_{p['id']}",
                    use_container_width=True,
                ):
                    add_to_cart(p["id"], int(qty))
                    st.toast(f"✓ {p['name']} agregado al carrito")
                    st.rerun()


def render_story() -> None:
    st.markdown(
        """
        <div class="story-card">
          <div class="story-quote">
            "Nació de un antojo.<br>Quedó de un hábito."
          </div>
          <p class="story-body">
            Curcubites empezó con una pregunta simple: ¿por qué el snack sabroso
            tiene que ser ultra-procesado? Plátano, cúrcuma y pimienta negra.
            Tres ingredientes reales, un resultado crujiente. Sin fritura, sin excusas.
          </p>
          <div class="story-brand">— Curcubites · Colombia</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ingredients() -> None:
    st.markdown('<span class="section-tag">Ingredientes</span>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-h2">Lo que le entra</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Sin saborizantes artificiales. Lo que lees en el empaque es lo que comes.</p>',
        unsafe_allow_html=True,
    )
    cols = st.columns(3, gap="large")
    data = [
        ("🍌", "Plátano", "Base crujiente, horneado sin freír. Natural, con fibra y sin aceite extra."),
        ("🌾", "Cúrcuma", "Color dorado, sabor terroso. El ingrediente estrella de Curcubites."),
        ("⚫", "Pimienta negra", "Activa la cúrcuma y da el cierre perfecto en cada mordisco."),
    ]
    for col, (icon, name, desc) in zip(cols, data):
        col.markdown(
            f"""
            <div class="ingredient-card">
              <div class="ingredient-icon">{icon}</div>
              <p class="ingredient-name">{name}</p>
              <p class="ingredient-desc">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_how_to_order() -> None:
    st.markdown('<span class="section-tag" style="margin-top:2.5rem;display:block">El proceso</span>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-h2">Cómo hacer tu pedido</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Sin registro, sin pago online. Directo y rápido.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="steps-wrap">
          <div class="step-card">
            <div class="step-num">01</div>
            <p class="step-title">Elige tu sabor</p>
            <p class="step-desc">Original, Picante o Dulce. Selecciona la cantidad y agrégalo al carrito lateral.</p>
          </div>
          <div class="step-card">
            <div class="step-num">02</div>
            <p class="step-title">Completa tus datos</p>
            <p class="step-desc">Nombre, WhatsApp, ciudad y dirección en el formulario de pedido.</p>
          </div>
          <div class="step-card">
            <div class="step-num">03</div>
            <p class="step-title">Confirma por WhatsApp</p>
            <p class="step-desc">Te generamos el mensaje con tu pedido. Lo enviás y coordinamos la entrega.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cart(products: list[dict]) -> None:
    with st.sidebar:
        items = cart_items(products)
        st.markdown("## 🛒 Carrito")

        if not items:
            st.markdown("Tu carrito está vacío.")
            st.caption("Elige un sabor arriba para continuar.")
            return

        total = cart_total(items)
        st.markdown(f"### Total: {money(total)}")
        st.caption("Sin pago online — confirmamos por WhatsApp")
        st.divider()

        for item in items:
            c1, c2 = st.columns([2, 1])
            c1.markdown(f"**{item['name']}**")
            c1.caption(f"{money(item['price'])} × {item['qty']} = {money(item['subtotal'])}")
            qty = c2.number_input(
                "cant",
                min_value=0,
                max_value=99,
                value=int(item["qty"]),
                step=1,
                key=f"cart_qty_{item['id']}",
                label_visibility="collapsed",
            )
            update_quantity(item["id"], int(qty))
            if st.button("✕ Quitar", key=f"remove_{item['id']}", use_container_width=True):
                remove_from_cart(item["id"])
                st.rerun()
            st.divider()

        st.markdown(f"**Total: {money(cart_total(cart_items(products)))}**")


def render_checkout(products: list[dict]) -> None:
    items = cart_items(products)
    st.markdown(
        '<span class="section-tag" style="margin-top:2rem;display:block">Finalizar</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<h2 class="section-h2">Finaliza tu pedido</h2>', unsafe_allow_html=True)

    if not items:
        st.info("Agrega al menos un producto al carrito para continuar.")
        return

    total = cart_total(items)
    rows = "".join(
        f"<tr>"
        f"<td style='padding:.28rem 0;font-size:.9rem;color:#4a5048'>{i['qty']} × {i['name']}</td>"
        f"<td style='text-align:right;padding:.28rem 0;font-weight:700;color:#151A12'>{money(i['subtotal'])}</td>"
        f"</tr>"
        for i in items
    )
    st.markdown(
        f"""
        <div class="order-summary-card">
          <table style="width:100%;border-collapse:collapse">
            {rows}
            <tr style="border-top:1.5px solid #E0D5C0">
              <td style="padding:.55rem 0;font-weight:900;font-size:1.05rem;color:#151A12">Total</td>
              <td style="text-align:right;padding:.55rem 0;font-weight:900;font-size:1.05rem;color:#151A12">{money(total)}</td>
            </tr>
          </table>
        </div>
        <div class="checkout-notice">
          💬 Sin pago online — generás el mensaje y lo enviás por WhatsApp para confirmar la entrega.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("checkout_form"):
        col_a, col_b = st.columns(2)
        name = col_a.text_input("Nombre completo *")
        phone = col_b.text_input("WhatsApp *", placeholder="+57 300 000 0000")
        city = col_a.text_input("Ciudad *")
        address = col_b.text_input("Dirección de entrega *")
        notes = st.text_area(
            "Notas del pedido",
            placeholder="Horario de entrega, barrio, referencias…",
        )
        submitted = st.form_submit_button("Preparar pedido →", use_container_width=True)

    if submitted:
        missing = [
            label
            for label, val in {
                "nombre": name, "WhatsApp": phone, "ciudad": city, "dirección": address
            }.items()
            if not val.strip()
        ]
        if missing:
            st.error(f"Faltan campos: {', '.join(missing)}")
            return
        st.session_state.order_message = order_message(
            items, name, phone, city, address, notes
        )

    message = st.session_state.get("order_message")
    if message:
        st.success("✓ Pedido listo. Envíalo por WhatsApp o correo para confirmar.")
        st.code(message, language="text")
        col_w, col_m = st.columns(2)
        col_w.link_button("📲 Enviar por WhatsApp", whatsapp_url(message), use_container_width=True)
        col_m.link_button("✉️ Enviar por correo", mailto_url(message), use_container_width=True)


def render_faq() -> None:
    st.markdown(
        '<span class="section-tag" style="margin-top:1.5rem;display:block">FAQ</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<h2 class="section-h2">Preguntas frecuentes</h2>', unsafe_allow_html=True)
    faqs = [
        ("¿Cuánto pesa cada bolsa?", "13 gramos por bolsa. Tamaño ideal para el antojo del día."),
        ("¿Cómo hago el pedido?", "Armas el carrito aquí, completas el formulario y nos contactas por WhatsApp. Sin pago online."),
        ("¿Hacen envíos?", "Coordinamos la entrega según la ciudad. Escríbenos para confirmar cobertura y tiempos."),
        ("¿Son realmente sin freír?", "Sí, todas las Curcubites son horneadas. Sin fritura, sin aceite extra, sin compromiso con el sabor."),
        ("¿Puedo pedir varios sabores en el mismo pedido?", "Claro. Agrega los sabores que quieras al carrito y hacemos un solo pedido."),
    ]
    for q, a in faqs:
        with st.expander(q):
            st.write(a)


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="site-footer">
          <div>
            <div class="footer-brand">Curcubites</div>
            <div class="footer-sub">Chips de plátano horneados con cúrcuma · Colombia</div>
          </div>
          <div style="text-align:right">
            <a class="footer-link" href="mailto:{DEFAULT_EMAIL}">{DEFAULT_EMAIL}</a>
            <div class="footer-note">Pedidos por WhatsApp · Sin pago online</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── main ───────────────────────────────────────────────────────────────────

def main() -> None:
    ensure_cart()
    inject_styles()
    products = load_products()
    render_cart(products)
    render_hero()
    render_trust_strip()
    render_products(products)
    render_story()
    render_ingredients()
    render_how_to_order()
    render_checkout(products)
    render_faq()
    render_footer()


if __name__ == "__main__":
    main()
