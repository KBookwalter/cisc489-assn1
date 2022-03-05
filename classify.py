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


class QuestionClassifier():
    def __init__(self):
        self.match_word = None


    # Finds the name of the entity referred to in a question
    # Works by finding the substring between 'did' and whatever rise/fall/open/close word is used
    # Ex. Finds X in 'How much did X rise/fall/open at/close at?'
    def getEntity(self, q: str):
        entity = 'ENTITY NAME'
        if self.match_word != None:
            start = q.index('did') + 4
            end = q.index(self.match_word) - 1
            entity = q[start:end]
        return entity



    # # Takes a question in the form of a string as an input and returns a
    # # tuple where the first item is the QuestionType and the second item
    # # is the named entity in the question

    def classifyQuestion(self, q: str) -> tuple:
        entity = 'ENTITY NAME'
        type = QuestionType.UNKNOWN

        # Make all letters lowercase for easier matching
        q = q.lower()

        # If a question contains 'or', it is
        if re.match(".+( or ).+", q):
            type = QuestionType.OR
            self.containsWords(self, rise_words + fall_words, q)
        elif re.match("\A(did).+", q):
            if self.containsWords(self, rise_words, q):
                type = QuestionType.RISE
            elif self.containsWords(self, fall_words, q):
                type = QuestionType.FALL
        elif re.match("\A(how much|what|where).+", q):
            if self.containsWords(self, open_words, q):
                type = QuestionType.AMT_OPEN
            elif self.containsWords(self, close_words, q):
                type = QuestionType.AMT_CLOSE
            elif self.containsWords(self, rise_words, q):
                type = QuestionType.AMT_RISE
            elif self.containsWords(self, fall_words, q):
                type = QuestionType.AMT_FALL

        entity = self.getEntity(self, q)

        return type, entity

    # Checks if q contains any word in words. Returns true if so, false otherwise
    def containsWords(self, words: list, q: str):
        for word in words:
            if re.match(".+\s%s(\s.+|[?.]|\Z)" % word, q):
                self.match_word = word
                return True

        self.match_word = None
        return False

    def questionTypeTest(self):
        q_file = open('Resources/assignment1-test-questions.txt', 'r')

        for line in q_file:
            print(line)
            print(self.classifyQuestion(self, line))
            print('\n')

        q_file.close()

    def entityTest(self):
        file = open('Resources/assignment1-test-questions.txt', 'r')

        for line in file:
            e = self.getEntity(self, line)
            # print(e + '\n')

        file.close()
        
# qc =  QuestionClassifier()
# qc.questionTypeTest()
# entityTest()
