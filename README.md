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


SETUP:

DEPENDENCY INSTALLATION INSTRUCTIONS:

Install regex and nltk libraries
    $pip install regex
    $pip install nltk

NLTK Downloads

    1) Start python interpreter in the command line
        $python
    2) Import nltk
        >>> import nltk
    3) Download corpora
        >>> nltk.dowload('wordnet')

If there is any more data you need to install, it will tell you in the console

NOTE:

Dependencies are listed in requirements.txt
