# Projet Polyvalent — Demo & API (SysWatch / API-Bibli / Controle)

Ce dépôt contient plusieurs modules pédagogiques et utilitaires :
- Un mini-monitor système (demo/syswatch) avec collecte, affichage, export CSV/JSON et stockage SQLite.
- Une API REST de gestion de bibliothèque (api-bibli) basée sur FastAPI avec routes, services et schémas.
- Des scripts d'exercices pour la partie "controle" (manipulation de données, classes véhicules, etc.).

## Arborescence (extraits)
- demo/
  - main.py — lance la démo syswatch ([demo/main.py](demo/main.py))
  - syswatch/
    - collector.py — collecte des métriques ([demo/syswatch/collector.py](demo/syswatch/collector.py))
    - models.py — dataclasses et collecteur ([demo/syswatch/models.py](demo/syswatch/models.py))
    - database.py — stockage SQLite ([demo/syswatch/database.py](demo/syswatch/database.py))
    - traitement.py — export CSV/JSON ([demo/syswatch/traitement.py](demo/syswatch/traitement.py))
    - stats.py — analyse CSV ([demo/syswatch/stats.py](demo/syswatch/stats.py))
    - syswatch_v1.py .. syswatch_v4.py — interfaces/CLI d'évolution ([demo/syswatch/syswatch_v2.py](demo/syswatch/syswatch_v2.py))
    - syswatch_data.csv — échantillon de données ([demo/syswatch/syswatch_data.csv](demo/syswatch/syswatch_data.csv))
- api-bibli/
  - app/main.py — application FastAPI ([api-bibli/app/main.py](api-bibli/app/main.py))
  - app/routers/ — routes API (books, authors, loans, stats) ([api-bibli/app/routers/stats_router.py](api-bibli/app/routers/stats_router.py))
  - app/services/ — logique métier (BookService, LoanService, StatsService...) ([api-bibli/app/services/stats_service.py](api-bibli/app/services/stats_service.py))
  - app/schemas/ — Pydantic / validation ([api-bibli/app/schemas/book.py](api-bibli/app/schemas/book.py))
  - app/data/orm.py — ORM async SQLAlchemy ([api-bibli/app/data/orm.py](api-bibli/app/data/orm.py))
  - tests/ — tests unitaires (fastapi TestClient mocks) ([api-bibli/tests/test_book_router.py](api-bibli/tests/test_book_router.py))
  - requirements.txt, pyproject.toml, pytest.toml
- controle/
  - vehicule.py, models.py, commandes.py, unpacking.py (exercices) ([controle/vehicule.py](controle/vehicule.py))

## Usage rapide

1. Demo SysWatch (local)
   - Python 3.x avec psutil installé.
   - Lancer la démo (v2) :
     ```sh
     python demo/main.py
     ```
   - Options CLI (ex. continuer, intervalle, stats) disponibles dans [demo/syswatch/syswatch_v4.py](http://_vscodecontentref_/0) / [demo/syswatch/syswatch_v3.py](http://_vscodecontentref_/1).

2. API bibliothéque (développement)
   - Installer dépendances : voir [api-bibli/requirements.txt](http://_vscodecontentref_/2)
   - Lancer avec uvicorn :
     ```sh
     uvicorn app.main:app --reload --app-dir api-bibli/app
     ```
   - Routes principales :
     - /api/v1/books, /api/v1/authors, /api/v1/loans, /api/v1/stats
     - Exemple d'export CSV : [api-bibli/app/routers/stats_router.py](http://_vscodecontentref_/3)

3. Tests
   - Depuis le dossier api-bibli :
     ```sh
     pytest
     ```

## Fichiers / symboles importants (sélection)
- Collecte et affichage système :
  - [collect_all_info](http://_vscodecontentref_/4)
  - [SystemCollector.collect](http://_vscodecontentref_/5)
  - [MetricsDatabase.save](http://_vscodecontentref_/6)
  - [export_csv](http://_vscodecontentref_/7)
  - [calculer_moyennes](http://_vscodecontentref_/8)
- API / services :
  - [StatsService.get_global_stats](http://_vscodecontentref_/9)
  - [LoanService.create_loan](http://_vscodecontentref_/10)
  - [BookService.get_all_filtered](http://_vscodecontentref_/11)
  - Routes : [api-bibli/app/routers/book_router.py](http://_vscodecontentref_/12), [api-bibli/app/routers/loan_router.py](http://_vscodecontentref_/13), [api-bibli/app/routers/author_router.py](http://_vscodecontentref_/14), [api-bibli/app/routers/stats_router.py](http://_vscodecontentref_/15)

## Contribution
- Suivre les patterns existants : séparation routers/services/schemas.
- Tests unitaires : voir [api-bibli/tests](http://_vscodecontentref_/16).

## Licences & notes
- Dépôt pédagogique — adapter licences en fonction de vos besoins.
- Certains fichiers de configuration et dépendances sont fournis dans [api-bibli/requirements.txt](http://_vscodecontentref_/17).