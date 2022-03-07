Kevin Bookwalter - kbookwal@udel.edu
Aaron Gluck - gluck@udel.edu

Assignment 1

FILE DESCRIPTIONS:

stock-chatter.py:
    This is the main file of the program.
classify.py:
    This file classifies questions and entities.
generate_synonyms.py:
    This file is used to generate synonyms for rise/fall words and the like.
parse.py
    This file does the parsing of the articles.


NLP TOOLS USED:

NLTK


EXPLANATION OF PROGRAM:

This program takes questions either from the user or a file, classifies the question type, and determines the suject of the question.
It then gets all sentences mentioning that entity and parses those sentences for a pattern consistent with a potential answer.

NOTE:
Please install the required packages found in Resources/requirements.txt
You may also have to download some data associated with NLTK, please follow related command line instructions.
