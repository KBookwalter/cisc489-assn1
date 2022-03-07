from classify import QuestionClassifier
from classify import QuestionType
from generate_synonyms import get_syns
import re

# Generate verb synonym lists based on common words of each question category
rise_words = get_syns(["go_up", "rise", "increase", "jump", "ascend", "went_up", "rose", "increased", "jumped", "ascended", "up"])
fall_words = get_syns(["fall", "drop", "dip", "decrease", "go_down", "fell", "dropped", "dipped", "decreased", "down", "loss", "dive", "lower", "off"])
open_words = get_syns(["open", "start", "begin", "opened", "started", "began"])
close_words = get_syns(["close", "end", "finish","closed_down", "closed", "ended", "finished"])

qc = QuestionClassifier

# Wrapper function for parsing
# Returns output based on question type in list format
def parse(article: str, question: str) -> list:
    questionInfo = qc.classifyQuestion(qc, question)
    
    # Get all relevant sentences (sentences where entity is mentioned), if none exist, we know nothing about the entity from the articles
    sentences = getSentences(article, questionInfo[1])
    if not sentences:
        return None

    result = []

    # Handle different question types
    if(questionInfo[0] == QuestionType.OR):
        result = parseOr(sentences, questionInfo[1])
        if result:
            return [('It %s.' % result[1]), result[0]]
        else:
            return None
    elif(questionInfo[0] == QuestionType.RISE):
        result = parsePolar(sentences, rise_words, questionInfo[1])
        if result:
            return ['It rose.', result]
        else:
            return None
    elif(questionInfo[0] == QuestionType.FALL):
        result = parsePolar(sentences, fall_words, questionInfo[1])
        if result:
            return ['It fell.', result]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_RISE):
        result = parseQuant(sentences, rise_words, questionInfo[1], questionInfo[0])
        if result:
            return ['QUANT_FLAG', result]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_FALL):
        result = parseQuant(sentences, fall_words, questionInfo[1], questionInfo[0])
        if result:
            return ['QUANT_FLAG', result]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_OPEN):
        result = parseQuant(sentences, open_words, questionInfo[1], questionInfo[0])
        if result:
            return ['QUANT_FLAG', result]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_CLOSE):
        result = parseQuant(sentences, close_words, questionInfo[1], questionInfo[0])
        if result:
            return ['QUANT_FLAG', result]
        else:
            return None
    else:
        return None


# Parses relevant sentences for answers to or-type questions
# Returns any/all sentences that contain answers as well as an indicator of whether the stock rose, fell, or both at differing times
def parseOr(sentences: str, entityNames: list) -> list:
    matches = []
    answer = 0
    words = [rise_words, fall_words]

    for i in range(2):
        for sentence in sentences:
            thisSentence = 0
            for word in words[i]:
                for entityName in entityNames:
                    regex = str(entityName).lower() + r'.{1,50}\s' + str(word).lower() + r'\s|' + str(word).lower() + r'.{1,15}' + str(entityName).lower()
                    if re.search(regex, sentence[0].lower()):
                        matches.append(sentence)
                        thisSentence = 1
                        if i == 0:
                            answer = 1
                        elif i == 1 and answer == 0:
                            answer = 2
                        elif i == 1 and answer == 1:
                            answer = 3
                        break
                if thisSentence:
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
def parsePolar(sentences: str, words: list, entityNames: list) -> list:
    matches = []
    foundSentence = 0
    for sentence in sentences:
        thisSentence = 0
        for word in words:
            for entityName in entityNames:
                regex = str(entityName).lower() + r'.{1,50}\s' + str(word).lower() + r'\s|' + str(word).lower() + r'.{1,15}' + str(entityName).lower()
                if re.search(regex, sentence[0].lower()):
                    matches.append(sentence)
                    foundSentence = 1
                    thisSentence = 1
                    break
            if thisSentence:
                break
    
    if foundSentence:
        return matches
    else:
        return None


# Parses relevant sentences for answers to quantitative questions
# Returns any/all sentences that contain answers as well as the quantity we are looking for
def parseQuant(sentences: str, words: list, entityNames: list, type: QuestionType) -> list:
    matches = []
    foundSentence = 0
    for sentence in sentences:
        thisSentence = 0
        for word in words:
            for entityName in entityNames:
                regex=''
                if type == QuestionType.AMT_CLOSE:
                    # regex = entityName.lower() + r'\s(?:\D{1,50})?\s' + str(word).lower() + r'\s(?:\D{1,15})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]|' + entityName.lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(?:\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower()
                    # regex = entityName.lower() + r'(?:\s.{1,50})?\s' + str(word).lower() + r'(?:.+at)?\s(?:\D{1,10})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]|' + entityName.lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(?:\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower()
                    regex =  str(entityName).lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(?:\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower() + r'|'+str(entityName).lower() + r'(?:\s.{1,50})?\s' + str(word).lower() + r'(?:.{1,20}(?:at|to))?\s(?:\D{1,10})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]'
                else:
                    regex =  str(entityName).lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(?:\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower() + r'|'+str(entityName).lower() + r'(?:\s.{1,50})?\s' + str(word).lower() + r'\s(?:\D{1,10})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]'
                match = re.search(regex, sentence[0].lower())
                if match:
                    if match.group(1):
                        matches.append([sentence, match.group(1)])
                    else:
                        matches.append([sentence, match.group(2)])
                    foundSentence = 1
                    thisSentence = 1
                    break
            if thisSentence:
                break
    
    if foundSentence:
        return matches
    else:
        return None



# Finds and returns all sentences that contain a mention of the entity found in the question
def getSentences(article: str, entityNames: list) -> list:
    sentences = []

    file = open(article, 'r')
    count = 0
    for line in file:
        lineText = line.strip()
        count += 1
        for term in entityNames:
            regex = r'.*\s' + term.lower() + r'\s.*'
            if re.search(regex, lineText.lower()):
                sentences.append((lineText, count))
                break
    file.close()
    return sentences
    