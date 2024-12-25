import stanza

stanza.download('fr')
nlp = stanza.Pipeline('fr', processors='tokenize,ner')

def extract_locations(key, txt):

    doc = nlp(txt)
    locentities = []

    for ent in doc.ents:
        if ent.type == "LOC":
            yield LocEntity(
                document= key,
                start= ent.start_char,
                end= ent.end_char,
                motor="stanza",
                text= ent.text
            )
    return locentities

def main():
    locations = extract_locations(key, txt)
    print(locations)
    
    main()
