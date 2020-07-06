# merge files up to this seconds
max_duration = 7

# split_on_silence
min_silence_len = 200 #ms
silence_thresh = -16
keep_silence = 200 #ms

# prepare txt using Google to convert speech to Text
speech_to_text = True
language = 'es-AR'

# https://pypi.org/project/num2words/
language_Num2words = 'es'

acceptedVocab = u'''␀␃ !',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz¡¿ÁÅÉÍÓÚáæèéëíîñóöúü—'''

# output files mhz
outrate = 22050

transcript_name = 'transcript.txt'