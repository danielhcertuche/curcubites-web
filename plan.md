# Plan de sitio web — Curcubites (Streamlit)

## Resumen

Plan para construir un sitio web funcional para Curcubites, desplegado en Streamlit Community Cloud (gratuito) y gestionado desde GitHub. MVP incluye: Inicio, Productos y Carrito de compras totalmente funcional (pedido/checkout simulado o integración de pago opcional).

## Objetivos

- Entregar sitio web simple, centrado en conversión (vender).
- Publicar en Streamlit Cloud desde repo GitHub (https://github.com/danielhcertuche).
- Mantener despliegue gratuito y escalable para futuras integraciones (Stripe, dominio propio, IA gratuita adicional).

## Entregables

- Archivo `plan.md` (este documento).
- Código fuente listo en este repo: `app.py`, `requirements.txt`, `data/products.json`, `static/`.
- Despliegue en Streamlit Community Cloud (link público) tras tu autorización.
- Guía de uso y pasos para producción, incl. instrucciones para integrar pagos.

## Alcance MVP (funcionalidades mínimas)

- Página Inicio: hero + CTA (activar notificaciones / seguir IG) + beneficios breves.
- Sección Productos: listado visual con imágenes, precio, y botón "Agregar al carrito".
- Carrito de compras: ver items, cambiar cantidades, eliminar items, ver total.
- Checkout mínimo: formulario de contacto + resumen de pedido que envía por email/WhatsApp o redirige a Stripe Checkout si se proveen claves.
- Persistencia de carrito por sesión (Streamlit `st.session_state`).

## Requisitos y recursos necesarios

- Contenido: fotos de producto, nombres, descripciones cortas, precios, stock (archivo CSV/JSON o carpeta `static/images/`).
- Acceso GitHub (tu repo o permiso para crear/push). Link sugerido: https://github.com/danielhcertuche
- (Opcional) Claves de Stripe/PayPal para habilitar pagos reales.

## Stack tecnológico recomendado

- Python 3.10+
- Streamlit (app multipágina o control de navegación manual).
- Librerías: `streamlit`, `pandas` (opcional), `Pillow` (imágenes), `python-dotenv` (variables de entorno), `requests` (si se conecta a APIs).
- Deploy: Streamlit Community Cloud (gratis) conectado al repo GitHub.

## Estructura de proyecto propuesta

```
valen/
├─ app.py                # entrada Streamlit
├─ requirements.txt
├─ data/
│  └─ products.json
├─ static/
│  └─ images/
├─ utils/
│  └─ cart.py
├─ plan.md               # este archivo
└─ README.md
```

## Implementación técnica (carrito)

- Productos en `data/products.json` (id, title, price, image, sku, description).
- Al agregar al carrito: actualizar `st.session_state['cart']` con items {id, qty, price}.
- Funciones básicas: `add_item()`, `remove_item()`, `update_qty()`, `cart_total()`.
- Checkout:
  - Opción A (recomendada para MVP gratuito): generar resumen y boton "Enviar pedido" que abre WhatsApp con mensaje prellenado o envía email con `mailto:`. No requiere claves.
  - Opción B (opcional): Stripe Checkout -> requiere claves públicas/secretas y configuración en Stripe. Podemos dejar integrado en código pero inhabilitado hasta que nos des claves.

## Diseño y UX

- Enfocar en conversión: hero con oferta clara, producto en contexto, CTA visible.
- Componentes: tarjetas de producto, modal/side-drawer para carrito, botones con microcopy orientado a compra.
- Revisión UI/UX: usar `ui-ux-pro-max-skill` para pulir layout, copy y CTA antes del despliegue público.

## Fases y cronograma estimado (orientativo)

1. Fase 0 — Planificación (esta entrega): `plan.md`, confirmación de assets y acceso. (0.5 día)
2. Fase 1 — Scaffold y MVP local: estructura, `app.py`, catálogo JSON, carrito básico, checkout vía WhatsApp/email. (1–2 días)
3. Fase 2 — Diseño y polish: UI/UX review, ajustes visuales, tests. (0.5–1 día)
4. Fase 3 — Integración GitHub y despliegue en Streamlit Cloud. (0.5 día)
5. Fase 4 — Opcionales: Stripe, dominio personalizado, IA gratuita para copy/product recommendations. (1–2 días extra)

## Integración con GitHub y despliegue Streamlit

- Flujo recomendado:
  1. Crear repo `curcubites-web` en tu cuenta o usar existente en https://github.com/danielhcertuche.
  2. Hacer push del código (branch `main` o `streamlit`).
  3. En Streamlit Cloud: conectar repo → seleccionar `app.py` como entrypoint → desplegar.
- Necesitaré tu autorización para clonar/push/crear el repo desde mi entorno. Hasta entonces trabajo localmente y muestro cambios.

## QA y pruebas

- Probar flujo completo localmente (`streamlit run app.py`) y validar:
  - Añadir/quitar items, actualizar cantidades.
  - Generación de resumen de pedido.
  - Envío vía WhatsApp/mail.
- Tests manuales de UX: mobile-first (Streamlit se ve en móvil), velocidad de carga de imágenes.

## Opciones para IA gratuita y dominio personalizado

- IA gratuita: usar OpenAI/GPT-free wrappers o servicios que permitan prompts para copy/product descriptions. Mantener integración opcional para evitar keys.
- Dominio personalizado: requiere compra/registro y configuración DNS que apunte al servicio que usemos (Streamlit Cloud soporta CNAME en planes pagados; la opción gratuita puede requerir redirección o usar un proxy).

## Requerimientos para avanzar (qué necesito de ti)

- Confirmación de que sigas con este plan.
- Carpeta de assets (imágenes) o autorización para usar las imágenes que ya están en repo `ig_posts/`.
- Indicar si quieres checkout real con Stripe (si sí, enviar credenciales de test/live luego).
- Permiso para crear/usar repo en https://github.com/danielhcertuche o instrucciones para enviar PR.

## Siguientes pasos propuestos

1. Confirmas plan y me das permiso para crear/committear código en repo.
2. Yo scaffold proyecto localmente y te muestro preview (link local + instrucciones para ejecutar).
3. Tras tu OK, conectamos repo a Streamlit Cloud y desplegamos público.

---

*Archivo creado automáticamente. Pide cambios o detalles y los incorporo.*
