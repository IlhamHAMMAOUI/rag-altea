from pathlib import Path
from pypdf import PdfReader


from pathlib import Path
from pypdf import PdfReader

# Lire un fichier PDF
def lire_pdf(chemin):
    lecteur = PdfReader(chemin)
    pages = []

    for numero, page in enumerate(lecteur.pages, start=1):
        texte = page.extract_text() or ""

        pages.append({
            "source": chemin.name,
            "page": numero,
            "texte": texte
        })

    return pages


# Lire un fichier TXT
def lire_txt(chemin):
    texte = chemin.read_text(encoding="utf-8")

    return [{
        "source": chemin.name,
        "page": 1,
        "texte": texte
    }]


# Collecter les documents
def collecter(dossier="/content/altea/docs"):
    pages = []

    for chemin in sorted(Path(dossier).rglob("*")):

        if not chemin.is_file():
            continue

        service = chemin.parent.name

        if chemin.suffix.lower() == ".pdf":
            nouvelles_pages = lire_pdf(chemin)

        elif chemin.suffix.lower() == ".txt":
            nouvelles_pages = lire_txt(chemin)

        else:
            continue

        for page in nouvelles_pages:
            page["service"] = service

        pages.extend(nouvelles_pages)

        print(
            f"{service} / {chemin.name} : "
            f"{len(nouvelles_pages)} page(s)"
        )

    return pages



if __name__ == "__main__":
    pages = collecter("/content/altea/docs")
    print("Nombre total de pages :", len(pages))
