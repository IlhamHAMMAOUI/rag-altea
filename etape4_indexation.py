from pathlib import Path
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from etape1_collecte import collecter
from etape2_nettoyage import nettoyer_pages
from etape3_decoupage import preparer_chunks


def indexer(dossier_docs="/content/altea/docs", dossier_base="/content/base_vectorielle"):
    pages = nettoyer_pages(collecter(dossier_docs))
    chunks = preparer_chunks(pages, taille=500, chevauchement=50)
    if not chunks:
        raise ValueError("Aucun chunk : vérifiez le dossier de documents")

    emb = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path=dossier_base)
    collection = client.get_or_create_collection(name="altea_upsert_test")
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    textes = [doc.page_content for doc in chunks]
    vecteurs = emb.embed_documents(textes)
    metadonnees = [doc.metadata for doc in chunks]
    collection.upsert(
        ids=ids, documents=textes, embeddings=vecteurs, metadatas=metadonnees
    )
    print("Chunks produits :", len(chunks))
    print("Chunks indexés :", collection.count())
    return collection


if __name__ == "__main__":
    indexer()
