import csv
import getopt
import json
import os.path
import requests
import sys
from os import getcwd
from time import sleep

from bs4 import BeautifulSoup

langs = None
target_lang = None
native_lang = None
verbose = False
inpath = None
outpath = None
delay: int = None
sentencesenabled = True
definitionsenabled = True
audioenabled = True
comprehensivemode = False
startpoint = 0
wordlist = []

_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                  'Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}


def getwordlist():
    global inpath
    if inpath is None:
        inpath = input("Enter path to word list: ")

    try:
        with open(inpath, "r") as file:
            for line in file.readlines():
                wordlist.append(line.replace('\n', ''))
            print("Successfully loaded {} words from the file.".format(len(wordlist)))
    except IOError as e:
        print(e)
        quit()

    if len(wordlist) < startpoint:
        print("-s value is greater than length of wordlist.")
        quit()


def getdelay():
    global delay

    if delay is None:
        try:
            delay = int(input("Provide a delay (ms) between word web requests (setting this too low may result in you "
                              "getting ip blocked): "))
        except TypeError:
            while delay is None:
                try:
                    delay = int(input("Please enter a whole integer number: "))
                except SyntaxError:
                    continue


def getlangcode():
    global target_lang
    global native_lang

    if target_lang is None:
        target_lang = input("Enter two letter language code for wordlist language: ")
        while target_lang not in langs:
            if native_lang == target_lang and target_lang is not None:
                native_lang = input("Wordlist language and native language cannot be the same: ")
            target_lang = input("Language not supported. Supported codes available at: "
                                "https://glosbe.com/all-languages-full.\nTry again: ")

    if native_lang is None:
        native_lang = input("Enter two letter language code for native language: ")
        while native_lang not in langs or native_lang == target_lang:
            if native_lang == target_lang:
                native_lang = input("Wordlist language and native language cannot be the same: ")
            else:
                native_lang = input("Language not supported. Supported codes available at: "
                                    "https://glosbe.com/all-languages-full.\nTry again: ")


def getoutputpath():
    global outpath

    if outpath is None:
        outpath = input("Enter output folder directory: ")

    # if os.path.exists(_path):
    #    print(getcwd() + "/" + _path + " already exists.")

    if not os.path.exists(outpath):
        try:
            os.mkdir(outpath)
            print(getcwd() + "/" + outpath + " created successfully.")
        except PermissionError as e:
            print(e)
            quit()

    # if os.path.exists(_path + "/audio"):
    #    print(getcwd() + "/" + _path + "/audio" + " already exists.")

    if not os.path.exists(outpath + "/audio"):
        try:
            os.mkdir(outpath + "/audio")
            print(getcwd() + "/" + outpath + "/audio created successfully.")
        except PermissionError as e:
            print(e)
            quit()
    elif os.listdir(outpath + "/audio"):
        response = None
        while response not in ("y", "n"):
            response = input(getcwd() + "/" + outpath + "/audio contains files. Empty folder? (y/n) ")
        if response == 'y':
            for file in os.scandir(outpath + '/audio'):
                try:
                    os.remove(file.path)
                except PermissionError as e:
                    print(e)
                    quit()
            print(getcwd() + "/" + outpath + "/audio successfully emptied.")

    if os.path.exists(outpath + "/output.csv"):
        response = None
        while response not in ("y", "n"):
            response = input(getcwd() + "/" + outpath + "/output.csv already exists. Overwrite? (y/n) ")
        if response == 'y':
            os.remove(outpath + "/output.csv")
            print(getcwd() + "/" + outpath + "/output.csv successfully deleted.")

    try:
        print(getcwd() + "/" + outpath + "output.csv created successfully.")
    except Exception as e:
        print(e)
        quit()


