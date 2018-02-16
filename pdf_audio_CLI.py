#! /usr/bin/python

# importing dependency packages
import os
import argparse
import PyPDF2
import pyttsx3


# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .pdf file. \
						Make sure to add .pdf in the end of file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."


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


def speak_text(text):
	"""
	function to invoke TTS engine to speak the pdf text
	"""
	engine = pyttsx3.init()
	engine.setProperty('rate', 150)
	engine.setProperty('voice', 'en+m7')
	engine.say(text)
	engine.runAndWait()


def main():

	parser = argparse.ArgumentParser(description = "  \"PDF Orateur\" - A PDF Audio Reader! \n \
										    \"Authors\" - Nikhil Kumar and Prashant Jain ")
	parser.add_argument("-s", "--speak", type = str, nargs = 1,
                        metavar = "file_name", default = None,
                        help = "Opens and reads the specified pdf file in human voice.")

	args = parser.parse_args()

	if args.speak is not None:
		text = extract_text(args)
		speak_text(text)


if __name__ == "__main__":
	main()
