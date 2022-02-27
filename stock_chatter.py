# stock-chatter.py

from sys import argv
import nltk
import classify
from parse import parse

def main():
    try:
        runFromFile(argv[1], argv[2], argv[3])
    except:
        runFromConsole(argv[1], argv[2])

def runFromFile(article1, article2, filename):
    file = open(filename, 'r')
    for line in file:
        result = parse(article1, article2, line.strip())
        if result:
            print(result[0])
            for sentence in result[1]:
                print('\nArticle:%d Line %d: %s', sentence[2], sentence[1], sentence[0])
        else:
            print('No information available.')
    file.close()

def runFromConsole(article1, article2):
    userInput = ""
    while userInput != 'quit':
        userInput = input('What would you like to know?\n')
        result = parse(article1, article2, userInput)
        if result:
            print(result[0])
            for sentence in result[1]:
                print('\nArticle:%d Line %d: %s', sentence[2], sentence[1], sentence[0])
        else:
            print('No information available.')


if __name__ == "__main__":
    main()
