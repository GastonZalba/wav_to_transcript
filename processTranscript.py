import re
from num2words import num2words

import config
import helpers as hp


def processLines():
    
    global errors
    errors = []

    for line in open(transcript, 'r'):
        fields = line.split('|')

        fields[1] = cleanRawField(fields[1])
        fields[2] = cleanFilteredField(fields[1])

        line = '|'.join(fields)
        hp.writeLine(line, newTranscript)


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
            except Exception:
                errors.append('ERROR converting {} to words'.format(number))
    
    # preserve only wanted characters
    field = re.sub("[^" + config.acceptedVocab + "]+","", field)

    return field


print('>> Start')

inputFolder = hp.getFolder(hp.getArgument(1))   

transcript = hp.checkInputFile( "{}/_data/{}".format( inputFolder, config.transcript_name) )
newTranscript = hp.createFile( inputFolder + '/_data/', "_new_" + config.transcript_name)

processLines()
hp.printErrors(errors)
print('>> Done')