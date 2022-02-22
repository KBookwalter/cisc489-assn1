# stock-chatter.py

from sys import argv
import nltk

def main():
    try:
        runFromFile(argv[1], argv[2], argv[3])
    except:
        runFromConsole(argv[1], argv[2])

def runFromFile(article1, article2, filename):
    file = open(filename, 'r')
    for line in file:
        print(line.strip())
        # replace with parser
    file.close()

def runFromConsole(article1, article2):
    userInput = ""
    while userInput != 'quit':
        userInput = input('What would you like to know?\n')
        print(userInput, article1, article2)
        # replace with parser


if __name__ == "__main__":
    main()

