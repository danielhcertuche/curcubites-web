import json
import os
import base64
from pathlib import Path
from urllib.parse import quote

import streamlit as st


BASE_DIR = Path(__file__).parent
PRODUCTS_PATH = BASE_DIR / "data" / "products.json"
DEFAULT_EMAIL = "ventas@curcubites.com"


st.set_page_config(
    page_title="Curcubites | Chips de plátano horneadas",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def money(value: int) -> str:
    return f"${value:,.0f}".replace(",", ".")


@st.cache_data
def load_products() -> list[dict]:
    with PRODUCTS_PATH.open(encoding="utf-8") as file:
        return json.load(file)


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
    by_id = {product["id"]: product for product in products}
    return [
        {**by_id[product_id], "qty": qty, "subtotal": int(by_id[product_id]["price"]) * qty}
        for product_id, qty in st.session_state.cart.items()
        if product_id in by_id
    ]


def cart_total(items: list[dict]) -> int:
    return sum(item["subtotal"] for item in items)


def order_message(items: list[dict], name: str, phone: str, city: str, address: str, notes: str) -> str:
    lines = [
        "Hola, quiero hacer un pedido de Curcubites:",
        "",
        *[f"- {item['qty']} x {item['name']} = {money(item['subtotal'])}" for item in items],
        "",
        f"Total: {money(cart_total(items))}",
        "",
        f"Nombre: {name}",
        f"WhatsApp: {phone}",
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


def image_data_uri(path: Path) -> str:
    suffix = path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def payment_mock_url(method: str, total: int) -> str:
    return f"?pago={quote(method)}&total={total}#pago-mock"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

        :root {
          --ink: #151A12;
          --olive: #0F1A0C;
          --green: #245C2A;
          --green-2: #3A7A41;
          --leaf: #E7F1DF;
          --cream: #FFF6E6;
          --cream-2: #F4EAD6;
          --paper: #FFFFFF;
          --turmeric: #D99A22;
          --terracotta: #A85232;
          --line: #E2D5BB;
          --muted: #50564C;
        }

        html { scroll-behavior: smooth; overscroll-behavior: contain; }
        .stApp { background: var(--cream); color: var(--ink); }
        html, body, [class*="css"] { font-family: Inter, system-ui, sans-serif; }

        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
        #MainMenu, footer { visibility: hidden; height: 0; }
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stMainBlockContainer"] {
          max-width: 1140px;
          padding: 1rem 1.35rem 3.2rem !important;
        }

        .topbar {
          position: sticky;
          top: 0;
          z-index: 20;
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
          background: rgba(255, 246, 230, 0.92);
          backdrop-filter: blur(14px);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 0.78rem 0.95rem;
          margin-bottom: 1.2rem;
        }
        .brand-lockup { display: flex; align-items: center; gap: 0.72rem; }
        .brand-mark {
          width: 38px; height: 38px; border-radius: 50%;
          display: grid; place-items: center;
          background: var(--olive); color: var(--cream);
          font-weight: 900; font-family: 'Playfair Display', Georgia, serif;
        }
        .brand-name { font-weight: 900; letter-spacing: 0; line-height: 1; }
        .brand-sub { font-size: 0.72rem; color: var(--muted); margin-top: 0.12rem; }
        .navlinks { display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; justify-content: flex-end; }
        .navlinks a {
          color: var(--ink) !important; text-decoration: none !important;
          font-size: 0.84rem; font-weight: 800;
          padding: 0.48rem 0.72rem; border-radius: 999px;
          min-height: 44px;
          display: inline-flex;
          align-items: center;
          touch-action: manipulation;
          transition: background 180ms ease, color 180ms ease, transform 180ms ease;
        }
        .navlinks a:hover { background: var(--leaf); transform: translateY(-1px); }
        .navlinks a:focus-visible,
        .social-rail a:focus-visible,
        .btn-main:focus-visible,
        .btn-soft:focus-visible {
          outline: 3px solid var(--turmeric);
          outline-offset: 3px;
        }
        .nav-cta { background: var(--green) !important; color: var(--cream) !important; }

        .social-rail {
          position: fixed; right: 1rem; top: 35%; z-index: 30;
          display: flex; flex-direction: column; gap: 0.55rem;
        }
        .social-rail a {
          width: 46px; height: 46px; border-radius: 50%;
          display: grid; place-items: center;
          background: var(--paper); border: 1px solid var(--line);
          color: var(--ink) !important; text-decoration: none !important;
          font-size: 0.72rem; font-weight: 900;
          box-shadow: 0 12px 32px rgba(15, 26, 12, 0.12);
          touch-action: manipulation;
          transition: background 180ms ease, color 180ms ease, transform 180ms ease;
        }
        .social-rail a:hover { background: var(--green); color: var(--cream) !important; transform: translateX(-2px); }

        .hero {
          position: relative;
          overflow: hidden;
          min-height: 58dvh;
          border-radius: 8px;
          background:
            radial-gradient(circle at 82% 18%, rgba(217,154,34,.28), transparent 34%),
            linear-gradient(135deg, #0F1A0C 0%, #152411 58%, #245C2A 100%);
          background-size: cover;
          background-position: center;
          padding: clamp(1.6rem, 4vw, 3.2rem);
          display: grid;
          grid-template-columns: 1.02fr 0.98fr;
          gap: clamp(1.4rem, 4vw, 4rem);
          align-items: center;
        }
        .hero::after {
          content: "";
          position: absolute;
          left: -6%; bottom: -10%;
          width: 48%; height: 34%;
          background: var(--turmeric);
          transform: rotate(-5deg);
          opacity: .92;
          clip-path: polygon(0 35%, 100% 0, 90% 100%, 0 100%);
        }
        .hero-copy, .hero-visual { position: relative; z-index: 2; }
        .eyebrow {
          display: inline-flex; align-items: center; gap: .45rem;
          color: rgba(255,246,230,.9);
          border: 1px solid rgba(255,246,230,.25);
          background: rgba(255,255,255,.08);
          border-radius: 999px;
          padding: .38rem .9rem;
          font-size: .74rem;
          font-weight: 900;
          text-transform: uppercase;
          letter-spacing: 1.8px;
          margin-bottom: 1.2rem;
        }
        .hero h1 {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(2.8rem, 7vw, 5.4rem);
          line-height: .94;
          color: var(--cream);
          margin: 0 0 1.1rem;
          letter-spacing: 0;
        }
        .hero p {
          color: rgba(255,246,230,.82);
          font-size: clamp(1rem, 2vw, 1.18rem);
          line-height: 1.7;
          max-width: 39rem;
          margin: 0 0 1.5rem;
        }
        .hero-actions { display: flex; gap: .8rem; flex-wrap: wrap; align-items: center; }
        .btn-main, .btn-soft {
          display: inline-flex; align-items: center; justify-content: center;
          min-height: 3rem;
          padding: .72rem 1.25rem;
          border-radius: 999px;
          text-decoration: none !important;
          font-weight: 900;
          font-size: .92rem;
          touch-action: manipulation;
          transition: transform 180ms ease, background 180ms ease, color 180ms ease;
        }
        .btn-main { background: var(--turmeric); color: var(--olive) !important; }
        .btn-soft { border: 1px solid rgba(255,246,230,.32); color: var(--cream) !important; background: rgba(255,255,255,.08); }
        .btn-main:hover, .btn-soft:hover { transform: translateY(-2px); }
        .hero-card-img {
          background: rgba(255,246,230,.92);
          border: 1px solid rgba(255,246,230,.45);
          border-radius: 8px;
          padding: .7rem;
          box-shadow: 0 30px 80px rgba(0,0,0,.32);
          transform: rotate(2deg);
          max-width: 380px;
          margin-left: auto;
        }
        .hero-card-img img {
          border-radius: 6px;
          display: block;
          width: 100%;
          aspect-ratio: 4 / 4.7;
          object-fit: cover;
        }

        .trust-strip {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          border: 1px solid var(--line);
          border-top: 0;
          background: var(--paper);
          border-radius: 0 0 8px 8px;
          margin-bottom: 1.4rem;
        }
        .trust-item { padding: 1rem; border-right: 1px solid var(--line); }
        .trust-item:last-child { border-right: 0; }
        .trust-item strong { display: block; font-size: .95rem; }
        .trust-item span { display: block; color: var(--muted); font-size: .78rem; margin-top: .15rem; }

        .section-band {
          margin: 1.45rem 0;
          padding: clamp(1.35rem, 3vw, 2.4rem);
          border-radius: 8px;
          background: var(--paper);
          border: 1px solid var(--line);
        }
        .section-band.alt { background: var(--cream-2); }
        .section-head { display: flex; justify-content: space-between; gap: 1rem; align-items: end; margin-bottom: 1.6rem; }
        .section-kicker {
          color: var(--green);
          font-size: .72rem;
          font-weight: 900;
          letter-spacing: 2px;
          text-transform: uppercase;
          margin-bottom: .45rem;
        }
        .section-title {
          font-family: 'Playfair Display', Georgia, serif;
          color: var(--ink);
          font-size: clamp(2.3rem, 5vw, 4.2rem);
          line-height: 1;
          margin: 0;
        }
        .section-copy { color: var(--muted); max-width: 34rem; line-height: 1.65; margin: .7rem 0 0; }

        .product-shell {
          display: grid;
          grid-template-columns: minmax(220px, .62fr) minmax(320px, 1fr);
          gap: clamp(1rem, 3vw, 2rem);
          align-items: center;
          background: var(--paper);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: clamp(1rem, 2.5vw, 1.6rem);
        }
        .product-photo img {
          border-radius: 8px;
          box-shadow: 0 14px 34px rgba(21,26,18,.14);
          aspect-ratio: 1 / 1;
          object-fit: cover;
          width: 100%;
          max-height: 330px;
        }
        .flavor-tag {
          display: inline-block;
          color: var(--cream);
          border-radius: 999px;
          padding: .38rem .9rem;
          font-size: .7rem;
          font-weight: 900;
          letter-spacing: 2px;
          text-transform: uppercase;
          margin-bottom: .9rem;
        }
        .product-title {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(2rem, 4vw, 3.15rem);
          line-height: 1;
          margin: 0 0 .55rem;
        }
        .product-sub { color: var(--terracotta); font-weight: 800; font-style: italic; margin-bottom: .75rem; }
        .product-desc { color: var(--muted); line-height: 1.55; margin-bottom: .8rem; }
        .ingredient-pill {
          display: inline-block;
          background: var(--leaf);
          color: var(--green);
          font-weight: 900;
          border-radius: 999px;
          padding: .45rem .8rem;
          font-size: .8rem;
          margin-bottom: 1rem;
        }
        .price { font-family: 'Playfair Display', Georgia, serif; font-weight: 900; font-size: clamp(2.6rem, 6vw, 4.1rem); line-height: .9; }
        .price-note { color: var(--muted); font-size: .82rem; margin-bottom: 1rem; }

        div[data-baseweb="tab-list"] { gap: .55rem; border: 0 !important; margin-bottom: 1.6rem; }
        button[data-baseweb="tab"] {
          border: 1px solid var(--line) !important;
          background: var(--paper) !important;
          border-radius: 999px !important;
          padding: .52rem 1.1rem !important;
          font-weight: 900 !important;
          color: var(--ink) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] { background: var(--olive) !important; color: var(--cream) !important; }
        div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }

        [data-testid="stNumberInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextArea"] [data-baseweb="textarea"] {
          border: 1px solid var(--line) !important;
          border-radius: 8px !important;
          background: #fff !important;
        }
        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea { color: var(--ink) !important; background: #fff !important; }
        div[data-testid="stButton"] > button {
          border-radius: 999px;
          border: 1px solid var(--green);
          background: var(--green);
          color: var(--cream);
          min-height: 3rem;
          font-weight: 900;
          touch-action: manipulation;
        }
        div[data-testid="stButton"] > button:hover { background: var(--olive); border-color: var(--olive); color: var(--cream); }
        div[data-testid="stButton"] > button:focus-visible {
          outline: 3px solid var(--turmeric) !important;
          outline-offset: 3px !important;
        }
        div[data-testid="stLinkButton"] > a { border-radius: 999px; font-weight: 900; }

        .editorial-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1rem;
        }
        .editorial-card {
          min-height: 190px;
          border-radius: 8px;
          padding: 1.35rem;
          background: var(--cream);
          border: 1px solid var(--line);
          position: relative;
          overflow: hidden;
        }
        .editorial-card::after {
          content: "";
          position: absolute;
          width: 160px; height: 80px;
          right: -32px; bottom: 20px;
          background: var(--turmeric);
          clip-path: polygon(0 20%, 100% 0, 85% 100%, 10% 80%);
          opacity: .75;
        }
        .editorial-card.dark { background: var(--olive); color: var(--cream); border-color: var(--olive); }
        .editorial-card h3 { font-family: 'Playfair Display', Georgia, serif; font-size: 1.7rem; line-height: 1; margin: 0 0 .7rem; position: relative; z-index: 2; }
        .editorial-card p { color: var(--muted); line-height: 1.6; font-size: .92rem; position: relative; z-index: 2; }
        .editorial-card.dark p { color: rgba(255,246,230,.74); }

        .blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
        .blog-card {
          background: var(--paper);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 1.25rem;
        }
        .blog-card span { color: var(--green); font-size: .7rem; font-weight: 900; letter-spacing: 1.6px; text-transform: uppercase; }
        .blog-card h3 { margin: .5rem 0; font-size: 1.12rem; }
        .blog-card p { color: var(--muted); font-size: .9rem; line-height: 1.55; }
        .blog-card a {
          color: var(--green) !important;
          font-weight: 900;
          text-decoration: none !important;
        }

        .problem-grid,
        .funnel-grid,
        .payment-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1rem;
        }
        .problem-card,
        .funnel-card,
        .payment-card {
          border: 1px solid var(--line);
          border-radius: 8px;
          background: var(--paper);
          padding: 1.25rem;
        }
        .problem-card.problem { border-top: 6px solid var(--terracotta); }
        .problem-card.process { border-top: 6px solid var(--turmeric); }
        .problem-card.solution { border-top: 6px solid var(--green); }
        .problem-card span,
        .funnel-card span {
          display: inline-flex;
          width: 34px;
          height: 34px;
          border-radius: 999px;
          align-items: center;
          justify-content: center;
          background: var(--leaf);
          color: var(--green);
          font-weight: 900;
          margin-bottom: .8rem;
        }
        .problem-card h3,
        .funnel-card h3,
        .payment-card h3 { margin: 0 0 .45rem; }
        .problem-card p,
        .funnel-card p,
        .payment-card p { color: var(--muted); line-height: 1.55; font-size: .92rem; margin: 0; }

        .cart-card, .checkout-card {
          background: var(--paper);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 1.1rem;
        }
        .cart-card { position: sticky; top: 92px; }
        .cart-row {
          display: flex;
          justify-content: space-between;
          gap: .8rem;
          border-bottom: 1px solid var(--line);
          padding: .75rem 0;
        }
        .cart-row:last-child { border-bottom: 0; }
        .notice {
          background: var(--leaf);
          color: var(--green);
          border-radius: 8px;
          padding: .85rem 1rem;
          font-weight: 800;
          margin: 1rem 0;
        }
        .payment-card.featured {
          background: var(--olive);
          color: var(--cream);
          border-color: var(--olive);
        }
        .payment-card.featured p { color: rgba(255,246,230,.72); }
        .mock-badge {
          display: inline-block;
          border-radius: 999px;
          background: var(--leaf);
          color: var(--green);
          padding: .28rem .7rem;
          font-size: .72rem;
          font-weight: 900;
          margin-bottom: .7rem;
        }
        .footer {
          margin-top: 3rem;
          background: var(--olive);
          color: var(--cream);
          border-radius: 8px;
          padding: 2rem;
          display: flex;
          justify-content: space-between;
          gap: 1rem;
          flex-wrap: wrap;
        }
        .footer a { color: var(--turmeric) !important; text-decoration: none !important; font-weight: 900; }

        @media (max-width: 900px) {
          [data-testid="stMainBlockContainer"] { padding: .7rem .8rem 3rem !important; }
          .topbar { position: relative; align-items: flex-start; }
          .navlinks { justify-content: flex-start; }
          .hero, .product-shell { grid-template-columns: 1fr; min-height: auto; }
          .trust-strip, .editorial-grid, .blog-grid, .problem-grid, .funnel-grid, .payment-grid { grid-template-columns: 1fr; }
          .trust-item { border-right: 0; border-bottom: 1px solid var(--line); }
          .social-rail { position: static; flex-direction: row; margin: .8rem 0 1rem; }
          .section-head { display: block; }
          .cart-card { position: static; }
          .hero-card-img { margin: 0; max-width: 100%; }
          .product-photo img { max-height: 280px; }
        }

        @media (max-width: 1180px) {
          .social-rail {
            right: .45rem;
            top: auto;
            bottom: .8rem;
            flex-direction: row;
          }
        }

        @media (prefers-reduced-motion: reduce) {
          html { scroll-behavior: auto; }
          *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_nav() -> None:
    st.markdown(
        """
        <nav class="topbar">
          <div class="brand-lockup">
            <div class="brand-mark">C</div>
            <div>
              <div class="brand-name">Curcubites</div>
              <div class="brand-sub">Chips de plátano horneadas</div>
            </div>
          </div>
          <div class="navlinks">
            <a href="#inicio">Inicio</a>
            <a href="#productos">Productos</a>
            <a href="#carrito">Carrito</a>
            <a href="#blog">Blog</a>
            <a href="#carrito" class="nav-cta">Pedir</a>
          </div>
        </nav>
        <aside class="social-rail" aria-label="Redes sociales y blog">
          <a href="https://www.instagram.com/curcubites_snack/" target="_blank" rel="noopener" title="Instagram" aria-label="Instagram de Curcubites">IG</a>
          <a href="https://www.tiktok.com/search?q=curcubites_snack" target="_blank" rel="noopener" title="TikTok" aria-label="TikTok de Curcubites">TK</a>
          <a href="#blog" title="Blog" aria-label="Blog Curcubites">BL</a>
          <a href="#carrito" title="Pedido" aria-label="Hacer pedido por WhatsApp">WA</a>
        </aside>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    image = BASE_DIR / "imgenes_finales" / "c0661bdd-e0ce-42bf-93d8-ee2a60dd867c.jpeg"
    st.markdown('<section id="inicio" class="hero">', unsafe_allow_html=True)
    copy_col, image_col = st.columns([1.08, 0.92], vertical_alignment="center")
    with copy_col:
        st.markdown(
            """
            <div class="hero-copy">
              <div class="eyebrow">Colombia · horneadas · sin freír</div>
              <h1>Chips de plátano horneadas.</h1>
              <p>
                Crujientes, naturales y fáciles de pedir. Con cúrcuma y pimienta negra.
                Lo que sientes después, lo cambia todo.
              </p>
              <div class="hero-actions">
                <a class="btn-main" href="#carrito">Pedir ahora</a>
                <a class="btn-soft" href="#productos">Ver productos</a>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with image_col:
        if image.exists():
            st.markdown(
                f"""
                <div class="hero-card-img">
                  <img src="{image_data_uri(image)}" alt="Bolsa Curcubites Original con chips de plátano horneadas">
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</section>", unsafe_allow_html=True)


def render_trust_strip() -> None:
    st.markdown(
        """
        <div class="trust-strip">
          <div class="trust-item"><strong>Horneadas</strong><span>No fritas.</span></div>
          <div class="trust-item"><strong>Ingredientes claros</strong><span>Plátano, cúrcuma y pimienta.</span></div>
          <div class="trust-item"><strong>Compra flexible</strong><span>WhatsApp o pago mock online.</span></div>
          <div class="trust-item"><strong>Marca local</strong><span>Diseñada para Colombia.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_problem_solution() -> None:
    st.markdown(
        """
        <section class="section-band alt">
          <div class="section-head">
            <div>
              <div class="section-kicker">Necesidad · problema · solución</div>
              <h2 class="section-title">Crujiente sin volver a lo de siempre.</h2>
            </div>
            <p class="section-copy">
              La estrategia de marca parte de una tensión simple: queremos algo rico y práctico,
              pero no siempre queremos caer en frituras o snacks sin historia.
            </p>
          </div>
          <div class="problem-grid">
            <article class="problem-card problem">
              <span>1</span>
              <h3>Necesidad</h3>
              <p>Un antojo rápido, fácil de llevar y con buen sabor para la U, oficina, gym o planes al aire libre.</p>
            </article>
            <article class="problem-card process">
              <span>2</span>
              <h3>Problema</h3>
              <p>La mayoría de opciones crujientes se sienten pesadas, grasosas o poco alineadas con un estilo de vida consciente.</p>
            </article>
            <article class="problem-card solution">
              <span>3</span>
              <h3>Solución</h3>
              <p>Curcubites: plátano horneado con cúrcuma y pimienta negra. Crujido real, ingredientes claros y pedido simple.</p>
            </article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_products(products: list[dict]) -> None:
    st.markdown(
        """
        <section id="productos" class="section-band">
          <div class="section-head">
            <div>
              <div class="section-kicker">Sección de productos</div>
              <h2 class="section-title">Elige el sabor que va contigo.</h2>
            </div>
            <p class="section-copy">
              Tres perfiles para diferentes antojos. Armas tu carrito y eliges confirmación
              por WhatsApp o pasarela mock online.
            </p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    labels = [product["name"].replace("Curcubites ", "") for product in products]
    tabs = st.tabs(labels)
    for tab, product in zip(tabs, products):
        with tab:
            img_path = BASE_DIR / product["image"]
            st.markdown('<div class="product-shell">', unsafe_allow_html=True)
            image_col, info_col = st.columns([1.05, 0.95], gap="large", vertical_alignment="center")
            with image_col:
                if img_path.exists():
                    st.markdown(
                        f"""
                        <div class="product-photo">
                          <img src="{image_data_uri(img_path)}" alt="{product['name']}">
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            with info_col:
                st.markdown(
                    f"""
                    <span class="flavor-tag" style="background:{product.get('badge_color', '#245C2A')}">{product['flavor_tag']}</span>
                    <h3 class="product-title">{product['name']}</h3>
                    <div class="product-sub">{product['tagline']}</div>
                    <p class="product-desc">{product['description']}</p>
                    <span class="ingredient-pill">{product['ingredients']}</span>
                    <div class="price">{money(int(product['price']))}</div>
                    <div class="price-note">por bolsa · 13 g · WhatsApp o pago mock online</div>
                    """,
                    unsafe_allow_html=True,
                )
                qty = st.number_input(
                    "Unidades",
                    min_value=1,
                    max_value=24,
                    value=1,
                    step=1,
                    key=f"qty_{product['id']}",
                )
                if st.button(
                    f"Agregar al pedido · {money(int(product['price']) * int(qty))}",
                    key=f"add_{product['id']}",
                    use_container_width=True,
                ):
                    add_to_cart(product["id"], int(qty))
                    st.toast(f"{product['name']} agregado")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


def render_brand_story() -> None:
    st.markdown(
        """
        <section id="marca" class="section-band alt">
          <div class="section-head">
            <div>
              <div class="section-kicker">Marca con intención</div>
              <h2 class="section-title">Coherencia de marca, compra simple y contenido que sostiene.</h2>
            </div>
            <p class="section-copy">
              La estrategia cruza las 4C: coherencia en promesa, consistencia visual,
              continuidad de contenidos y complementariedad entre web, Instagram, TikTok y WhatsApp.
            </p>
          </div>
          <div class="editorial-grid">
            <article class="editorial-card dark">
              <h3>Coherencia</h3>
              <p>Misma promesa en web, empaque y redes: plátano horneado con cúrcuma y pimienta negra.</p>
            </article>
            <article class="editorial-card">
              <h3>Consistencia</h3>
              <p>Verde natural, dorado cúrcuma y tono fresco para que la marca se reconozca rápido.</p>
            </article>
            <article class="editorial-card">
              <h3>Complementariedad</h3>
              <p>La web vende, Instagram educa, TikTok atrae y WhatsApp cierra la conversación.</p>
            </article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_moments() -> None:
    st.markdown(
        """
        <section class="section-band">
          <div class="section-head">
            <div>
              <div class="section-kicker">Momentos Curcubites</div>
              <h2 class="section-title">Para cuando el cuerpo pide crujiente.</h2>
            </div>
            <p class="section-copy">
              Oficina, universidad, post-entreno o plan en casa. Curcubites entra donde antes entraba
              cualquier paquete de fritura, pero con una historia más limpia.
            </p>
          </div>
          <div class="editorial-grid">
            <article class="editorial-card"><h3>Después de entrenar</h3><p>Algo rápido, con sabor y sin sentir que dañaste la rutina.</p></article>
            <article class="editorial-card dark"><h3>Entre reuniones</h3><p>Un snack práctico para tener a la mano sin terminar con grasa en los dedos.</p></article>
            <article class="editorial-card"><h3>Plan de tarde</h3><p>Para compartir, probar sabores y convertir el antojo en conversación.</p></article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_blog() -> None:
    st.markdown(
        """
        <section id="blog" class="section-band alt">
          <div class="section-head">
            <div>
              <div class="section-kicker">Blog Curcubites</div>
              <h2 class="section-title">Contenido que abre apetito.</h2>
            </div>
            <p class="section-copy">
              Ideas cortas para redes, educación de producto y cultura snack.
              Esto ayuda a que la marca parezca activa, no solo una página de ventas.
            </p>
          </div>
          <div class="blog-grid">
            <article class="blog-card">
              <span>Ingredientes</span>
              <h3>Por qué usamos cúrcuma y pimienta negra</h3>
              <p>Una dupla de sabor intenso, color dorado y personalidad propia en cada mordisco.</p>
              <a href="https://www.instagram.com/curcubites_snack/" target="_blank" rel="noopener">Ver contenido</a>
            </article>
            <article class="blog-card">
              <span>Estilo de vida</span>
              <h3>Snacks para llevar a la U, oficina o gimnasio</h3>
              <p>Pequeños rituales para resolver el antojo sin complicarse la vida.</p>
              <a href="https://www.instagram.com/curcubites_snack/" target="_blank" rel="noopener">Ir a Instagram</a>
            </article>
            <article class="blog-card">
              <span>Marca</span>
              <h3>Cómo se diseñó la identidad de Curcubites</h3>
              <p>Color, empaque y tono pensados para vender desde la primera mirada.</p>
              <a href="#marca">Leer enfoque</a>
            </article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_payment_mock_status() -> None:
    payment = st.query_params.get("pago")
    total = st.query_params.get("total")
    if not payment:
        return
    method = "Nequi" if payment == "nequi" else "Addi" if payment == "addi" else payment.title()
    amount = money(int(total)) if total and total.isdigit() else "total del pedido"
    st.markdown(
        f"""
        <section id="pago-mock" class="section-band alt">
          <div class="section-head">
            <div>
              <div class="section-kicker">Pasarela mock</div>
              <h2 class="section-title">Redirección a {method} simulada.</h2>
            </div>
            <p class="section-copy">
              Ambiente demo para mostrar el flujo de pago online. No procesa dinero real.
              Pedido por {amount}. En producción aquí se conectaría la pasarela real.
            </p>
          </div>
          <div class="payment-grid">
            <article class="payment-card featured">
              <span class="mock-badge">Demo</span>
              <h3>Estado del pago</h3>
              <p>Pago pendiente de confirmación. Usa WhatsApp para cerrar el pedido piloto.</p>
            </article>
            <article class="payment-card">
              <span class="mock-badge">Siguiente paso</span>
              <h3>Confirmación</h3>
              <p>El usuario vuelve a Curcubites y recibe instrucciones claras de entrega.</p>
            </article>
            <article class="payment-card">
              <span class="mock-badge">Producción</span>
              <h3>Integración real</h3>
              <p>Se reemplaza este enlace por Nequi, Addi u otra pasarela cuando existan credenciales.</p>
            </article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_checkout(products: list[dict]) -> None:
    items = cart_items(products)
    render_payment_mock_status()
    st.markdown(
        """
        <section id="carrito" class="section-band">
          <div class="section-head">
            <div>
              <div class="section-kicker">Sección del carrito de compras</div>
              <h2 class="section-title">Carrito claro. Pago flexible.</h2>
            </div>
            <p class="section-copy">
              El flujo está pensado como funnel de conversión: eliges sabores, completas datos
              y confirmas por WhatsApp o por una pasarela mock tipo Nequi/Addi.
            </p>
          </div>
          <div class="funnel-grid">
            <article class="funnel-card"><span>1</span><h3>Elige</h3><p>Agrega sabores y cantidades al carrito.</p></article>
            <article class="funnel-card"><span>2</span><h3>Completa</h3><p>Deja tus datos para coordinar entrega.</p></article>
            <article class="funnel-card"><span>3</span><h3>Confirma</h3><p>WhatsApp, Nequi mock o Addi mock.</p></article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    cart_col, form_col = st.columns([0.9, 1.1], gap="large")
    with cart_col:
        st.markdown('<div class="cart-card">', unsafe_allow_html=True)
        st.markdown("### Tu carrito")
        if not items:
            st.info("Agrega un sabor para iniciar el pedido.")
        else:
            for item in items:
                st.markdown(
                    f"""
                    <div class="cart-row">
                      <div><strong>{item['name']}</strong><br><span>{money(item['price'])} x {item['qty']}</span></div>
                      <strong>{money(item['subtotal'])}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                qty = st.number_input(
                    f"Cantidad {item['name']}",
                    min_value=0,
                    max_value=99,
                    value=int(item["qty"]),
                    step=1,
                    key=f"cart_qty_{item['id']}",
                )
                update_quantity(item["id"], int(qty))
                if st.button("Quitar", key=f"remove_{item['id']}"):
                    remove_from_cart(item["id"])
                    st.rerun()
            st.markdown(f"## Total: {money(cart_total(cart_items(products)))}")
            st.markdown('<div class="notice">Confirmación por WhatsApp o pago mock online.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with form_col:
        st.markdown('<div class="checkout-card">', unsafe_allow_html=True)
        if not items:
            st.warning("El formulario se activa cuando tengas productos en el carrito.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        with st.form("checkout_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Nombre completo *")
            phone = c2.text_input("WhatsApp *", placeholder="+57 300 000 0000")
            city = c1.text_input("Ciudad *")
            address = c2.text_input("Dirección de entrega *")
            notes = st.text_area("Notas", placeholder="Barrio, horario o referencias de entrega.")
            submitted = st.form_submit_button("Preparar mensaje de pedido", use_container_width=True)

        if submitted:
            missing = [
                label
                for label, value in {
                    "nombre": name,
                    "WhatsApp": phone,
                    "ciudad": city,
                    "dirección": address,
                }.items()
                if not value.strip()
            ]
            if missing:
                st.error("Faltan campos: " + ", ".join(missing))
            else:
                st.session_state.order_message = order_message(items, name, phone, city, address, notes)

        message = st.session_state.get("order_message")
        if message:
            st.success("Pedido listo. Envíalo para confirmar disponibilidad y entrega.")
            st.code(message, language="text")
            w_col, m_col = st.columns(2)
            w_col.link_button("Enviar por WhatsApp", whatsapp_url(message), use_container_width=True)
            m_col.link_button("Enviar por correo", mailto_url(message), use_container_width=True)

        total = cart_total(cart_items(products))
        st.markdown("### Pago online mock")
        st.caption("Demo visual: no cobra dinero real. Sirve para mostrar cómo se vería la redirección.")
        p1, p2 = st.columns(2)
        p1.link_button("Pagar con Nequi mock", payment_mock_url("nequi", total), use_container_width=True)
        p2.link_button("Pagar con Addi mock", payment_mock_url("addi", total), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown(
        f"""
        <footer class="footer">
          <div>
            <h3 style="margin:0;font-family:'Playfair Display',Georgia,serif;font-size:2rem">Curcubites</h3>
            <p style="margin:.35rem 0 0;color:rgba(255,246,230,.72)">Chips de plátano horneadas · Colombia</p>
          </div>
          <div>
            <a href="mailto:{DEFAULT_EMAIL}">{DEFAULT_EMAIL}</a><br>
            <span style="color:rgba(255,246,230,.62);font-size:.86rem">Instagram · TikTok · Blog · WhatsApp</span>
          </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    ensure_cart()
    inject_styles()
    products = load_products()
    render_nav()
    render_hero()
    render_trust_strip()
    render_problem_solution()
    render_products(products)
    render_checkout(products)
    render_brand_story()
    render_moments()
    render_blog()
    render_footer()


if __name__ == "__main__":
    main()
