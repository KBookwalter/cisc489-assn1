from classify import QuestionClassifier
from classify import QuestionType
from nltk.tokenize import word_tokenize
from generate_synonyms import get_syns
import re

# past_rise_words = get_syns(["went_up", "rose", "increased", "jumped", "ascended", "up"])
# past_fall_words = get_syns(["fell", "dropped", "dipped", "decreased", "down", "loss", "dive", "lower", "off"])
# past_open_words = get_syns(["opened", "started", "began"])
# past_close_words = get_syns(["closed", "ended", "finished"])

rise_words = get_syns(["go_up", "rise", "increase", "jump", "ascend", "went_up", "rose", "increased", "jumped", "ascended", "up"])
fall_words = get_syns(["fall", "drop", "dip", "decrease", "go_down", "fell", "dropped", "dipped", "decreased", "down", "loss", "dive", "lower", "off"])
open_words = get_syns(["open", "start", "begin", "opened", "started", "began"])
close_words = get_syns(["close", "end", "finish", "closed", "ended", "finished"])



qc = QuestionClassifier

# Wrapper function for parsing
# Returns output based on question type in list format
def parse(article: str, question: str) -> list:
    questionInfo = qc.classifyQuestion(qc, question)
    
    


    # Get all relevant sentences, if none exist, we know nothing about the entity from the articles
    sentences = getSentences(article, questionInfo[1])
    if not sentences:
        return None

    print('\n\nQUESTION INFO:\n')
    print(questionInfo[0])
    print(questionInfo[1])
    print('\n')
    for sentence in sentences:
        print(sentence[0])
        print('\n')
    print('\n\n')

    result = []

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
        result = parseQuant(sentences, rise_words, questionInfo[1])
        if result:
            return ['%s.' % result[0][1], [list(result[0][0])]]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_FALL):
        result = parseQuant(sentences, fall_words, questionInfo[1])
        if result:
            return ['%s.' % result[0][1], [list(result[0][0])]]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_OPEN):
        result = parseQuant(sentences, open_words, questionInfo[1])
        if result:
            return ['%s.' % result[0][1], [list(result[0][0])]]
        else:
            return None
    elif(questionInfo[0] == QuestionType.AMT_CLOSE):
        result = parseQuant(sentences, close_words, questionInfo[1])
        if result:
            return ['%s.' % result[0][1], [list(result[0][0])]]
        else:
            return None
    else:
        return None


# Parses relevant sentences for answers to or-type questions
# Returns any all sentences that contain answers as well as an indicator of whether the stock rose, fell, or both at differing times
def parseOr(sentences: str, entityName: str) -> list:
    matches = []
    answer = 0
    words = [rise_words, fall_words]

    for i in range(2):
        for sentence in sentences:
            for word in words[i]:
                regex = entityName + r'.{1,50}\s' + str(word).lower() + r'\s|' + str(word).lower() + r'.{1,15}' + entityName
                # print(word)
                if re.search(regex, sentence[0].lower()):
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
            regex = entityName + r'.{1,50}\s' + str(word).lower() + r'\s|' + str(word).lower() + r'.{1,15}' + entityName
            if re.search(regex, sentence[0].lower()):
                print('\n\n')
                print(word)
                matches.append(sentence)
                foundSentence = 1
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
            # regex = entityName.lower() + r'\s(?:\D{1,50})?\s' + str(word).lower() + r'\s(?:\D{1,15})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]|' + entityName.lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(?:\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower()
            regex = entityName.lower() + r'(?:\s.{1,50})?\s' + str(word).lower() + r'\s(?:\D{1,15})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)[\s.,-]|' + entityName.lower() + r'\s(?:\D{1,125})?(\d+(?:\.\d+)?%?(?:\s\d/\d)?)(?:\D{1,15})?(?:\d+(?:\.\d+)?%)?(?:\D{1,15})?\s'+ str(word).lower()
            match = re.search(regex, sentence[0].lower())
            if match:
                if match.group(1):
                    matches.append([sentence, match.group(1)])
                else:
                    matches.append([sentence, match.group(2)])
                foundSentence = 1
                break
    
    if foundSentence:
        # for m in matches:
        #     print(m)
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
    