# Manifest de paquete

## Listo para subir a GitHub

```text
.github/workflows/streamlit-smoke.yml
.gitignore
.streamlit/config.toml
.streamlit/secrets.example.toml
DEPLOYMENT.md
PACKAGE_MANIFEST.md
README.md
app.py
curcubites_concept_1_crujiente_sin_culpa.jpg
data/products.json
ig_posts/post_1_crujiente_sin_culpa.jpg
ig_posts/post_2_postgym_sin_dramas.jpg
ig_posts/post_3_detalle_que_cambia_todo.jpg
plan.md
requirements.txt
```

## Excluido

```text
.venv/
__pycache__/
.streamlit/secrets.toml
dist/
*.pdf
*.jpeg
CURCUBITES_*.md
generate_*.py
imagenes no usadas por la app
```

## Validacion local

```bash
source .venv/bin/activate
python -m py_compile app.py
streamlit run app.py
```