def getsentences():
    global outpath
    global target_lang
    global native_lang
    global wordlist
    global startpoint

    count = startpoint
    savedwords = 0
    skipppedwords = 0

    for word in wordlist[startpoint:]:
        count += 1

        try:
            print('Processing word ' + str(count) + "/" + str(len(wordlist)) + ': "' + word + '"')
            r = requests.get("https://glosbe.com/" + target_lang + "/" + native_lang + "/" + word, headers=_headers)
            soup = BeautifulSoup(r.content, "html.parser")

            attributes = ""
            try:
                mb2 = soup.find("div", attrs={"class": "mb-2"}).findAll(attrs={"class": "phrase__summary__field"})
                for item in mb2:
                    attributes += item.decode_contents() + ","
                attributes = attributes[:len(attributes) - 1]
                if verbose:
                    print('Attributes obtained: "' + attributes + '"')
            except KeyError:
                if verbose:
                    print('No attributes obtained.')
                if comprehensivemode:
                    print('Skipping word (comprehensive mode).')
                    skipppedwords += 1
                    continue

            global audioenabled
            if audioenabled:
                audiourl = ""
                try:
                    r = requests.get("https://glosbe.com/api/audios/" + target_lang + "/" + word, headers=_headers)
                    audioname = list(json.loads(r.content)['phraseAudioCarrier']['audioEntries'][0]['url'].values())[0]
                    audioformat = list(json.loads(r.content)['phraseAudioCarrier']['audioEntries'][0]['url'].keys())[0]
                    audiowebsite = "https://glosbe.com/fb_aud/" + audioformat
                    audiofile = open(outpath + "/audio/" + audioname, "wb")
                    audiourl = audiowebsite + "/" + audioname
                    if verbose:
                        print('Downloading audio file from "' + audiourl + '"')
                    audio = requests.get(audiourl, headers=_headers)
                    audiofile.write(audio.content)
                    if verbose:
                        print('Audio file saved as  "' + outpath + "/audio/" + audioname + '"')
                except ConnectionError:
                    if verbose:
                        print('No audio obtained.')
                    if comprehensivemode:
                        print('Skipping word (comprehensive mode).')
                        skipppedwords += 1
                        continue

            global definitionsenabled
            if definitionsenabled:
                translation = ""
                try:
                    for item in soup.findAll("span", attrs={"data-element": "phrase"}):
                        translation += item.decode_contents().replace('\n', '') + ", "

                    translation = translation[:len(translation) - 2]

                    if len(translation) > 0:
                        if verbose:
                            print('Translations obtained: "' + translation + '"')
                    else:
                        if verbose:
                            print("No translations obtained")
                except KeyError:
                    if verbose:
                        print("No translations obtained")
                    if comprehensivemode:
                        print('Skipping word (comprehensive mode).')
                        skipppedwords += 1
                        continue

            global sentencesenabled
            if sentencesenabled:
                sentences = ["", ""]
                try:
                    if target_lang == 'en':
                        sentence = soup.find("p", attrs={"lang": native_lang}).findPrevious('p')
                    else:
                        sentence = soup.find("p", attrs={"lang": target_lang})

                    sentences = sentence.decode_contents(), sentence.findNext('p').decode_contents()
                    if verbose:
                        print('Obtained sentence target language: "' + sentences[0] + '"')
                        print('Obtained sentence native language: "' + sentences[1] + '"')
                except KeyError as e:
                    print(e)
                    if verbose:
                        print('No sentences obtained.')
                    if comprehensivemode:
                        print('Skipping word (comprehensive mode).')
                        skipppedwords += 1
                        continue

            with open(outpath + "/output.csv", 'a') as file:
                writer = csv.writer(file)

                datatowrite = [word]

                if definitionsenabled:
                    datatowrite.append(translation)
                if audioenabled:
                    datatowrite.append(audiourl)
                if sentencesenabled:
                    datatowrite.append(sentences[0])
                    datatowrite.append(sentences[1])

                writer.writerow(datatowrite)
                savedwords += 1

            global delay
            sleep(delay / 1000)
        except ConnectionError:
            print("Error connecting to server. \nSkipping word.")

    print("Job completed. " + str(savedwords) + " words saved, " + str(skipppedwords) + " words skipped.")


def checkflags():
    opts, args = getopt.getopt(sys.argv[1:], "i:o:hvdcs:t:n:l:", ["ns","na","nd"])
    for opt in opts:
        if opt[0] == '-h':
            print("Correct usage: main.py -i <input_file> -o <output_file> -h (help) -v (verbose mode) -d (dev mode) "
                  "-c (only save complete words) -s <start number> -t <wordlist language code> -n <native language "
                  "code> -l <word delay in ms> --na (no audio) --nt (no translations) --ns (no sentences)")
            quit()
        if opt[0] == '-v':
            global verbose
            verbose = True
        if opt[0] == '-c':
            global comprehensivemode
            comprehensivemode = True
        if opt[0] == '-s':
            global startpoint
            try:
                startpoint = int(opt[1]) - 1
            except TypeError:
                print("Error parsing -s arguement")
        global target_lang
        if opt[0] == '-t':
            target_lang = opt[1]
            if target_lang not in langs:
                print("Language code " + target_lang + "is not valid. Supported codes available at: "
                                                       "https://glosbe.com/all-languages-full")
                quit()
        global native_lang
        if opt[0] == '-n':
            native_lang = opt[1]
            if native_lang not in langs:
                print("Language code " + native_lang + "is not valid. Supported codes available at: "
                                                       "https://glosbe.com/all-languages-full")
                quit()
        if target_lang == native_lang and native_lang is not None:
            print("Wordlist language cannot be the same as native language.")
            quit()
        if opt[0] == '-o':
            global outpath
            outpath = opt[1]
        if opt[0] == '-i':
            global inpath
            inpath = opt[1]
        if opt[0] == '-l':
            global delay
            try:
                delay = int(opt[1])
            except TypeError:
                print("Error parsing -l arguement")
            if delay == 0:
                input("A delay of 0ms may get you ip-blocked for spam. It is recommended you increase this.")
        if opt[0] == '--ns':
            global sentencesenabled
            sentencesenabled = False
        if opt[0] == '--nd':
            global definitionsenabled
            definitionsenabled = False
        if opt[0] == '--na':
            global audioenabled
            audioenabled = False

def importlangcodes():
    global langs
    langs = str.split(open("codes.array", "r").read(), ",")


def main() -> None:
    importlangcodes()
    checkflags()
    getdelay()
    getwordlist()
    getlangcode()
    getoutputpath()
    getsentences()


if __name__ == "__main__":
    main()
