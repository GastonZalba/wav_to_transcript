import os
import sys
import re
from num2words import num2words

import config

def prepareTranscript():

    if len(sys.argv) < 2:
        print('Folder argument missing')
        exit()

    inputFolder = str(sys.argv[1])            

    if not os.path.exists(inputFolder):
        print('Folder not found')
        exit()

    transcript = "./{}/_data/{}".format(inputFolder, config.transcript_name)
    
    if not os.path.isfile(transcript):
        print('Trasncript not found')
        exit()

    global errors
    errors = []
    
    for line in open(transcript, 'r'):
        fields = line.split('|')

        transcriptRaw = cleanRawField(fields[1])
        transcriptFiltered = cleanFilteredField(fields[1])

        print(transcriptRaw)
        print(transcriptFiltered)
    

def cleanRawField(field):
    field = field.replace("…", "...")
    field = field.replace("—", "-")
    return field


def cleanFilteredField(field):
    field = re.sub("()«»\"\'","", field)

    # find numbers
    numbers = re.findall('\d+', field)
    if len(numbers) > 0:
        for number in numbers:
            try:
                textNumber = num2words(number, lang=config.language_Num2words)
                field = field.replace(number, textNumber)
            except:
                errors.append('ERROR converting {} to words'.format(number))

    return field


def createProcessedTranscript():   
    file = open(outputFolder + '/_tmp_' + config.transcript_name, 'w')
    file.close()
    print('Created transcript')


def printErrors():
    for error in errors:
        print(error)


prepareTranscript()
printErrors()