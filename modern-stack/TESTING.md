# Tester `modern-stack` rapidement

## 0) Copier `modern-stack` en local

### Option A (recommandée) : cloner le repo puis utiliser la branche moderne

```bash
git clone <URL_DU_REPO> graph2plan
cd graph2plan
git checkout modern-stack-blueprint
cd modern-stack
```

### Option B : copier seulement le dossier `modern-stack`

Depuis le repo existant:

```bash
cp -R modern-stack /chemin/vers/mon/projet/
cd /chemin/vers/mon/projet/modern-stack
```

## 0bis) Si `uv` n'est pas reconnu

Si ton terminal affiche "commande introuvable: uv", tu as 2 options.

### Option 1: installer `uv`

```bash
python -m pip install --user uv
# puis redémarrer le terminal
uv --version
```

### Option 2: continuer sans `uv` (venv + pip)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

Dans ce cas, remplace les commandes `uv run ...` par des commandes Python directes:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src uvicorn g2p_modern.api.main:app --app-dir src --host 0.0.0.0 --port 8080
```

## 1) Pré-requis

- Python 3.12+
- `uv` installé (`pip install uv`)

## 2) Installer les dépendances

```bash
cd modern-stack
uv sync
```

## 3) Lancer les tests unitaires

```bash
PYTHONPATH=src uv run pytest -q
```

Attendu: les tests de `tests/test_health_contract.py` passent.

## 4) Lancer l'API en local

```bash
uv run uvicorn g2p_modern.api.main:app --app-dir src --host 0.0.0.0 --port 8080
```

Puis vérifier:

```bash
curl -s http://127.0.0.1:8080/health
```

Réponse attendue:

```json
{"status":"ok"}
```

## 5) Tester `/v1/retrieve`

```bash
curl -s -X POST http://127.0.0.1:8080/v1/retrieve \
  -H 'content-type: application/json' \
  -d '{
    "boundary": {
      "points": [
        {"x": 0, "y": 0},
        {"x": 10, "y": 0},
        {"x": 0, "y": 10}
      ]
    },
    "k": 3
  }'
```

Réponse attendue (structure):

```json
{
  "candidates": [],
  "meta": {
    "status": "ok",
    "num_loaded_samples": 0
  }
}
```

`num_loaded_samples` dépend de la présence du fichier legacy `Interface/static/Data/data_train_converted.pkl`.

## 6) Tester `/v1/generate`

```bash
curl -s -X POST http://127.0.0.1:8080/v1/generate \
  -H 'content-type: application/json' \
  -d '{
    "boundary": {
      "points": [
        {"x": 0, "y": 0},
        {"x": 10, "y": 0},
        {"x": 0, "y": 10}
      ]
    },
    "constraints": []
  }'
```

Réponse attendue: `meta.status = "stub"`.
