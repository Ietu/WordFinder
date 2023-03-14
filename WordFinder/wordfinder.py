import requests
import time
import nltk
from rich.progress import Progress, track
from bs4 import BeautifulSoup
from tqdm import tqdm 
from nltk.corpus import words

red = '\033[31m'
blue = '\033[34m'
cyan = '\033[36m'
lightred = '\033[91m'
lightblue = '\033[94m'
RESA = '\033[0m' #RESET_ALL

#nltk.download('words')
#filter words of length 3 and above, just set number lower if you want 1 and 2 letter words

with open('words.txt', 'r') as file:
    english_words = [line.strip() for line in file]

#english_words = set(word.lower() for word in words.words() if len(word) >= 3)

letters = input(f"{cyan}> {RESA}Enter letters: ")
word_length_range = input(f"{cyan}> {RESA}Enter range of word lengths (e.g. '5' or '4-6', leave blank for all): ")

if word_length_range:
    if "-" in word_length_range:
        #filter words within the specified range
        word_length_range = [int(num) for num in word_length_range.split("-")]
        min_length = word_length_range[0]
        max_length = word_length_range[1]
        words_to_check = [word for word in english_words if min_length <= len(word) <= max_length]
    else:
        #filter words with the specified length
        word_length = int(word_length_range)
        words_to_check = [word for word in english_words if len(word) == word_length]
else:
    #sort words by length
    words_to_check = sorted(english_words, key=len)

#create a frequency count of the input letters
input_freq = {}
for letter in letters:
    input_freq[letter] = input_freq.get(letter, 0) + 1

#filter words that can be made from the input letters
matching_words = []
start_time = time.time()  #starting timer
for word in words_to_check:
    #create a frequency count of the word
    word_freq = {}
    for letter in word:
        word_freq[letter] = word_freq.get(letter, 0) + 1
    #check if the frequency count of the word is a subset of the frequency count of the input letters
    if all(word_freq.get(letter, 0) <= input_freq.get(letter, 0) for letter in word):
        matching_words.append(word)

show_defs = False

definitions_input = input(f"{cyan}> {RESA}Would you like to see definitions? (y/n): ")
if definitions_input.lower() == "y":
    show_defs = True

if show_defs == True:
    def_dict = {}
    for word in track(matching_words):
        page = requests.get(f'https://www.dictionary.com/browse/{word}')
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            def_dict[word] = soup.find('meta', attrs={'name': 'description'})['content']
        except:
            continue
    for length in range(3, max(len(word) for word in matching_words) + 1):
        words_of_length = sorted([word for word in matching_words if len(word) == length])
        if words_of_length:
            print(f"\n[{lightred}{length}{RESA}]{lightred}Letter Words:{RESA}")
            for word in words_of_length:
                definition = def_dict.get(word)
                if definition is not None:
                    print(f"{cyan}> {RESA}[ {lightblue}{word.capitalize()} {RESA}]: {definition}")
else:
    for length in range(3, max(len(word) for word in matching_words) + 1):
        words_of_length = sorted([word for word in matching_words if len(word) == length])
        if words_of_length:
            print(f"\n[{lightred}{length}{RESA}]{lightred}Letter Words:{RESA}")
            for word in words_of_length:
                print(f"{cyan}> {RESA}[ {lightblue}{word.capitalize()} {RESA}]")
end_time = time.time()

print(f"\n{cyan}> {RESA}Found {lightred}{len(matching_words)}{RESA} words in {lightred}{end_time - start_time:.2f}{RESA} seconds! {cyan}<{RESA}")