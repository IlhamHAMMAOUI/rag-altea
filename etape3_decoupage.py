from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def preparer_chunks(pages_nettoyees, taille=500, chevauchement=50):
    documents = [
        Document(
            page_content=page["texte"],
            metadata={
                "source": page["source"],
                "service": page["service"],
                "page": page["page"],
            },
        )
        for page in pages_nettoyees
    ]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=taille, chunk_overlap=chevauchement
    )
    return splitter.split_documents(documents)


if __name__ == "__main__":
    from etape1_collecte import collecter
    from etape2_nettoyage import nettoyer_pages
    pages = nettoyer_pages(collecter("/content/altea/docs"))
    print("Nombre de chunks :", len(preparer_chunks(pages)))
