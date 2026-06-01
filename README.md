# Curcubites Web

Pagina de venta en Streamlit para Curcubites.

## Costo

- Hosting: Streamlit Community Cloud gratis.
- Codigo: GitHub publico gratis.
- Pedidos: WhatsApp/mailto gratis, sin pasarela paga.
- Pagos reales: no incluidos en el MVP para evitar costos y llaves privadas.

## Ejecutar local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Configuracion opcional

Para que el boton de WhatsApp vaya directo al vendedor, configura una variable o secreto:

```toml
WHATSAPP_NUMBER = "573001234567"
ORDER_EMAIL = "ventas@curcubites.com"
```

Si no existe `WHATSAPP_NUMBER`, la app abre WhatsApp con el mensaje listo para elegir contacto.

## Editar productos

Modifica precios, nombres e imagenes en `data/products.json`.

## Desplegar gratis en Streamlit Cloud

1. Sube este repo a GitHub.
2. Entra a `https://share.streamlit.io`.
3. Conecta el repo.
4. Selecciona `app.py` como archivo principal.
5. Deploy.
