import re


import re

def nettoyer_texte(texte):
    # Remplacer les espaces multiples
    texte = re.sub(r"\s+", " ", texte)

    # Supprimer les espaces au début et à la fin
    return texte.strip()


def nettoyer_pages(pages):
    pages_nettoyees = []

    for page in pages:
        nouvelle_page = page.copy()

        nouvelle_page["texte"] = nettoyer_texte(
            page["texte"]
        )

        pages_nettoyees.append(nouvelle_page)

    return pages_nettoyees



if __name__ == "__main__":
    from etape1_collecte import collecter
    pages = collecter("/content/altea/docs")
    print("Pages nettoyées :", len(nettoyer_pages(pages)))
