import spacy
from spacy import displacy
import json

#python -m spacy download fr_dep_news_trf
#python -m spacy download fr_core_news_lg

Modele_version = "trf"
if Modele_version == "lg_Efficiency":
    Modele = "fr_core_news_lg"
elif Modele_version == "trf_Precision":
    Modele = "fr_dep_news_trf"

def extract_locations(txt, model_lang, key):
    nlp = spacy.load(model_lang)
    doc = nlp(txt)

    locentities = []

    for ent in doc.ents:
        if ent.type == "LOC":
            yield LocEntity(
                document= key,
                start= ent.start_char,
                end= ent.end_char,
                motor=f"{model_lang}",
                text= ent.text
            )
    return locentities

def main():
    locations = extract_locations(key, txt)
    print(locations)
    
    main()
