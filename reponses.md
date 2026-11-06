## Q2 — Métadonnées

On conserve le nom du fichier, la page et le service
pour identifier l'origine des informations.

Deux usages concrets :
1. Afficher la source et la page d'une réponse.
2. Filtrer les documents selon le service RH, IT ou Général.

## Q4 — Nettoyage des documents

Avant nettoyage, le texte peut contenir des retours
à la ligne et des espaces inutiles.

Après nettoyage, le texte devient plus lisible.

Défaut restant possible : un en-tête répété sur
plusieurs pages.

Solution : détecter et supprimer les en-têtes
répétés lors du nettoyage.

## Q5 — Explication du découpage

Test :
decouper("abcdefghij", taille=4, chevauchement=1)

Résultat :
['abcd', 'defg', 'ghij']

Chaque chunk contient 4 caractères.
Le chevauchement est de 1 caractère.

Le premier chunk est 'abcd'.
Le deuxième commence par 'd' : 'defg'.
Le troisième commence par 'g' : 'ghij'.

## Q6 — Comparaison des tailles de chunks

| Taille | Chevauchement | Nombre de chunks | Longueur moyenne |
|---|---|---|---|
| 200 | 20 | 150 | 198,87 |
| 500 | 50 | 60 | 496,68 |
| 1000 | 100 | 30 | 991,70 |

Conclusion :
Plus la taille des chunks augmente, plus leur nombre diminue.
Je retiens 500 caractères avec un chevauchement de 50.

## Q7 — Choix de la taille des chunks

1. Un chunk trop petit risque de perdre le contexte
et de produire des réponses incomplètes.

2. Un chunk trop grand peut contenir plusieurs sujets
et rendre la recherche moins précise.

3. Le chevauchement permet de conserver le contexte
entre deux chunks.

4. Je retiens une taille de 500 caractères avec
un chevauchement de 50 caractères.
Cette configuration a produit 60 chunks.

## Q8 — Dimension des embeddings

Le modèle all-MiniLM-L6-v2 génère des vecteurs
de 384 dimensions.

Nombre de chunks : 69
Nombre total de valeurs à stocker :
69 × 384 = 26496.


## Q9 — Matrice de similarité

Les phrases 1 et 2 parlent toutes les deux
des demandes de congés, même si elles utilisent
des mots différents.

Le modèle d'embeddings représente le sens des
phrases sous forme de vecteurs, ce qui permet
de détecter des ressemblances sémantiques.

Dans notre matrice :
- Phrases 1 et 2 : 0,432
- Phrases 1 et 3 : 0,558
- Phrases 2 et 3 : 0,412

Le score le plus élevé est celui des phrases
1 et 3, même si elles traitent de sujets différents.

Cela montre que la similarité vectorielle
n'est pas toujours parfaitement alignée
avec le sens attendu.


## Q11 — Recherche dans la base vectorielle

Trois questions de salariés ont été testées
avec k = 3.

1. Congés :
   Source principale : conges_absences.pdf

2. Mot de passe :
   Sources : livret_accueil.pdf et mot_de_passe.txt

3. Horaires de travail :
   Source principale : horaires.txt

Les résultats sont globalement pertinents,
mais certains chunks sont moins liés à la question.

## Q12 — Réindexation et upsert

Avec add_documents sans identifiants stables,
le nombre de chunks est passé de 68 à 136.
Il a donc doublé.

Avec upsert et les mêmes identifiants,
le nombre reste à 68 après deux indexations.

Upsert permet d'ajouter un nouveau chunk
ou de mettre à jour un chunk existant.

Si un document de l'entreprise est modifié,
il faut le relire, le nettoyer, le redécouper,
recalculer ses embeddings et mettre à jour
la base vectorielle.

Il faut aussi supprimer les anciens chunks
qui ne correspondent plus au document.

## Q13 — Base vectorielle et GitHub

Le dossier base_vectorielle/ n'est pas envoyé
sur GitHub car il contient des données générées
automatiquement, potentiellement volumineuses
et confidentielles.

Pour recréer la base, un collègue doit :
1. Cloner le dépôt GitHub.
2. Installer les dépendances Python.
3. Récupérer les documents autorisés.
4. Exécuter le script d'indexation.

Ce script relit les documents, les nettoie,
les découpe, calcule les embeddings et
recrée la base vectorielle.

Le dossier base_vectorielle/ doit être ajouté
au fichier .gitignore.

## Exercice 2 — Étape 5 — Q2

Question testée : Comment demander des congés ?

Avec k = 1, on récupère un seul chunk pertinent,
mais on risque de manquer des informations.

Avec k = 3, on récupère trois chunks du document
conges_absences.pdf. Cela donne davantage de contexte.

Avec k = 10, on récupère plus de passages,
mais certains concernent le télétravail ou
la sécurité des e-mails et sont moins pertinents.

Quand k augmente, on gagne en couverture
des informations, mais on risque d'ajouter
du bruit et d'augmenter le coût de traitement.

Pour cette question, je retiens k = 3.

## Exercice 2 — Étape 5 — Q3

Question : Comment demander des congés ?

Avec service="RH", les trois résultats viennent
du document conges_absences.pdf.
Les distances sont 0,7268, 0,7984 et 0,8835.

