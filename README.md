# wav_to_transcript

Prepare audio files while creating a transcript.txt to be used in [dc_tts](https://github.com/Kyubyong/dc_tts), breaking large files into small pieces and converting to the recommended format. This use Google's voice recognition to prepare a basis for transcription.

## Requirements
* NumPy
* PyDub
* Soundfile
* SpeechRecognition
* Librosa

## Usage
* Adjust audio parameters and language in config.py
* Place all the wav files to be processed in the same folder
* Run `python process.py [folderName]`
* The converted files and the transcript are created in the subfolder '_data'

### Specs of processed audio files:
* PCM wav
* mono
* 32 bits
* 22.050Mhz
* Up to 10 seconds

### Transcription
The transcription.txt has the following structure:<br>
[folderName]/[filename]_0001.wav | [Automatically recognized text] | * | [duration in seconds]<br>
You must check and correct the recognized text and fill the * column accordingly.

## Todo
- Allow more voice recognition services.
- Add function to clean numbers and punctuaction signs in the transcript.txt to fill rhe * column.