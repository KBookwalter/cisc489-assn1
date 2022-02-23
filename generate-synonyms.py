from nltk.corpus import wordnet

def get_syns(words_init, file):
    all_syns = []
    for word in words_init:
        syns = wordnet.synsets(word)
        for syn in syns:
            normalized = syn.lemmas()[0].name().lower().replace("_", " ")
            if normalized not in all_syns:
                all_syns.append(normalized)

    return all_syns