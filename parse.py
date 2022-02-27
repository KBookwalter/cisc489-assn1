from classify import QuestionClassifier
from nltk.tokenize import word_tokenize
from generate_synonyms import get_syns
import re

past_rise_words = get_syns(["went_up", "rose", "increased", "jumped", "ascended"])
past_fall_words = get_syns(["fell", "dropped", "dipped", "decreased", "went_down"])
past_open_words = get_syns(["opened", "started", "began"])
past_close_words = get_syns(["closed", "ended", "finished"])

qc = QuestionClassifier

# Wrapper function for parsing
# Returns output based on question type in list format
def parse(article1: str, article2: str, question: str) -> list:
    questionInfo = qc.classifyQuestion(question)

    # Get all relevant sentences, if none exist, we know nothing about the entity from the articles
    sentences = getSentences(article1, article2, question)
    if not sentences:
        return None


    result = []

    if(questionInfo[0] == 1):
        result = parseOr(sentences)
        if result:
            return [str('%s %s.', questionInfo[1], result[1]), result[0]]
        else:
            return None
    elif(questionInfo[0] == 2):
        result = parsePolar(sentences, past_rise_words)
        if result:
            return [str('%s rose.', questionInfo[1]), result]
        else:
            return None
    elif(questionInfo[0] == 3):
        result = parsePolar(sentences, past_fall_words)
        if result:
            return [str('%s fell.', questionInfo[1]), result]
        else:
            return None
    elif(questionInfo[0] == 4):
        result = parseQuant(sentences, past_rise_words)
        if result:
            return [str('%s rose %d.', questionInfo[1]), result]
        else:
            return None
    elif(questionInfo[0] == 5):
        result = parseQuant(sentences, past_fall_words)
        if result:
            return [str('%s fell %d.', questionInfo[1]), result]
        else:
            return None
    elif(questionInfo[0] == 6):
        result = parseQuant(sentences, past_open_words)
        if result:
            return [str('%s opened at %d.', questionInfo[1]), result]
        else:
            return None
    elif(questionInfo[0] == 7):
        result = parseQuant(sentences, past_close_words)
        if result:
            return [str('%s closed at %d.', questionInfo[1]), result]
        else:
            return None
    else:
        return None


# Parses relevant sentences for answers to or-type questions
# Returns any all sentences that contain answers as well as an indicator of whether the stock rose, fell, or both at differing times
def parseOr(sentences: str) -> list:
    matches = []
    answer = 0
    words = [past_rise_words, past_fall_words]

    for i in range(2):
        for sentence in sentences:
            for word in words[i]:
                regex = r'.*' + word.lower() + r'.*'
                if re.match(regex, sentence.lower()):
                    matches.append(sentence)
                    if i == 0:
                        answer = 1
                    elif i == 1 and answer == 0:
                        answer = 2
                    elif i == 1 and answer == 1:
                        answer = 3
                    break

    if answer == 0:
        return None
    if answer == 1:
        return [matches, 'rose']
    elif answer == 2:
        return [matches, 'fell']
    elif answer == 3:
        return [matches, 'both rose and fell']


# Parses relevant sentences for answers to polar interrogative questions
# Returns any/all sentences that countain answers
def parsePolar(sentences: str, words: list) -> list:
    matches = []
    foundSentence = 0
    for sentence in sentences:
        for word in words:
            regex = r'.*' + word.lower() + r'.*'
            if re.match(regex, sentence.lower()):
                matches.append(sentence)
                foundSentence == 1
                break
    
    if foundSentence:
        return matches
    else:
        return None


# Parses relevant sentences for answers to quantitative questions
# Returns any/all sentences that contain answers as well as the quantity we are looking for
def parseQuant(sentences: str, words: list) -> list:
    matches = []
    foundSentence = 0
    for sentence in sentences:
        for word in words:
            regex = word + r' [A-Za-z]? (\d+(\.\d+)?) ' # ex. '... rose( by) amount' or 'closed( at) amount'
            match = re.search(regex, sentence.lower())
            if match:
                matches.append([sentence, match.group()])
                foundSentence == 1
                break
    
    if foundSentence:
        return matches
    else:
        return None



# Finds and returns all sentences that contain a mention of the entity found in the question
def getSentences(article1: str, article2: str, question: str):
    sentences = []

    for i in range(2):
        if i == 0:
            article = article1
        elif i == 1:
            article = article2

        terms = word_tokenize(question)
        file = open(article, 'r')
        count = 0
        for line in file:
            lineText = line.strip()
            count += 1
            for term in terms:
                regex = r'.*' + term.lower() + r'.*'
                if re.search(regex, lineText.lower()):
                    sentences.append((lineText, count, i + 1))
                    break
        file.close()

    return sentences