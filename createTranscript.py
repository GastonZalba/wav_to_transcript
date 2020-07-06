import librosa
import glob
import os
import sys
import speech_recognition as sr
r = sr.Recognizer()

import config
import helpers as hp

def processAudioFiles():
    global errors
    errors = []

    for dirpath, subdirs, files in os.walk(outputFolder):
        for dir in subdirs:
            
            outputSubfolder = outputFolder + dir
            infiles = glob.glob( "{}/{}/*.wav".format(outputFolder, dir))
            
            for infile in infiles:
                duration = round(librosa.get_duration(filename=infile), 2)   
                path = os.path.split(infile)
                filename = dir + '/' + path[len(path) -1]       
                line = prepareTranscriptLine(infile, filename, duration)
                hp.writeLine(line, transcript)


def prepareTranscriptLine(fileOutput, filename, duration):

    if config.speech_to_text:
        text = speechToText(fileOutput)
    else:
        text = '*'

    line = filename + '|' # file
    line += text + '|' # transcript
    line += str(duration) # length in seconds
    line += "\n"
    
    return line


def speechToText(outfile):

    with sr.AudioFile(outfile) as source:
        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text, language=config.language)
            #print(text)

        except Exception: 
            text = '*' # valor por defecto si no se pudo decodificar el texto
            errors.append('Speech not recognized', outfile)

        finally:
            return text


print('>> Start')

inputFolder = hp.getFolder(hp.getArgument(1))
outputFolder = "{}/_data".format(inputFolder)

transcript = hp.createFile(outputFolder, config.transcript_name)
processAudioFiles()
hp.printErrors(errors)
print('>> Done')