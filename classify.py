from enum import Enum
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re
from generate_synonyms import get_syns

rise_words = get_syns(["go_up", "rise", "increase", "jump", "ascend"])
fall_words = get_syns(["fall", "drop", "dip", "decrease", "go_down"])
open_words = get_syns(["open", "start", "begin"])
close_words = get_syns(["close", "end", "finish"])


class QuestionType(Enum):
    OR = 1          # Ex: Did IBM rise or fall?
    RISE = 2        # Ex: Did the Dow go up?
    FALL = 3        # Ex: Did Apple decrease?
    AMT_RISE = 4    # Ex: How much did Amazon go up?
    AMT_FALL = 5    # Ex: How much did American Airlines decrease?
    AMT_OPEN = 6    # Ex: What did Google open at?
    AMT_CLOSE = 7   # Ex: How much did Tesla close at?
    UNKNOWN = 8     # Question didn't match any of the above types

# Use this method to get the name of the entity a question is asking about
def getEntity(q):
    entity = "ENTITY NAME"
    return entity

# Takes a question in the form of a string as an input and returns a
# tuple where the first item is the QuestionType and the second item
# is the named entity in the question
def classifyQuestion(q: str) -> tuple:
    entity = getEntity(q)

    # Make all letters lowercase for easier matching
    q = q.lower()

    # If a question contains 'or', it is
    if re.match(".+( or ).+", q):
        return QuestionType.OR, entity
    
    if re.match("\A(did).+", q):
        if containsWords(rise_words, q):
            return QuestionType.RISE, entity
        if containsWords(fall_words, q):
            return QuestionType.FALL, entity

    if re.match("\A(how much|what|where).+", q):
        if containsWords(open_words, q):
            return QuestionType.AMT_OPEN, entity
        if containsWords(close_words, q):
            return QuestionType.AMT_CLOSE, entity
        if containsWords(rise_words, q):
            return QuestionType.AMT_RISE, entity
        if containsWords(fall_words, q):
            return QuestionType.AMT_FALL, entity

    return QuestionType.UNKNOWN, entity


# Checks if q contains any word in words. Returns true if so, false otherwise
def containsWords(words: list, q: str):
    for word in words:
        if re.match(".+\s%s(\s.+|[?.]|\Z)" % word, q):
            return True
    
    return False

def questionTypeTest():
    q_file = open('Resources/assignment1-test-questions.txt', 'r')

    for line in q_file:
        print(line)
        print(classifyQuestion(line))
        print('\n')

    q_file.close()

questionTypeTest()