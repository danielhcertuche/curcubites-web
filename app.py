import json
import os
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

        html { scroll-behavior: smooth; }
        .stApp { background: var(--cream); color: var(--ink); }
        html, body, [class*="css"] { font-family: Inter, system-ui, sans-serif; }

        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
        #MainMenu, footer { visibility: hidden; height: 0; }
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stMainBlockContainer"] {
          max-width: 1220px;
          padding: 1.15rem 1.6rem 4rem !important;
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
        }
        .navlinks a:hover { background: var(--leaf); }
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
        }
        .social-rail a:hover { background: var(--green); color: var(--cream) !important; }

        .hero {
          position: relative;
          overflow: hidden;
          min-height: 78vh;
          border-radius: 8px;
          background:
            linear-gradient(90deg, rgba(15,26,12,.94), rgba(15,26,12,.72)),
            url('https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1800&q=80');
          background-size: cover;
          background-position: center;
          padding: clamp(2rem, 5vw, 4.7rem);
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
          font-size: clamp(3.3rem, 8vw, 6.6rem);
          line-height: .9;
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
        }
        .btn-main { background: var(--turmeric); color: var(--olive) !important; }
        .btn-soft { border: 1px solid rgba(255,246,230,.32); color: var(--cream) !important; background: rgba(255,255,255,.08); }
        .hero-card-img {
          background: rgba(255,246,230,.92);
          border: 1px solid rgba(255,246,230,.45);
          border-radius: 8px;
          padding: .7rem;
          box-shadow: 0 30px 80px rgba(0,0,0,.32);
          transform: rotate(2deg);
        }
        .hero-card-img img { border-radius: 6px; display: block; width: 100%; }

        .trust-strip {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          border: 1px solid var(--line);
          border-top: 0;
          background: var(--paper);
          border-radius: 0 0 8px 8px;
          margin-bottom: 3rem;
        }
        .trust-item { padding: 1rem; border-right: 1px solid var(--line); }
        .trust-item:last-child { border-right: 0; }
        .trust-item strong { display: block; font-size: .95rem; }
        .trust-item span { display: block; color: var(--muted); font-size: .78rem; margin-top: .15rem; }

        .section-band {
          margin: 3rem 0;
          padding: clamp(2rem, 5vw, 4rem);
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
          line-height: .98;
          margin: 0;
        }
        .section-copy { color: var(--muted); max-width: 34rem; line-height: 1.65; margin: .7rem 0 0; }

        .product-shell {
          display: grid;
          grid-template-columns: minmax(0, 1fr) minmax(320px, .86fr);
          gap: clamp(1.4rem, 4vw, 3rem);
          align-items: center;
        }
        .product-photo img { border-radius: 8px; box-shadow: 0 20px 50px rgba(21,26,18,.16); }
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
          font-size: clamp(2.2rem, 5vw, 4rem);
          line-height: .98;
          margin: 0 0 .55rem;
        }
        .product-sub { color: var(--terracotta); font-weight: 800; font-style: italic; margin-bottom: .75rem; }
        .product-desc { color: var(--muted); line-height: 1.7; margin-bottom: 1rem; }
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
        .price { font-family: 'Playfair Display', Georgia, serif; font-weight: 900; font-size: clamp(3rem, 7vw, 5.2rem); line-height: .88; }
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
        }
        div[data-testid="stButton"] > button:hover { background: var(--olive); border-color: var(--olive); color: var(--cream); }
        div[data-testid="stLinkButton"] > a { border-radius: 999px; font-weight: 900; }

        .editorial-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1rem;
        }
        .editorial-card {
          min-height: 250px;
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

        .cart-card, .checkout-card {
          background: var(--paper);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 1.25rem;
        }
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
          .trust-strip, .editorial-grid, .blog-grid { grid-template-columns: 1fr; }
          .trust-item { border-right: 0; border-bottom: 1px solid var(--line); }
          .social-rail { position: static; flex-direction: row; margin: .8rem 0 1rem; }
          .section-head { display: block; }
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
            <a href="#sabores">Sabores</a>
            <a href="#marca">La marca</a>
            <a href="#blog">Blog</a>
            <a href="#pedido" class="nav-cta">Pedir</a>
          </div>
        </nav>
        <aside class="social-rail" aria-label="Redes sociales y blog">
          <a href="https://instagram.com/curcubites" target="_blank" title="Instagram">IG</a>
          <a href="https://www.tiktok.com/search?q=curcubites" target="_blank" title="TikTok">TK</a>
          <a href="#blog" title="Blog">BL</a>
          <a href="#pedido" title="Pedido">WA</a>
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
              <h1>El snack que se ve bien y sabe mejor.</h1>
              <p>
                Chips de plátano horneadas con cúrcuma y pimienta negra.
                Una marca pensada para antojos reales, momentos activos y pedidos fáciles por WhatsApp.
              </p>
              <div class="hero-actions">
                <a class="btn-main" href="#sabores">Ver sabores</a>
                <a class="btn-soft" href="#marca">Conocer la marca</a>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with image_col:
        if image.exists():
            st.markdown('<div class="hero-card-img">', unsafe_allow_html=True)
            st.image(str(image), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)


def render_trust_strip() -> None:
    st.markdown(
        """
        <div class="trust-strip">
          <div class="trust-item"><strong>Horneadas</strong><span>No fritas, sin aceite extra.</span></div>
          <div class="trust-item"><strong>Ingredientes claros</strong><span>Plátano, cúrcuma y pimienta.</span></div>
          <div class="trust-item"><strong>Compra simple</strong><span>Carrito y confirmación por WhatsApp.</span></div>
          <div class="trust-item"><strong>Marca local</strong><span>Diseñada para Colombia.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_products(products: list[dict]) -> None:
    st.markdown(
        """
        <section id="sabores" class="section-band">
          <div class="section-head">
            <div>
              <div class="section-kicker">Nuestros sabores</div>
              <h2 class="section-title">Elige el que va contigo.</h2>
            </div>
            <p class="section-copy">
              Tres perfiles para diferentes antojos. Sin pago online: armas tu carrito
              y confirmamos disponibilidad y entrega por WhatsApp.
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
                    st.markdown('<div class="product-photo">', unsafe_allow_html=True)
                    st.image(str(img_path), use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            with info_col:
                st.markdown(
                    f"""
                    <span class="flavor-tag" style="background:{product.get('badge_color', '#245C2A')}">{product['flavor_tag']}</span>
                    <h3 class="product-title">{product['name']}</h3>
                    <div class="product-sub">{product['tagline']}</div>
                    <p class="product-desc">{product['description']}</p>
                    <span class="ingredient-pill">{product['ingredients']}</span>
                    <div class="price">{money(int(product['price']))}</div>
                    <div class="price-note">por bolsa · 13 g · pedido por WhatsApp</div>
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
              <h2 class="section-title">No vendemos bolsitas. Construimos antojos memorables.</h2>
            </div>
            <p class="section-copy">
              Curcubites combina producto, empaque y experiencia digital.
              La idea es sencilla: que el snack se entienda rápido, se vea apetitoso
              y sea fácil de pedir desde cualquier celular.
            </p>
          </div>
          <div class="editorial-grid">
            <article class="editorial-card dark">
              <h3>Natural sin verse aburrido.</h3>
              <p>El verde comunica origen. El dorado de la cúrcuma abre apetito. El contraste oscuro da presencia premium.</p>
            </article>
            <article class="editorial-card">
              <h3>Pedido sin fricción.</h3>
              <p>La página lleva al usuario del sabor al WhatsApp sin crear cuentas, pagos complejos ni pasos innecesarios.</p>
            </article>
            <article class="editorial-card">
              <h3>Contenido que vende.</h3>
              <p>Sabores, momentos de consumo, ingredientes y blog trabajan juntos para que la marca se sienta seria.</p>
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
            </article>
            <article class="blog-card">
              <span>Estilo de vida</span>
              <h3>Snacks para llevar a la U, oficina o gimnasio</h3>
              <p>Pequeños rituales para resolver el antojo sin complicarse la vida.</p>
            </article>
            <article class="blog-card">
              <span>Marca</span>
              <h3>Cómo se diseñó la identidad de Curcubites</h3>
              <p>Color, empaque y tono pensados para vender desde la primera mirada.</p>
            </article>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_checkout(products: list[dict]) -> None:
    items = cart_items(products)
    st.markdown(
        """
        <section id="pedido" class="section-band">
          <div class="section-head">
            <div>
              <div class="section-kicker">Pedido</div>
              <h2 class="section-title">Finaliza por WhatsApp.</h2>
            </div>
            <p class="section-copy">
              Sin pago online. Preparas el mensaje, lo envías y coordinamos entrega.
            </p>
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
            st.markdown('<div class="notice">Confirmación y entrega por WhatsApp.</div>', unsafe_allow_html=True)
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
    render_products(products)
    render_brand_story()
    render_moments()
    render_blog()
    render_checkout(products)
    render_footer()


if __name__ == "__main__":
    main()
