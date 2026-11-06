# Assistant RAG — Altéa Services

## Objectif
Développer un assistant documentaire utilisant le RAG
(Retrieval-Augmented Generation) pour répondre aux questions
des salariés à partir des documents internes d'Altéa Services.

## Technologies
- Python
- Google Colab
- ChromaDB : base vectorielle
- Sentence Transformers : embeddings
- Ollama avec le modèle qwen2.5:1.5b
- Streamlit : interface utilisateur

## Installation
Installer les bibliothèques Python :

```bash
pip install -r requirements.txt
```

Installer Ollama séparément, puis télécharger le modèle :

```bash
ollama pull qwen2.5:1.5b
```

## Fonctionnement
1. Charger les documents RH, IT et généraux.
2. Nettoyer les textes.
3. Découper les textes en chunks.
4. Créer les embeddings et la base Chroma.
5. Rechercher les passages pertinents.
6. Générer une réponse avec Ollama.
7. Évaluer les réponses.
8. Afficher les réponses dans Streamlit.

## Lancement
Après avoir préparé la base vectorielle et démarré Ollama :

```bash
streamlit run app.py
```

Remarque : les scripts de préparation de la base vectorielle
doivent encore être ajoutés au dépôt pour permettre une
installation complète depuis zéro.

## Exemple de question
Question : Combien de jours de télétravail sont autorisés ?

Réponse attendue : Jusqu'à 2 jours par semaine pour les
salariés éligibles.

Source : teletravail.pdf, page 1.

## Résultats de l'évaluation
Évaluation sur 10 questions :

- Réussite de la recherche documentaire : 100 %
- Réponses justes : 30 %
- Réponses partielles : 60 %
- Réponses fausses : 10 %
- Réponses explicitement sourcées : 0 %

## Limites connues
- Le modèle peut générer des réponses incorrectes.
- Certaines réponses sont incomplètes.
- Les sources ne sont pas toujours citées dans le texte généré.
- La gestion des droits d'accès n'est pas implémentée.
- La mise à jour automatique des documents n'est pas prévue.
- Le prototype nécessite Ollama et une base vectorielle préparée.

## Auteur
Projet réalisé dans le cadre du TP RAG en entreprise.
