def rechercher(question, base_propre, k=3):
    return base_propre.similarity_search_with_score(
        question, k=k
    )
