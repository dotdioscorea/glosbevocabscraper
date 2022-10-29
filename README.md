
# glosbevocabscraper v1.0


Glosbevocabscraper is a tool for quickly scraping translated definitions, audio files and example sentences for use with flashcard apps such as Anki.

The tool takes an input text file consisting of a list of words in a target language, one per line. It then scrapes glosbe.com for available translations, word attributes (eg noun, gender), example sentences in both the target and alternative language, and audio files, before exporting the scraped data in a csv.

This prepared data can then be easily imported into flashcard apps such as Anki, and used to generate cards that have word definitions and audio, for basic vocab decks, or example sentences, for sentence based decks.


## Features

- Supports over 6,000 languages thanks to glosbe language selection (https://glosbe.com/all-languages)

- Scrapes definitions, example sentences and audio files

- Exports to csv for easy data manipulation and importing into other apps such as Anki


## Installation
Not sure yet, havent figured out how that works. coming soon^tm


## Options
    -h, --help                      Print this help text and exit
    --version                       Print program version and exit
    -v                              Verbose mode
    -c                              Comprehensive mode will only save a 
                                    word's scraped data if all fields
                                    were successfully scraped. Using this
                                    option will improve the quality of
                                    the dataset, but will potentially
                                    decrease the number of words in the
                                    final dataset. Leave this out if you
                                    do not mind missing fields here and there.
    -s <#>                          Define a custom start point. The program
                                    will start processing the list from the 
                                    specified position. This can be used when
                                    a previous run was incomplete and you
                                    wish to pick up where you left off.
    -t                              Wordlist language. This is the language
                                    the provided wordlist is currently in.
                                    This should be considered the 'target'
                                    language, which audio will be based off
                                    and words translated from.
    -n                              Native language. This is the language
                                    you already know. Definitions will be in
                                    this language.
    -o <path>                       Output path. This is the directory where
                                    the output.csv and Audio folder will be
                                    generated.
    -i <path>                       Input path. This is the path to the wordlist
                                    text file you wish to process.
    -l <#>                          Delay. This is the delay in milliseconds
                                    between each request to glosbe.com. Setting
                                    this too low may result in you getting
                                    blocked for too many spam requests.
    --ns                            No sentences. Do not scrape example sentences.
    --na                            No audio. Do not scrape audio files.
    --nd                            No definitions. Do not scrape word definitions.


## Example usage
inputfile.txt
```    
Tisch
sehen
bewegt
Krankenhaus
```

Command
```
main.py -i /Users/aaronrucinski/Desktop/samplelist.txt -o /Users/aaronrucinski/Desktop/testrun -t de -n en -l 500
```

output.csv
```csv
Tisch,"table, desk, board, meal, bench, platen, stage",https://glosbe.com/fb_aud/mp3/zB150194_wikipedia-commons-e-e9-De-Tisch.ogg.cvrt.mp3,Kannst du mir mal gerade bei diesem <strong>Tisch</strong> helfen?,Can you give me a hand with this <strong>table</strong>?
sehen,"see, look, view, seeing, eyesight, look at",https://glosbe.com/fb_aud/mp3/B6810949_audio-by-111005.mp3,"Bitte grüß sie von mir, wenn du sie auf der Party <strong>siehst</strong>.",Please say hello to her if you <strong>see</strong> her at the party.
bewegt,"eventful, touched, animate",https://glosbe.com/fb_aud/mp3/CG323076_De-at-bewegt.ogg.cvrt.mp3,Zwei Ereignisse der vergangenen Monate haben mich tief <strong>bewegt</strong>.,Two <strong>events</strong> in the past few months have touched me deeply.
Krankenhaus,"hospital, infirmary, clinic",https://glosbe.com/fb_aud/mp3/D2280751_De-Krankenhaus.ogg.cvrt.mp3,"Sie bestand darauf, dass er ins <strong>Krankenhaus</strong> geht.",She insisted that he should go to the <strong>hospital</strong>.
```


## Planned features

- Produce input wordlist from source material such as book, ordered by frequency
- Produce GUI
- Produce sentence weight based on word frequency so that sentences can be ordered. This would mean each new sentence should in theory introduce only one or two new words (after the most common words).


## Disclaimer
This tool relies on glosbe.com for all data and audio files. Audio on glosbe may be user submitted, or taken from other websites. Do not distribute data without permission. This tool is based on the glosbe page html, and so may break at any time. Be aware that you may be blocked by spam detection. You can try and avoid this through use of vpns and the delay feature. MIT license applies.

