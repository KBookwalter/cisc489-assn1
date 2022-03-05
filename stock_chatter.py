# stock-chatter.py

from sys import argv
import nltk
import classify
from parse import parse

def main():
    try:
        runFromFile(argv[1], argv[2])
    except:
        runFromConsole(argv[1])

def runFromFile(article, filename):
    file = open(filename, 'r')
    for line in file:
        result = parse(article, line.strip())
        if result:
            print('Answer: %s\n' % result[0])
            for sentence in result[1]:
                print('Source: Line %d: %s\n' % (sentence[1], sentence[0]))
        else:
            print('No information available.')
    file.close()

def runFromConsole(article):
    userInput = ""
    while True:
        userInput = input('What would you like to know?\n')
        if userInput.lower() == 'quit':
            break
        result = parse(article, userInput)

        print('\n\n')
        print(result)
        print('\n\n')

        if result:
            print('\n')
            print('Answer: %s\n' % result[0])
            for sentence in result[1]:
                print('Source: Line %d: %s\n' % (sentence[1], sentence[0]))
        else:
            print('No information available.\n')

    print('stonks')


if __name__ == "__main__":
    main()
