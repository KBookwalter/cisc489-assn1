from classify import QuestionClassifier
from nltk.tokenize import word_tokenize
from generate_synonyms import get_syns
import re

past_rise_words = get_syns(["went_up", "rose", "increased", "jumped", "ascended", "up"])
past_fall_words = get_syns(["fell", "dropped", "dipped", "decreased", "down", "loss", "dive", "lower", "off"])
past_open_words = get_syns(["opened", "started", "began"])
past_close_words = get_syns(["closed", "ended", "finished"])

qc = QuestionClassifier

# Wrapper function for parsing
# Returns output based on question type in list format
def parse(article: str, question: str) -> list:
    questionInfo = qc.classifyQuestion(question)

    # Get all relevant sentences, if none exist, we know nothing about the entity from the articles
    sentences = getSentences(article, question)
    if not sentences:
        return None


    result = []

    if(questionInfo[0] == 1):
        result = parseOr(sentences, questionInfo[1])
        if result:
            return [str('It %s.', result[1]), result[0]]
        else:
            return None
    elif(questionInfo[0] == 2):
        result = parsePolar(sentences, past_rise_words, questionInfo[1])
        if result:
            return ['It rose.', result]
        else:
            return None
    elif(questionInfo[0] == 3):
        result = parsePolar(sentences, past_fall_words, questionInfo[1])
        if result:
            return ['It fell.', result]
        else:
            return None
    elif(questionInfo[0] == 4):
        result = parseQuant(sentences, past_rise_words, questionInfo[1])
        if result:
            return ['%d.', result]
        else:
            return None
    elif(questionInfo[0] == 5):
        result = parseQuant(sentences, past_fall_words, questionInfo[1])
        if result:
            return ['%d.', result]
        else:
            return None
    elif(questionInfo[0] == 6):
        result = parseQuant(sentences, past_open_words, questionInfo[1])
        if result:
            return ['%d', result]
        else:
            return None
    elif(questionInfo[0] == 7):
        result = parseQuant(sentences, past_close_words, questionInfo[1])
        if result:
            return ['%d', result]
        else:
            return None
    else:
        return None


# Parses relevant sentences for answers to or-type questions
# Returns any all sentences that contain answers as well as an indicator of whether the stock rose, fell, or both at differing times
def parseOr(sentences: str, entityName: str) -> list:
    matches = []
    answer = 0
    words = [past_rise_words, past_fall_words]

    for i in range(2):
        for sentence in sentences:
            for word in words[i]:
                regex = entityName + r'.*\s' + str(word).lower() + r'\s.*'
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
def parsePolar(sentences: str, words: list, entityName: str) -> list:
    matches = []
    foundSentence = 0
    for sentence in sentences:
        for word in words:
            regex = entityName + r'.*\s' + str(word).lower() + r'\s.*'
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
def parseQuant(sentences: str, words: list, entityName: str) -> list:
    matches = []
    foundSentence = 0
    for sentence in sentences:
        for word in words:
            regex = entityName.lower() + r'\s(?:\D{1,50})?\s' + str(word).lower() + r'\s(?:\D{1,15})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]|' + entityName.lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower()
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
def getSentences(article: str, question: str) -> list:
    sentences = []

    terms = word_tokenize(question)
    file = open(article, 'r')
    count = 0
    for line in file:
        lineText = line.strip()
        count += 1
        for term in terms:
            regex = r'.*\s' + term.lower() + r'\s.*'
            if re.search(regex, lineText.lower()):
                sentences.append((lineText, count))
                break
    file.close()

    return sentences
    