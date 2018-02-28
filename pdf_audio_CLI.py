#! /usr/bin/python

# importing dependency packages
import os
import argparse
import PyPDF2
import pyttsx3


# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .pdf file. \
						Make sure to add .pdf in the end of file. "
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."
INVALID_VOICE_INPUT = "Error: %s is wrong input for voice. Enter 'm' or 'f' for voice."


def validate_file(file_name):
    '''
    validate file name(with .pdf) and path.
    '''
    if not valid_filetype(file_name):
			print(INVALID_FILETYPE_MSG % (file_name))
			quit()
    elif not valid_path(file_name):
			print(INVALID_PATH_MSG % (file_name))
			quit()
    return


def valid_filetype(file_name):
    # validate file type
    return file_name.endswith('.pdf')


def valid_path(path):
    # validate file path
    return os.path.exists(path)


def valid_voice(voice):
	#validate correct input for male or female voice
	voices = ['m', 'f']

	if voice not in voices:
		print(INVALID_VOICE_INPUT % (voice))
		quit()


def extract_text(args):
	"""
	function to extract text from pdf at given filename 
	and that filename can be used by args.speak[0]
	"""
	filename = args.speak[0]
	validate_file(filename)
	pdfFileObj = open(filename, "rb")
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

	mytext = ""

	for pageNum in range(pdfReader.numPages):
		pageObj = pdfReader.getPage(pageNum)
		mytext += pageObj.extractText()

	pdfFileObj.close()

	return mytext


def speak_text(text, rate, voice):
	"""
	function to invoke TTS engine to speak the pdf text
	"""
	engine = pyttsx3.init()
	all_voices = engine.getProperty('voices')		#getting available voices by system-engine
	maleVoice = all_voices[0].id
	femaleVoice = all_voices[1].id
	voice = maleVoice if voice == 'm' else femaleVoice
	engine.setProperty('rate', rate)
	engine.setProperty('voice', voice)
	engine.say(text)
	engine.runAndWait()


def main():

	parser = argparse.ArgumentParser(description="  \"PDF Orateur\" - A PDF Audio Reader! \n \
										    \"Authors\" - Nikhil Kumar and Prashant Jain ")
	parser.add_argument("speak", type=str, nargs=1,
                     metavar="file_name", default=None,
                     help="Opens and reads the specified pdf file in human voice.")
	parser.add_argument("-r", "--rate", type=int, nargs=1,
                     metavar="rate_of_speech", default=None,
                     help="Select the rate of speech, default is 150.")
	parser.add_argument("-v", "--voice", type=str, nargs=1,
                     metavar="voice", default=None,
                     help="Select male or female voice. Enter 'm' for male voice or 'f' for \
					 female voice preceded by -v. Default voice in male")

	args = parser.parse_args()			#parsing all arguments in args var

	if args.rate is not None:
		rate = args.rate[0]
	else:
		rate = 150						#default rate of speech

	if args.voice is not None:
		voice = args.voice[0]
		valid_voice(voice)
	else:
		voice = 'm'					#default voice of speech -male

	if args.speak is not None:
		text = extract_text(args)
		speak_text(text, rate, voice)	#passing all three arguments


if __name__ == "__main__":
	main()
