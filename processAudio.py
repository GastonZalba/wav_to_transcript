import librosa
import glob
import os
import sys

import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf
import unicodedata
import config

import speech_recognition as sr
r = sr.Recognizer()

def prepareFolders():
    
    print('Start')

    global inputFolder
    global tmpFolder
    global outputFolder

    if len(sys.argv) < 2:
        print('Folder argument missing')
        exit()

    inputFolder = str(sys.argv[1])            

    if not os.path.exists(inputFolder):
        print('Folder not found')
        exit()

    tmpFolder = "./{}/_tmp".format(inputFolder) # for audio Chunks
    outputFolder = "./{}/_data/".format(inputFolder)
    
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)  # create output folder

    if not os.path.exists(tmpFolder):
        os.makedirs(tmpFolder)  # create tmp folder
    
    print('Folders created:', outputFolder , tmpFolder)


def splitFilesBySilence():

    print('Files splitting started')

    exclude = set(['_tmp', '_data'])
    for dirpath, subdirs, files in os.walk(inputFolder, topdown=True):
        subdirs[:] = [d for d in subdirs if d not in exclude]
        for file in files:
            fileName = clean_filename(file)
            split(os.path.join(dirpath, file), fileName)

def mergePieces():

    print('File merging started')

    createTranscript()

    for dirpath, subdirs, files in os.walk(tmpFolder):

        for dir in subdirs:

            outputSubfolder = outputFolder + dir
            infiles = glob.glob(tmpFolder + '/' + dir +
                                "/*.wav")  # wav files only
            data = [[]]
            durations = [[]]
            mixDuration = 0
            outputNum = 0

            for infile in infiles:

                duration = librosa.get_duration(filename=infile)
                mixDuration += duration

                y, sr = librosa.load(infile, sr=config.outrate,
                                     mono=True)  # Downsample

                if mixDuration <= config.max_duration:
                    data[outputNum] = np.append(data[outputNum], y)
                    durations[outputNum] = mixDuration
                else:
                    outputNum += 1
                    mixDuration = duration
                    data.append(np.append([], y))
                    durations.append(mixDuration)

            if not os.path.exists(outputSubfolder):
                os.makedirs(
                    outputSubfolder)  # create output subfolder

            for i, d in enumerate(data):
                duration = round(durations[i], 2)
                fileOutput = dir + "_{:04d}.wav".format(i)

                outfile = outputSubfolder + '/' + fileOutput

                sf.write(outfile, d, config.outrate, 'PCM_32')

                print('Created file', fileOutput)

                writeTranscript(dir, fileOutput, duration, outfile)

            print('Total files:', len(data))
            


def createTranscript():   
    file = open(outputFolder + '/' + config.transcript_name, 'w')
    file.close()
    print('Created transcript')


def speechToText(outfile):

    with sr.AudioFile(outfile) as source:
        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text, language=config.language)
            print(text)

        except:
            text = '*' # valor por defecto si no se pudo decodificar el texto
            print('Speech not recognized')

        finally:
            return text


def writeTranscript(dir, fileOutput, duration, outfile):

    if config.speech_to_text:
        text = speechToText(outfile)
    else:
        text = '*'

    line = dir.replace(" ", "_") + '/' + fileOutput + '|'  # file
    line += text + '|' # transcript 1
    line += '*|' # transcript 2
    line += str(duration) # length in seconds
    line += "\n"
    file = open(outputFolder + '/' + config.transcript_name, 'a')
    file.write(line)
    file.close()


def split(filepath, fileName):

    print('Splitting', fileName)

    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(
        sound,

        # split on silences longer than
        min_silence_len=config.min_silence_len,

        # anything under this is considered silence
        silence_thresh=dBFS + config.silence_thresh,

        # keep ms of leading/trailing silence
        keep_silence=config.keep_silence
    )

    tmpSubfolder = tmpFolder + "/" + fileName
    if not os.path.exists(tmpSubfolder):
        os.makedirs(tmpSubfolder)  # create output subfolder

    print('Created folder', fileName)
    print('Splitted', fileName, 'in', len(chunks), 'chunks')

    for i, chunk in enumerate(chunks):
        chunk.export(tmpFolder + '/' + fileName + '/' +
                     fileName + "_{:04d}.wav".format(i), format="wav")


# Remove accents, whitespaces and Uppercases
def clean_filename(s):
    s = os.path.splitext(s)[0]
    return strip_accents(s).replace(" ", "_").lower()


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

def deleteTmp():
    for root, dirs, files in os.walk(tmpFolder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    
    os.rmdir(tmpFolder)
    print('Temporary files removed')

prepareFolders()
splitFilesBySilence()
mergePieces()
deleteTmp()
print('Done')