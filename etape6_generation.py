import requests

def construire_prompt(question, documents):
    extraits = ""

    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "inconnue")
        page = doc.metadata.get("page", "?")

        extraits += (
            f"\nExtrait {i} - Source : {source}, page {page}\n"
            f"{doc.page_content}\n"
        )

    prompt = f"""CONSIGNE :
Tu es un assistant pour les salariés d'Altéa Services.
Réponds uniquement à partir des extraits fournis.
Indique les sources utilisées.
Si les extraits ne permettent pas de répondre,
dis que tu ne disposes pas de l'information.

EXTRAITS :
{extraits}

QUESTION :
{question}

RÉPONSE :
"""
    return prompt


def generer_reponse(question, base_propre):
    from etape5_recherche import rechercher

    resultats = rechercher(question, base_propre, k=3)
    documents = [doc for doc, score in resultats]

    prompt = construire_prompt(question, documents)

    reponse = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=180
    )

    reponse.raise_for_status()
    return reponse.json()["response"]
