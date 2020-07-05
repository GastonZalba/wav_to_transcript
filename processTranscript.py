import os
import sys
import re
from num2words import num2words

import config

def prepareTranscript():

    global inputFolder
    global transcript

    if len(sys.argv) < 2:
        print('Folder argument missing')
        exit()

    inputFolder = str(sys.argv[1])            

    if not os.path.exists(inputFolder):
        print('Folder not found')
        exit()

    transcript = "{}/_data/{}".format(inputFolder, config.transcript_name)
    
    if not os.path.isfile(transcript):
        print('Transcript not found')
        exit()
    

def createProcessedTranscript():   
    global file
    file = open("{}/_data/_{}".format(inputFolder, config.transcript_name), 'w')
    print('Created transcript')


def process():
    
    global errors
    errors = []

    for line in open(transcript, 'r'):
        fields = line.split('|')

        fields[1] = cleanRawField(fields[1])
        fields[2] = cleanFilteredField(fields[1])

        line = '|'.join(fields)
        writeLine(line)


def cleanRawField(field):
    field = field.replace("…", "...")
    field = field.replace("—", "-")
    return field


def cleanFilteredField(field):
    # find numbers
    numbers = re.findall('\d+', field)
    if len(numbers) > 0:
        for number in numbers:
            try:
                textNumber = num2words(number, lang=config.language_Num2words)
                field = field.replace(number, textNumber)
            except:
                errors.append('ERROR converting {} to words'.format(number))
    
    # preserve only wanted characters
    field = re.sub("[^" + config.acceptedVocab + "]+","", field)

    return field


def writeLine(line):   
    file.write(line)
    print(line)


def printErrors():
    if not len(errors):
        print('No errors found')
    else:
        for error in errors:
            print(error)


prepareTranscript()
createProcessedTranscript()
process()
printErrors()
print('Done')