Avec service="IT", les résultats viennent de
securite_emails.txt, demande_materiel.txt
et mot_de_passe.txt.
Les distances sont plus élevées.

Le filtre permet de limiter la recherche
aux documents d'un service.

C'est une première étape vers la confidentialité,
car il réduit les documents accessibles
pendant la recherche.

Cependant, il ne suffit pas : il faut aussi
authentifier les utilisateurs et vérifier
leurs droits d'accès côté serveur.

## Exercice 2 — Étape 6 — Q4

Le prompt contient trois parties :

1. Consigne :
L'assistant doit répondre uniquement à partir
des documents fournis et citer ses sources.

2. Extraits :
Trois chunks provenant de conges_absences.pdf,
avec les numéros de page.

3. Question :
Comment demander des congés ?

Le prompt se termine par RÉPONSE,
où le modèle devra générer sa réponse.

## Exercice 2 — Étape 6 — Q5

Cinq questions ont été testées avec le RAG,
dont deux sans réponse dans la documentation.

1. Congés :
Réponse globalement pertinente.
Source citée : conges_absences.pdf, pages 1-2.
Quelques informations supplémentaires sont inutiles.

2. Mot de passe :
Le modèle propose une procédure pertinente.
La source n'est pas citée explicitement.

3. Horaires de travail :
Le modèle fournit des horaires.
L'exactitude reste à vérifier dans horaires.txt.
La source n'est pas citée.

4. Météo de demain :
Le modèle indique qu'il ne peut pas répondre
avec les extraits disponibles.
La phrase de repli est correctement utilisée.

5. Coupe du monde 2030 :
Le modèle indique que les documents ne
contiennent pas l'information nécessaire.
La phrase de repli est correctement utilisée.

Conclusion :
Le RAG répond globalement aux questions
documentées et évite d'inventer une réponse
pour les deux questions hors documentation.

Il faut améliorer la citation systématique
des sources et la précision des réponses.

## Exercice 2 - Q6

Le LLM seul indique qu'il ne connait pas les regles
de teletravail d'Altea. Il n'invente pas de reponse.

Le RAG retrouve teletravail.pdf, pages 1 et 2,
et utilise ces extraits pour formuler sa reponse.

Une hallucination est une information fausse ou
inventee par le modele.

Le RAG limite ce risque en fournissant des documents
pertinents au LLM, mais il ne garantit pas une
reponse toujours exacte ou complete.

## Exercice 2 - Etape 6 - Q7

On fixe temperature=0 pour obtenir des reponses
plus stables, previsibles et moins aleatoires.

Un assistant documentaire doit repondre avec
precision a partir des documents de l'entreprise,
sans chercher a etre creatif.

Ce parametre limite les variations, mais ne
garantit pas l'absence d'hallucinations.

## Exercice 2 - Etape 7 - Q9

Nous avons evalue la recherche vectorielle sur
10 questions avec k=3.

Resultats :
- Questions testees : 10
- Questions reussies : 10
- Taux de reussite : 100 %

Pour chaque question, le document attendu
apparait parmi les trois premiers resultats.

La recherche est donc efficace sur ce jeu de test,
mais cela ne garantit pas que les reponses generees
par le modele soient toujours correctes.

## Exercice 2 - Etape 7 - Q10

Evaluation manuelle des 10 reponses du RAG :

Q1 - Conges : juste, source non citee
Q2 - Jours de conges : partielle, source non citee
Q3 - Mot de passe : partielle, source non citee
Q4 - Expiration : juste, source non citee
Q5 - Horaires : partielle, source non citee
Q6 - Teletravail : partielle, source non citee
Q7 - Materiel : partielle, source non citee
Q8 - E-mail suspect : partielle, source non citee
Q9 - Notes de frais : fausse, source non citee
Q10 - VPN : juste, source non citee

Bilan :
- Reponses justes : 3/10 = 30 %
- Reponses partielles : 6/10 = 60 %
- Reponses fausses : 1/10 = 10 %
- Reponses correctement sourcees : 0/10 = 0 %

Le taux de reussite de la recherche est de 100 %,
mais la generation des reponses doit etre amelioree.

Le modele doit mieux respecter les documents
et citer explicitement les sources utilisees.

## Exercice 2 - Etape 7 - Q11

Question choisie :
Comment demander un remboursement de frais ?

Le document attendu, notes_de_frais.pdf page 2,
a bien ete retrouve a l'etape de recherche.

L'erreur vient donc de la generation et non
de la recherche.

La reponse initiale etait fausse :
le modele demandait de contacter le service RH
au lieu d'utiliser l'application Frais+.

Ameliorations testees :
1. Prompt plus strict avec k=3 : reponse fausse.
2. Prompt plus strict avec k=1 : reponse fausse.
3. Extraction stricte avec k=1 : reponse fausse,
   mais citation de la source correcte.

Le dernier test invente encore des etapes
et ne mentionne pas l'application Frais+.

Resultat :
Les modifications testees n'ont pas permis
d'obtenir une reponse correcte.

Conclusion :
Le modele qwen2.5:1.5b ne respecte pas toujours
les informations du contexte documentaire.
Une amelioration possible serait de tester
un modele plus performant ou une extraction
plus controlee des informations.
