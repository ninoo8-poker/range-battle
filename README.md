# Range Battle — Streamlit

## Tester en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Puis ouvrir l'adresse affichée par Streamlit.

## Déployer avec Streamlit Community Cloud

1. Mettre `app.py` et `requirements.txt` dans un repository GitHub.
2. Aller sur https://share.streamlit.io/
3. Se connecter avec GitHub.
4. `Create app` → choisir le repository.
5. Branch : `main`
6. Main file path : `app.py`
7. Deploy.

L'application sera disponible sur une adresse `streamlit.app`.

## Données

Les ranges sont actuellement dans `DATA` dans `app.py`.
Les captures 50bb LJ/HJ/CO ont servi à créer une première base de test.
Les autres positions et les ranges 100bb doivent être ajoutés à partir de tes captures.
