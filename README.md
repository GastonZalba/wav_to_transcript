# wav_to_transcript

Prepare audio files while creating a transcript.txt to be used in [dc_tts](https://github.com/Kyubyong/dc_tts), breaking large files into small pieces and converting to the recommended format. This use Google's voice recognition to prepare a basis and facilitate subsequent manual transcription.

## Requirements
* NumPy
* PyDub
* Soundfile
* Librosa
* SpeechRecognition (`createTranscript.py`)
* num2words (`processTranscript.py`)

## Step 1: Audio files splitting 
* Adjust audio parameters (silence, max_duration, language, etc) in `config.py`
* Place all the wav files to be processed in the same folder
* Run `python processAudio.py [folderName]` to convert and trim the audio files
* This will create multiple audio files with the following characteristics:
    * PCM wav
    * mono
    * 32 bits
    * 22.050 Mhz
    * Duration up to 10 seconds (default)

## Step 2: Transcript creation
* Run `python createTranscript.py [folderName]` to create the transcript from the generated audio files
* Check and correct the text transcripts

### Transcript.txt structure:

| FolderName/FileName                  | Automatically recognized text   | Seconds length
| --------------------- | -------------------------------  | ------------------ 
| sampleFolder/sampleFile_0001.wav   | This is an automatic transcript and may contains numbers (1, 2) and some punctuation marks ('"-) | 6.10
| sampleFolder/sampleFile_0002.wav   | This line may has errors, but it's a good start | 5.51
| anotherFolder/anotherFile_0001.wav   | I may have censored words like f*** | 2.07  
| anotherFolder/anotherFile_0002.wav   | This column is allowed to have some abbreviations like vs. or tel. | 3.12  


## Step 3: Finishing the transcript
* After the transcription is corrected, run `python processTranscript.py [folderName]` to automatically add a third column with a cleaned version of the transcription. This also will remove some unwanted characters and convert numbers to words
* If they exist, remove all abbreviations from this column
* Check and correct


## Todo
- Allow other voice recognition services