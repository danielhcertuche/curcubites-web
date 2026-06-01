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
        return
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


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
          --verde: #245C2A;
          --verde-hover: #1a4320;
          --curcuma: #D99A22;
          --terracota: #A85232;
          --crema: #FFF6E6;
          --negro: #151A12;
          --gris: rgba(21,26,18,0.65);
          --verde-suave: #E7F1DF;
          --linea: #E6D8BF;
        }

        .stApp {
          background: var(--crema);
        }

        [data-testid="stSidebar"] {
          background: var(--negro);
          border-right: 1px solid rgba(255,255,255,0.06);
        }

        [data-testid="stSidebar"] * {
          color: #FFF6E6 !important;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] > button {
          border-color: rgba(255,255,255,0.18) !important;
          background: rgba(255,255,255,0.07) !important;
          color: #FFF6E6 !important;
          font-weight: 600 !important;
        }

        [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
          background: rgba(255,255,255,0.14) !important;
        }

        .block-container {
          max-width: 1180px;
          padding-top: 1.5rem;
          padding-bottom: 4rem;
        }

        /* ── EYEBROW ── */
        .eyebrow {
          display: inline-block;
          background: var(--verde-suave);
          color: var(--verde);
          font-size: 0.76rem;
          font-weight: 800;
          letter-spacing: 2px;
          text-transform: uppercase;
          padding: 0.3rem 0.8rem;
          border-radius: 999px;
          margin-bottom: 1.1rem;
        }

        /* ── HERO ── */
        .hero-h1 {
          font-size: clamp(3.2rem, 8vw, 6.2rem);
          font-weight: 900;
          line-height: 0.9;
          color: var(--negro);
          margin: 0 0 1rem;
          letter-spacing: -2px;
        }

        .hero-claim {
          color: var(--gris);
          font-size: 1.08rem;
          line-height: 1.68;
          max-width: 38rem;
          margin: 0 0 1.4rem;
        }

        .hero-pills {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-bottom: 1.6rem;
        }

        .hero-pill {
          border: 1.5px solid var(--linea);
          border-radius: 999px;
          padding: 0.35rem 0.85rem;
          font-size: 0.83rem;
          font-weight: 600;
          color: var(--negro);
          background: rgba(255,255,255,0.72);
        }

        /* ── TRUST BAR ── */
        .trust-bar {
          background: var(--negro);
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: space-around;
          flex-wrap: wrap;
          gap: 0.5rem;
          padding: 1rem 1.5rem;
          margin: 1.6rem 0 2.4rem;
        }

        .trust-item {
          color: #FFF6E6;
          font-size: 0.84rem;
          font-weight: 700;
          text-align: center;
          padding: 0.2rem 0.4rem;
        }

        .trust-item span {
          display: block;
          font-size: 0.71rem;
          opacity: 0.52;
          font-weight: 400;
          margin-top: 0.12rem;
        }

        /* ── SECTION TITLES ── */
        .section-title {
          font-size: clamp(1.8rem, 4vw, 2.6rem);
          font-weight: 900;
          color: var(--negro);
          line-height: 1.05;
          margin: 0 0 0.4rem;
          letter-spacing: -0.5px;
        }

        .section-copy {
          color: var(--gris);
          font-size: 0.97rem;
          margin-bottom: 1.6rem;
        }

        /* ── PRODUCT CARDS ── */
        .flavor-bar {
          border-radius: 8px 8px 0 0;
          color: #fff;
          font-size: 0.68rem;
          font-weight: 900;
          letter-spacing: 3px;
          text-align: center;
          padding: 0.38rem;
          text-transform: uppercase;
          margin-bottom: 0;
        }

        .product-badge {
          font-size: 0.74rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin: 0.65rem 0 0.2rem;
        }

        .product-name {
          font-size: 1.3rem;
          font-weight: 900;
          color: var(--negro);
          margin: 0 0 0.18rem;
        }

        .product-tagline {
          font-size: 0.88rem;
          color: var(--gris);
          margin: 0 0 0.45rem;
        }

        .product-desc {
          font-size: 0.86rem;
          color: rgba(21,26,18,0.74);
          margin: 0 0 0.65rem;
          line-height: 1.5;
        }

        .product-ingredients {
          font-size: 0.77rem;
          color: var(--verde);
          font-weight: 600;
          margin: 0 0 0.45rem;
        }

        .product-price {
          font-size: 2rem;
          font-weight: 900;
          color: var(--negro);
          line-height: 1;
          margin: 0.45rem 0 0.12rem;
        }

        .product-weight {
          font-size: 0.76rem;
          color: rgba(21,26,18,0.44);
          margin: 0 0 0.5rem;
        }

        /* ── BUTTONS ── */
        div[data-testid="stButton"] > button {
          border-radius: 8px;
          border: 2px solid var(--verde);
          background: var(--verde);
          color: #FFF6E6;
          font-weight: 800;
          font-size: 0.9rem;
          min-height: 2.75rem;
          transition: background 0.14s, border-color 0.14s, transform 0.1s;
        }

        div[data-testid="stButton"] > button:hover {
          border-color: var(--verde-hover);
          background: var(--verde-hover);
          transform: translateY(-1px);
        }

        div[data-testid="stLinkButton"] > a {
          border-radius: 8px;
          font-weight: 800;
        }

        /* ── INGREDIENTS ── */
        .ingredient-card {
          background: #fff;
          border: 1px solid var(--linea);
          border-radius: 12px;
          padding: 1.3rem;
          text-align: center;
          height: 100%;
        }

        .ingredient-icon {
          font-size: 2.1rem;
          margin-bottom: 0.5rem;
        }

        .ingredient-name {
          font-weight: 800;
          color: var(--negro);
          font-size: 1rem;
          margin: 0 0 0.28rem;
        }

        .ingredient-desc {
          font-size: 0.84rem;
          color: var(--gris);
          margin: 0;
          line-height: 1.45;
        }

        /* ── OCCASIONS ── */
        .occasion-chip {
          background: var(--verde-suave);
          border: 1px solid #c8ddc2;
          border-radius: 12px;
          padding: 0.8rem 0.5rem;
          text-align: center;
          font-weight: 700;
          color: var(--verde);
          font-size: 0.88rem;
          line-height: 1.5;
        }

        /* ── CHECKOUT ── */
        .checkout-notice {
          background: var(--verde-suave);
          border: 1px solid #c8ddc2;
          border-radius: 10px;
          padding: 0.85rem 1.1rem;
          color: var(--verde);
          font-size: 0.87rem;
          font-weight: 600;
          margin-bottom: 1.2rem;
        }

        .order-summary {
          background: #fff;
          border: 1px solid var(--linea);
          border-radius: 10px;
          padding: 1rem 1.25rem;
          margin-bottom: 1.2rem;
        }

        /* ── FOOTER ── */
        .site-footer {
          border-top: 1px solid var(--linea);
          padding: 2rem 0 1rem;
          margin-top: 2rem;
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          flex-wrap: wrap;
          gap: 1rem;
          color: var(--gris);
          font-size: 0.86rem;
        }

        .site-footer strong {
          color: var(--negro);
          font-size: 0.97rem;
        }

        .site-footer a {
          color: var(--verde);
          text-decoration: none;
          font-weight: 600;
        }

        @media (max-width: 768px) {
          .hero-h1 { font-size: 3rem; letter-spacing: -1px; }
          .trust-bar { flex-direction: column; }
          .site-footer { flex-direction: column; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    col_copy, col_img = st.columns([1.1, 0.9], vertical_alignment="center")
    with col_copy:
        st.markdown(
            """
            <div class="eyebrow">Horneadas · Sin freír · Con cúrcuma</div>
            <h1 class="hero-h1">Curcubites</h1>
            <p class="hero-claim">
              Chips de plátano horneados con cúrcuma y pimienta negra.
              Crujiente real, ingredientes de verdad, sin fritura y sin drama.
            </p>
            <div class="hero-pills">
              <span class="hero-pill">🌿 Plátano + cúrcuma</span>
              <span class="hero-pill">⚫ Pimienta negra</span>
              <span class="hero-pill">13 g por bolsa</span>
              <span class="hero-pill">Pedido por WhatsApp</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Pedir ahora →", "#sabores", use_container_width=False)
    with col_img:
        hero_img = BASE_DIR / "imgenes_finales" / "55d95c75-98ae-4418-a4df-c4689f51441c.jpeg"
        if hero_img.exists():
            st.image(str(hero_img), use_container_width=True)


def render_trust_bar() -> None:
    st.markdown(
        """
        <div class="trust-bar">
          <div class="trust-item">🔥 Horneadas<span>No fritas</span></div>
          <div class="trust-item">🌿 Ingredientes reales<span>Sin aditivos artificiales</span></div>
          <div class="trust-item">📦 13 g por bolsa<span>Tamaño perfecto para el antojo</span></div>
          <div class="trust-item">💬 Pedido por WhatsApp<span>Sin pago online</span></div>
          <div class="trust-item">🇨🇴 Hecho en Colombia<span>Producción local</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_products(products: list[dict]) -> None:
    st.markdown('<h2 id="sabores" class="section-title">Elige tu sabor</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">3 sabores · 13 g por bolsa · Pedido por WhatsApp · Sin pago online</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="large")
    for col, p in zip(cols, products):
        with col:
            st.markdown(
                f'<div class="flavor-bar" style="background:{p["badge_color"]}">{p["flavor_tag"]}</div>',
                unsafe_allow_html=True,
            )
            img_path = BASE_DIR / p["image"]
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            st.markdown(
                f"""
                <p class="product-badge" style="color:{p['badge_color']}">{p['badge']}</p>
                <p class="product-name">{p['name']}</p>
                <p class="product-tagline">{p['tagline']}</p>
                <p class="product-desc">{p['description']}</p>
                <p class="product-ingredients">🌿 {p['ingredients']}</p>
                <div class="product-price">{money(int(p['price']))}</div>
                <p class="product-weight">por bolsa · 13 g</p>
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
                label_visibility="collapsed",
            )
            total_line = money(int(p["price"]) * int(qty))
            if st.button(
                f"Agregar {int(qty)} — {total_line}",
                key=f"add_{p['id']}",
                use_container_width=True,
            ):
                add_to_cart(p["id"], int(qty))
                st.toast(f"✓ {p['name']} agregado al carrito")
                st.rerun()


def render_ingredients() -> None:
    st.markdown("---")
    st.markdown('<h2 class="section-title">Ingredientes reales</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Sin saborizantes artificiales. Lo que lees en el empaque es lo que comes.</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="large")
    data = [
        ("🍌", "Plátano", "Base crujiente, horneado sin freír. Natural y con fibra."),
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


def render_occasions() -> None:
    st.markdown(
        '<h2 class="section-title" style="margin-top:2rem">Para cada momento</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="section-copy">El snack que cabe en cualquier plan.</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4, gap="medium")
    data = [("🎒", "Universidad"), ("💻", "Trabajo"), ("🏋️", "Post-gym"), ("🛋️", "Plan en casa")]
    for col, (icon, label) in zip(cols, data):
        col.markdown(
            f'<div class="occasion-chip">{icon}<br>{label}</div>',
            unsafe_allow_html=True,
        )


def render_cart(products: list[dict]) -> None:
    with st.sidebar:
        items = cart_items(products)
        st.markdown("## 🛒 Carrito")

        if not items:
            st.markdown("Tu carrito está vacío.")
            st.caption("Elige un sabor y agrégalo para continuar.")
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
        '<h2 class="section-title" style="margin-top:2.5rem">Finaliza tu pedido</h2>',
        unsafe_allow_html=True,
    )

    if not items:
        st.info("Agrega al menos un producto al carrito para continuar.")
        return

    total = cart_total(items)
    rows = "".join(
        f"<tr>"
        f"<td style='padding:0.28rem 0'>{i['qty']} × {i['name']}</td>"
        f"<td style='text-align:right;padding:0.28rem 0;font-weight:700'>{money(i['subtotal'])}</td>"
        f"</tr>"
        for i in items
    )
    st.markdown(
        f"""
        <div class="order-summary">
          <table style="width:100%;border-collapse:collapse;font-size:0.92rem">
            {rows}
            <tr style="border-top:1px solid #E6D8BF">
              <td style="padding:0.5rem 0;font-weight:900;font-size:1.08rem">Total</td>
              <td style="text-align:right;padding:0.5rem 0;font-weight:900;font-size:1.08rem">{money(total)}</td>
            </tr>
          </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="checkout-notice">
          💬 Sin pago online — armas el pedido aquí, lo enviás por WhatsApp y coordinamos la entrega.
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
            placeholder="Horario de entrega, barrio, referencias, sabor favorito…",
        )
        submitted = st.form_submit_button("Preparar pedido →", use_container_width=True)

    if submitted:
        missing = [
            label
            for label, val in {
                "nombre": name,
                "WhatsApp": phone,
                "ciudad": city,
                "dirección": address,
            }.items()
            if not val.strip()
        ]
        if missing:
            st.error(f"Faltan campos obligatorios: {', '.join(missing)}")
            return
        st.session_state.order_message = order_message(
            items, name, phone, city, address, notes
        )

    message = st.session_state.get("order_message")
    if message:
        st.success("✓ Pedido listo. Envíalo por WhatsApp o correo para confirmar.")
        st.code(message, language="text")
        col_w, col_m = st.columns(2)
        col_w.link_button(
            "📲 Enviar por WhatsApp", whatsapp_url(message), use_container_width=True
        )
        col_m.link_button(
            "✉️ Enviar por correo", mailto_url(message), use_container_width=True
        )


def render_faq() -> None:
    st.markdown(
        '<h2 class="section-title" style="margin-top:2.5rem">Preguntas frecuentes</h2>',
        unsafe_allow_html=True,
    )
    faqs = [
        (
            "¿Cuánto pesa cada bolsa?",
            "13 gramos por bolsa. Tamaño ideal para el antojo del día sin pasarse.",
        ),
        (
            "¿Cómo hago el pedido?",
            "Armas el carrito aquí, completas el formulario y nos contactas por WhatsApp. Sin pago online.",
        ),
        (
            "¿Hacen envíos?",
            "Coordinamos la entrega según la ciudad. Escríbenos para confirmar cobertura y tiempos.",
        ),
        (
            "¿Son realmente sin freír?",
            "Sí, todas las Curcubites son horneadas. Sin fritura, sin aceite extra, sin compromiso con el sabor.",
        ),
        (
            "¿Puedo pedir varios sabores en el mismo pedido?",
            "Claro, agrega los sabores que quieras al carrito y hacemos un solo pedido.",
        ),
    ]
    for question, answer in faqs:
        with st.expander(question):
            st.write(answer)


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="site-footer">
          <div>
            <strong>Curcubites</strong><br>
            Chips de plátano horneados con cúrcuma<br>
            Colombia · Pedidos por WhatsApp
          </div>
          <div style="text-align:right">
            <a href="mailto:{DEFAULT_EMAIL}">{DEFAULT_EMAIL}</a><br>
            <span style="font-size:0.78rem;opacity:0.55">Hecho con 🌿 en Colombia</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    ensure_cart()
    inject_styles()
    products = load_products()
    render_cart(products)
    render_hero()
    render_trust_bar()
    render_products(products)
    render_ingredients()
    render_occasions()
    render_checkout(products)
    render_faq()
    render_footer()


if __name__ == "__main__":
    main()
