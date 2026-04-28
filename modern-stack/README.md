# Graph2Plan Modern Stack (Blueprint)

Cette branche propose une base **moderne** inspirée du fonctionnement du repo historique :

- `DataPreparation` ➜ pipeline de données versionné et testable.
- `Network` ➜ module d'entraînement isolé.
- `PostProcess` ➜ service de génération via API.
- `Interface` ➜ frontend découplé consommant l'API.

## Choix techniques

- **Python 3.12**
- **FastAPI + Pydantic v2** pour l'API.
- **PyTorch 2.x** pour entraînement/inférence.
- **uv** pour la gestion d'environnement.
- **Ruff + MyPy + Pytest** pour qualité.
- **Docker Compose** pour exécution locale.

## Structure proposée

```text
modern-stack/
  src/g2p_modern/
    api/         # endpoints HTTP
    core/        # contrats, schémas, service d'orchestration
    training/    # entrée entraînement
  tests/
  pyproject.toml
  docker-compose.yml
  Makefile
```

## Démarrage rapide

```bash
cd modern-stack
uv sync
uv run uvicorn g2p_modern.api.main:app --reload --app-dir src
```

## Roadmap de migration (depuis le repo legacy)

1. Migrer les schémas de données `.mat/.pkl` vers un format canonique (`parquet + metadata.json`).
2. Extraire la logique de retrieval dans `core/retrieval.py` avec tests unitaires.
3. Encapsuler le post-traitement Matlab derrière une interface, puis ajouter un fallback Python.
4. Exposer des endpoints `/v1/retrieve` et `/v1/generate` compatibles frontend.
5. Ajouter CI (lint, typecheck, tests, build image).


## API disponible

- `GET /health`
- `POST /v1/retrieve` (retrieval simple basé sur signature de boundary)
- `POST /v1/generate` (stub de génération, migration progressive)


Voir aussi `TESTING.md` pour un guide pas-à-pas de validation locale.


Pour copier localement cette stack, voir la section **0) Copier `modern-stack` en local** dans `TESTING.md`.
