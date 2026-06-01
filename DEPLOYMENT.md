# Despliegue gratis en Streamlit Cloud

## Archivos que se suben

Este repo esta empacado para subir solo lo necesario:

- `app.py`: aplicacion principal.
- `requirements.txt`: dependencias.
- `.streamlit/config.toml`: tema visual.
- `.streamlit/secrets.example.toml`: ejemplo de configuracion, sin secretos reales.
- `data/products.json`: catalogo editable.
- `ig_posts/*.jpg` y `curcubites_concept_1_crujiente_sin_culpa.jpg`: imagenes usadas por la app.
- `.github/workflows/streamlit-smoke.yml`: prueba gratis en GitHub Actions.
- `README.md` y `plan.md`: documentacion.

No se suben PDFs, borradores, entorno virtual, caches ni secretos.

## Pasos

1. Crear repo publico gratis en GitHub: `curcubites-web`.
2. Ejecutar:

```bash
git push -u origin main
```

3. Abrir `https://share.streamlit.io`.
4. Conectar GitHub.
5. Elegir:

```text
Repository: danielhcertuche/curcubites-web
Branch: main
Main file path: app.py
```

6. Deploy.

## Secrets opcionales

Para WhatsApp directo:

```toml
WHATSAPP_NUMBER = "573001234567"
ORDER_EMAIL = "ventas@curcubites.com"
```

Si no configuras `WHATSAPP_NUMBER`, la app sigue funcionando gratis: abre WhatsApp con el mensaje listo.

## Checklist antes de publicar

- Revisar precios en `data/products.json`.
- Cambiar numero de WhatsApp en secrets de Streamlit.
- Abrir app local y probar agregar al carrito.
- Confirmar que el boton de WhatsApp genera el mensaje correcto.
