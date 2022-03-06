# stock-chatter.py

from sys import argv
import nltk
import classify
from parse import parse

def main():
    try:
        runFromFile(argv[1], argv[2])
    except IndexError:
        runFromConsole(argv[1])

# TODO: handle flag
def runFromFile(article, filename):
    file = open(filename, 'r')
    for line in file:
        q = line.strip()
        result = parse(article, q)
        print(q)
        if result:
            if result[0] == 'QUANT_FLAG':
                # print('QUANT_FLAG')
                for r in result[1]:
                    print('Answer: %s' % r[1])
                    print('Source: Line %s: %s\n' % (r[0][1], r[0][0]))

            else:
                print('\n')
                print('Answer: %s\n' % result[0])
                for sentence in result[1]:
                    print('Source: Line %d: %s\n' % (sentence[1], sentence[0]))
        else:
            print('No information available.\n')
    file.close()

def runFromConsole(article):
    userInput = ""
    while True:
        userInput = input('What would you like to know?\n')
        if userInput.lower() == 'quit':
            break
        result = parse(article, userInput)

        # print('\n\n')
        # print(result)
        # print('\n\n')

        if result:
            if result[0] == 'QUANT_FLAG':
                for r in result[1]:
                    print('Answer: %s' % r[1])
                    print('Source: Line %s: %s\n' % (r[0][1], r[0][0]))

            else:
                print('\n')
                print('Answer: %s\n' % result[0])
                for sentence in result[1]:
                    print('Source: Line %d: %s\n' % (sentence[1], sentence[0]))
        else:
            print('No information available.\n')

    print('stonks')


if __name__ == "__main__":
    main()
