import re
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------
# 1) Données
# -------------
documents = [
    "Paris est une belle ville.", 
    "Lyon est une autre belle ville.", 
    "Berlin est la capitale de l'Allemagne."
]

# -------------
# 2) TF-IDF
# -------------
vectorizer = TfidfVectorizer()  # token_pattern par défaut : r"(?u)\b\w\w+\b"
tfidf_matrix = vectorizer.fit_transform(documents)

# Liste de tous les tokens dans le vocabulaire
terms = vectorizer.get_feature_names_out()

# -------------
# 3) Tokenisation manuelle du premier document (pour les offsets)
# -------------
first_doc = documents[0]  # "Paris est une belle ville."
token_pattern = re.compile(r"(?u)\b\w\w+\b") 
tokens_in_first_doc = token_pattern.findall(first_doc.lower())
# tokens_in_first_doc = ['paris', 'est', 'une', 'belle', 'ville']

# -------------
# 4) Récupérer les offsets [start, end] de chaque token
#    en parcourant le texte original
# -------------
offsets = []
search_start = 0
for token in tokens_in_first_doc:
    # Recherche "case-insensitive" à partir de search_start
    subsequence = first_doc[search_start:].lower()
    match = re.search(re.escape(token), subsequence)
    if match:
        start_idx = search_start + match.start()
        end_idx   = search_start + match.end()
        offsets.append([start_idx, end_idx])
        # On se positionne après la fin du token trouvé
        search_start = end_idx
    else:
        # Si on ne trouve pas (cas très rare, ex. répétitions)
        offsets.append([-1, -1])

# -------------
# 5) Afficher scores TF-IDF + offsets
#    pour chaque token du premier document
# -------------
print("=== Résultats pour le 1er document ===")
for i, token in enumerate(tokens_in_first_doc):
    # Récupérer l'index du token dans le vocabulaire TF-IDF
    # (peut être absent, par ex. si token < 2 chars, stopwords, etc.)
    if token in terms:
        vocab_index = list(terms).index(token)
        tfidf_value = tfidf_matrix[0, vocab_index]
    else:
        tfidf_value = 0.0

    start, end = offsets[i]
    print(f"Token '{token}' => TF-IDF: {tfidf_value:.4f}, offsets: [{start}, {end}]")

# -------------
# 6) (Optionnel) Structure de sortie type "modèle"
#    Par ex. [[start, end], [start, end], ...]
# -------------
modele = offsets
print("\nModele :", modele)
