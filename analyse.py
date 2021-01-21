import os
import csv
from pathlib import Path

allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZäöüÄÖÜß.:,;'\"!?"

def save_frequencies(frequencies, path):
    frequencies = [(i[0], i[1][0], i[1][1]) for i in frequencies.items()]
    frequencies.sort(key=lambda tup: tup[1], reverse=True)
    with open(path, "w", encoding="utf-8", newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['item', 'total', 'frequency'])
        csv_out.writerows(frequencies)
    
def convert_count_to_percentage(items):
    total_items = 0
    for item in items:
        total_items += items[item]

    for item in items:
        items[item] = (items[item], (items[item] / total_items * 100))

def analyse_text(path, convert_to_lower=True):
    print("Analysing text in", path)

    with open("{}/content.txt".format(path), "r", encoding="utf-8") as f:
        # get list of words
        words = []
        for line in f.readlines():
            for word in line.split(" "):
                words.append(word)

        # item: frequency
        letters = {}            
        bigrams = {}
        trigrams = {}
        count = 0

        # count letters and bigrams
        for word in words:
            for letter in word:
                if convert_to_lower:
                    letter = letter.lower()
                if letter not in allowed_characters:
                    continue

                count += 1

                if letter in letters:
                    letters[letter] += 1
                else:
                    letters[letter] = 1

            for bigram in zip(word[:-1], word[1:]):
                if (bigram[0] not in allowed_characters) or (bigram[1] not in allowed_characters):
                    continue
                bigram = bigram[0] + bigram[1]
                if convert_to_lower:
                    bigram = bigram.lower()
                if bigram in bigrams:
                    bigrams[bigram] += 1
                else: 
                    bigrams[bigram] = 1

            for trigram in zip(word[:-2], word[1:-1], word[2:]):
                if (trigram[0] not in allowed_characters) or (trigram[1] not in allowed_characters) or (trigram[2] not in allowed_characters):
                    continue
                trigram = trigram[0] + trigram[1] + trigram[2]
                if convert_to_lower:
                    trigram = trigram.lower()
                if trigram in trigrams:
                    trigrams[trigram] += 1
                else: 
                    trigrams[trigram] = 1

        return letters, bigrams, trigrams, count
        

def main():
    all_frequencies = {}
    for dirpath, dirnames, filenames in os.walk("data", ):
        dirpath = dirpath.replace("\\", "/")
        all_frequencies[dirpath] = ({}, {}, {}, [0])
        # print(dirpath)
        if "content.txt" in filenames:
            letters, bigrams, trigrams, count = analyse_text(dirpath)
            all_frequencies[dirpath] = (letters, bigrams, trigrams, [count])
            
            parent = dirpath
            while True:
                index = parent.rfind('/')
                if index == -1:
                    break
                parent = parent[:index]
                for letter in letters:
                    if letter in all_frequencies[parent][0]:
                        all_frequencies[parent][0][letter] += letters[letter]
                    else:
                        all_frequencies[parent][0][letter] = letters[letter]

                for bigram in bigrams:
                    if bigram in all_frequencies[parent][1]:
                        all_frequencies[parent][1][bigram] += bigrams[bigram]
                    else:
                        all_frequencies[parent][1][bigram] = bigrams[bigram]

                for trigram in trigrams:
                    if trigram in all_frequencies[parent][2]:
                        all_frequencies[parent][2][trigram] += trigrams[trigram]
                    else:
                        all_frequencies[parent][2][trigram] = trigrams[trigram]

                all_frequencies[parent][3][0] += count

    # convert count into percentage
    for path in all_frequencies:
        letters = all_frequencies[path][0]
        bigrams = all_frequencies[path][1]
        trigrams = all_frequencies[path][2]
        count = all_frequencies[path][3][0]
        convert_count_to_percentage(letters)
        convert_count_to_percentage(bigrams)
        convert_count_to_percentage(trigrams)
        save_frequencies(letters, "{}/letters.csv".format(path))
        save_frequencies(bigrams, "{}/bigrams.csv".format(path))
        save_frequencies(trigrams, "{}/trigrams.csv".format(path))

        with open("{}/count.txt".format(path), "w") as f:
            f.write(str(count))
    # print(frequencies)

if __name__ == "__main__":
    main()