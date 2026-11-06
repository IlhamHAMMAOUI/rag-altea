import streamlit as st
import requests
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

st.set_page_config(
    page_title="Assistant RAG Altéa Services",
    page_icon="📚"
)

st.title("📚 Assistant documentaire Altéa Services")
st.write("Posez une question sur les documents de l'entreprise.")

@st.cache_resource
def charger_base():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma(
        collection_name="altea_upsert_test",
        persist_directory="/content/base_vectorielle",
        embedding_function=embeddings
    )

base = charger_base()

def repondre(question):
    resultats = base.similarity_search_with_score(question, k=3)

    extraits = ""
    sources = []

    for doc, score in resultats:
        source = doc.metadata.get("source", "inconnue")
        page = doc.metadata.get("page", "?")

        extraits += f"\nSource : {source}, page {page}\n"
        extraits += doc.page_content + "\n"

        sources.append((source, page))

    prompt = f"""
Tu es un assistant documentaire d'Altéa Services.
Réponds uniquement à partir des extraits.
Si l'information est absente, dis que tu ne sais pas.
N'invente aucune information.

EXTRAITS :
{extraits}

QUESTION :
{question}

RÉPONSE :
"""

    r = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=180
    )
    r.raise_for_status()

    return r.json()["response"], sources

question = st.text_input(
    "Votre question",
    placeholder="Exemple : Combien de jours de télétravail sont autorisés ?"
)

if st.button("Rechercher", type="primary"):
    if question.strip():
        with st.spinner("Recherche et génération en cours..."):
            try:
                reponse, sources = repondre(question)

                st.subheader("Réponse")
                st.write(reponse)

                st.subheader("Sources utilisées")
                for source, page in dict.fromkeys(sources):
                    st.write(f"📄 {source} — page {page}")

            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.warning("Veuillez saisir une question.")
