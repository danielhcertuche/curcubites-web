# Despliegue en Streamlit Cloud

## Archivos en el repo

- `app.py` — aplicación principal
- `requirements.txt` — dependencias (`streamlit==1.45.1`)
- `.streamlit/config.toml` — tema de marca (verde #245C2A, crema #FFF6E6)
- `.streamlit/secrets.example.toml` — plantilla de secretos, sin valores reales
- `data/products.json` — catálogo editable (3 SKUs: Original, Picante, Dulce)
- `imgenes_finales/` — fotos reales del producto (lifestyle + estudio)
- `imgenes_finales/logo_curcubites_hq.svg` — logo vectorial generado
- `curcubites_concept_1_crujiente_sin_culpa_original_borde_verde.jpg` — imagen Dulce

No se suben: `.venv/`, `__pycache__/`, `secrets.toml`, PDFs, borradores.

## Pasos para deploy

1. Push al repo:

```bash
git push origin main
```

2. Abrir [share.streamlit.io](https://share.streamlit.io)
3. Conectar GitHub
4. Configurar:

```
Repository : danielhcertuche/curcubites-web
Branch     : main
Main file  : app.py
```

5. Deploy

## Secrets en Streamlit Cloud

App → Settings → Secrets:

```toml
WHATSAPP_NUMBER = "573008901210"
ORDER_EMAIL     = "ventas@curcubites.com"
```

`WHATSAPP_NUMBER` ya está hardcodeado como fallback en el código — la app funciona sin configurar el secret. El secret permite cambiarlo sin tocar el código.

## Checklist pre-deploy

- [ ] Precios correctos en `data/products.json`
- [ ] WhatsApp number confirmado: 300 890 1210
- [ ] Prueba local: agregar al carrito → checkout → mensaje WhatsApp
- [ ] Prueba: botón "Pedir" lleva a sección de productos
- [ ] Prueba: cart badge muestra conteo al agregar ítems
- [ ] Secrets configurados en Streamlit Cloud
