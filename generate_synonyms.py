from nltk.corpus import wordnet

# Takes a list of words and returns a list of unique synonyms of all words in the list
def get_syns(words_init):
    all_syns = []
    for word in words_init:
        syns = wordnet.synsets(word)
        for syn in syns:
            normalized = syn.lemmas()[0].name().lower().replace("_", " ")
            if normalized not in all_syns:
                all_syns.append(normalized)

    return all_syns