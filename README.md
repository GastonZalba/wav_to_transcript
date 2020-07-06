# wav_to_transcript

Prepare audio files while creating a transcript.txt to be used in [dc_tts](https://github.com/Kyubyong/dc_tts), breaking large files into small pieces and converting to the recommended format. This use Google's voice recognition to prepare a basis for transcription.

## Requirements
* NumPy
* PyDub
* Soundfile
* SpeechRecognition
* Librosa
* num2words (in processTranscript.py)

## Step 1: split audio files
* Adjust audio parameters(silences, db) and language in config.py
* Place all the wav files to be processed in the same folder
* Run `python processAudio.py [folderName]`
* The converted files and the transcript are created in the subfolder '_data'

### Specs of processed audio files:
* PCM wav
* mono
* 32 bits
* 22.050Mhz
* Up to 10 seconds

## Step 2: create the transcription
* Run `python createTranscript.py [folderName]` to automatically complete the cleaned trasncription in field *. This will remove unwanted characters, and convert numbers to words.

* You must check and correct the recognized text.

### The transcription.txt has the following structure:
[Path to file] | [Text automatically recognized] | * | [duration in seconds]<br>

## Step 3: complete the transcription
* Run `python processTranscript.py [folderName]` to automatically complete the cleaned trasncription in field *. This will remove unwanted characters, and convert numbers to words.



## Todo
- Allow more voice recognition services.
- Add function to clean numbers and punctuaction signs in the transcript.txt to fill rhe * column.