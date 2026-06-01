import json
import os
from pathlib import Path
from urllib.parse import quote

import streamlit as st


BASE_DIR = Path(__file__).parent
PRODUCTS_PATH = BASE_DIR / "data" / "products.json"
DEFAULT_WHATSAPP = ""
DEFAULT_EMAIL = "ventas@curcubites.com"


st.set_page_config(
    page_title="Curcubites | Chips horneadas",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
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
        return
    st.session_state.cart[product_id] = qty


def cart_items(products: list[dict]) -> list[dict]:
    ensure_cart()
    by_id = {product["id"]: product for product in products}
    items = []
    for product_id, qty in st.session_state.cart.items():
        product = by_id.get(product_id)
        if not product:
            continue
        items.append(
            {
                **product,
                "qty": qty,
                "subtotal": int(product["price"]) * qty,
            }
        )
    return items


def cart_total(items: list[dict]) -> int:
    return sum(item["subtotal"] for item in items)


def order_message(items: list[dict], name: str, phone: str, city: str, address: str, notes: str) -> str:
    lines = [
        "Hola, quiero pedir Curcubites:",
        "",
        *[f"- {item['qty']} x {item['name']} = {money(item['subtotal'])}" for item in items],
        "",
        f"Total: {money(cart_total(items))}",
        "",
        f"Nombre: {name}",
        f"Telefono: {phone}",
        f"Ciudad: {city}",
        f"Direccion: {address}",
    ]
    if notes:
        lines.append(f"Notas: {notes}")
    return "\n".join(lines)


def whatsapp_url(message: str) -> str:
    number = get_secret("WHATSAPP_NUMBER", DEFAULT_WHATSAPP).strip().replace("+", "")
    if number:
        return f"https://wa.me/{number}?text={quote(message)}"
    return f"https://wa.me/?text={quote(message)}"


def mailto_url(message: str) -> str:
    email = get_secret("ORDER_EMAIL", DEFAULT_EMAIL)
    subject = quote("Pedido Curcubites")
    body = quote(message)
    return f"mailto:{email}?subject={subject}&body={body}"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
          --green: #2f7d32;
          --dark: #1e241b;
          --gold: #d59b28;
          --cream: #fff8ec;
          --terracotta: #b95f35;
          --line: rgba(30, 36, 27, 0.14);
        }

        .stApp {
          background:
            radial-gradient(circle at top left, rgba(213, 155, 40, 0.14), transparent 28rem),
            linear-gradient(180deg, #fff8ec 0%, #ffffff 44%, #f8f1e4 100%);
        }

        [data-testid="stSidebar"] {
          background: #1e241b;
        }

        [data-testid="stSidebar"] * {
          color: #fff8ec !important;
        }

        .block-container {
          max-width: 1180px;
          padding-top: 1.5rem;
          padding-bottom: 3rem;
        }

        .hero {
          display: grid;
          grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
          gap: 2rem;
          align-items: center;
          min-height: 72vh;
          padding: 2rem 0 1rem;
        }

        .eyebrow {
          color: var(--terracotta);
          font-size: 0.86rem;
          font-weight: 800;
          letter-spacing: 0;
          margin-bottom: 0.65rem;
          text-transform: uppercase;
        }

        .hero h1 {
          color: var(--dark);
          font-size: clamp(2.6rem, 7vw, 5.8rem);
          line-height: 0.95;
          letter-spacing: 0;
          margin: 0 0 1rem;
        }

        .hero p {
          color: rgba(30, 36, 27, 0.78);
          font-size: 1.15rem;
          line-height: 1.65;
          max-width: 44rem;
        }

        .hero-image img {
          border-radius: 8px;
          box-shadow: 0 28px 70px rgba(30, 36, 27, 0.18);
          width: 100%;
        }

        .pill-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.65rem;
          margin: 1.4rem 0;
        }

        .pill {
          border: 1px solid var(--line);
          border-radius: 999px;
          color: var(--dark);
          font-size: 0.92rem;
          font-weight: 700;
          padding: 0.5rem 0.8rem;
          background: rgba(255,255,255,0.7);
        }

        .section-title {
          color: var(--dark);
          font-size: 2rem;
          line-height: 1.1;
          margin: 2.4rem 0 0.35rem;
        }

        .section-copy {
          color: rgba(30, 36, 27, 0.72);
          margin-bottom: 1.2rem;
        }

        .metric {
          border-left: 4px solid var(--gold);
          padding-left: 0.9rem;
        }

        .metric strong {
          display: block;
          color: var(--dark);
          font-size: 1.3rem;
        }

        .metric span {
          color: rgba(30, 36, 27, 0.68);
          font-size: 0.92rem;
        }

        div[data-testid="stButton"] > button {
          border-radius: 8px;
          border: 1px solid var(--green);
          background: var(--green);
          color: #fff8ec;
          font-weight: 800;
          min-height: 2.8rem;
        }

        div[data-testid="stButton"] > button:hover {
          border-color: #225e25;
          background: #225e25;
          color: #fff8ec;
        }

        div[data-testid="stLinkButton"] > a {
          border-radius: 8px;
          font-weight: 800;
        }

        @media (max-width: 840px) {
          .hero {
            grid-template-columns: 1fr;
            min-height: auto;
          }

          .hero-image {
            order: -1;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    copy_col, image_col = st.columns([1.05, 0.95], vertical_alignment="center")
    with copy_col:
        st.markdown(
            """
            <div class="eyebrow">Horneadas, no fritas</div>
            <h1>Curcubites</h1>
            <p>
              Chips de platano con curcuma y pimienta negra para matar el antojo
              con crujido real, menos grasa y cero drama.
            </p>
            <div class="pill-row">
              <span class="pill">Contiene curcuma</span>
              <span class="pill">Contiene pimienta negra</span>
              <span class="pill">150 g por bolsa</span>
              <span class="pill">Pedido por WhatsApp</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Comprar ahora", "#elige-tu-pedido", use_container_width=False)
    with image_col:
        st.image(str(BASE_DIR / "curcubites_concept_1_crujiente_sin_culpa.jpg"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_metrics() -> None:
    cols = st.columns(3)
    metrics = [
        ("Menos grasa", "Que papas fritas tradicionales"),
        ("Sabor real", "Platano, curcuma y pimienta negra"),
        ("Compra facil", "Armas carrito y pides por WhatsApp"),
    ]
    for col, (title, copy) in zip(cols, metrics):
        col.markdown(f'<div class="metric"><strong>{title}</strong><span>{copy}</span></div>', unsafe_allow_html=True)


def render_products(products: list[dict]) -> None:
    st.markdown('<h2 id="elige-tu-pedido" class="section-title">Elige tu pedido</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Selecciona tu formato, agrega unidades y confirma el pedido en segundos.</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, product in zip(cols, products):
        with col:
            image_path = BASE_DIR / product["image"]
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            st.caption(product["badge"])
            st.subheader(product["name"])
            st.write(product["tagline"])
            st.write(product["description"])
            st.markdown(f"### {money(int(product['price']))}")
            qty = st.number_input(
                "Cantidad",
                min_value=1,
                max_value=24,
                value=1,
                step=1,
                key=f"qty_{product['id']}",
            )
            if st.button("Agregar al carrito", key=f"add_{product['id']}", use_container_width=True):
                add_to_cart(product["id"], int(qty))
                st.toast(f"{product['name']} agregado")
                st.rerun()


def render_cart(products: list[dict]) -> None:
    with st.sidebar:
        st.title("Carrito")
        items = cart_items(products)
        if not items:
            st.info("Tu carrito esta vacio.")
            return

        for item in items:
            st.markdown(f"**{item['name']}**")
            qty = st.number_input(
                "Unidades",
                min_value=0,
                max_value=99,
                value=int(item["qty"]),
                step=1,
                key=f"cart_qty_{item['id']}",
            )
            update_quantity(item["id"], int(qty))
            st.write(f"Subtotal: {money(item['subtotal'])}")
            if st.button("Quitar", key=f"remove_{item['id']}", use_container_width=True):
                remove_from_cart(item["id"])
                st.rerun()
            st.divider()

        st.subheader(f"Total: {money(cart_total(cart_items(products)))}")


def render_checkout(products: list[dict]) -> None:
    items = cart_items(products)
    st.markdown('<h2 class="section-title">Finaliza tu compra</h2>', unsafe_allow_html=True)
    if not items:
        st.warning("Agrega productos al carrito para activar el pedido.")
        return

    with st.form("checkout_form"):
        col_a, col_b = st.columns(2)
        name = col_a.text_input("Nombre completo")
        phone = col_b.text_input("WhatsApp")
        city = col_a.text_input("Ciudad")
        address = col_b.text_input("Direccion de entrega")
        notes = st.text_area("Notas del pedido", placeholder="Horario, barrio, referencias o sabor favorito.")
        submitted = st.form_submit_button("Preparar pedido")

    if submitted:
        missing = [label for label, value in {"nombre": name, "WhatsApp": phone, "ciudad": city, "direccion": address}.items() if not value.strip()]
        if missing:
            st.error("Falta: " + ", ".join(missing))
            return
        st.session_state.order_message = order_message(items, name, phone, city, address, notes)

    message = st.session_state.get("order_message")
    if message:
        st.success("Pedido listo. Envia por WhatsApp o correo.")
        st.code(message, language="text")
        col_w, col_m = st.columns(2)
        col_w.link_button("Enviar por WhatsApp", whatsapp_url(message), use_container_width=True)
        col_m.link_button("Enviar por correo", mailto_url(message), use_container_width=True)


def render_story() -> None:
    st.markdown('<h2 class="section-title">Por que funciona</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        Curcubites entra en momentos donde el antojo pide algo crujiente:
        tarde de trabajo, universidad, post-gym o plan en casa.
        La promesa es simple: platano horneado, curcuma, pimienta negra y una bolsa facil de pedir.
        """
    )


def main() -> None:
    ensure_cart()
    inject_styles()
    products = load_products()
    render_cart(products)
    render_hero()
    render_metrics()
    render_products(products)
    render_checkout(products)
    render_story()


if __name__ == "__main__":
    main()
