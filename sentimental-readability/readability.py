#!/usr/bin/env python3

import cs50


def count_letters(text):
    text_upper = text.upper()
    count = 0
    for ii in range(0, len(text)):
        if (text_upper[ii] >= 'A' and text_upper[ii] <= 'Z'):
            count = count + 1
    return count


def count_words(text):
    count = 0
    word_found = False
    for ii in range(0, len(text)):
        if (not word_found and text[ii] != ' '):
            word_found = True
            count = count + 1
            continue
        elif (word_found and text[ii] == ' '):
            word_found = False
    return count


def count_sentences(text):
    count = 0
    for ii in range(0, len(text)):
        c = text[ii]
        if (c == '.' or c == '!' or c == '?'):
            count = count + 1
    if count == 0 and len(text) > 0:
        count = 1
    return count


"""
index = 0.0588 * L - 0.296 * S - 15.8
L is the avg number of letters per 100 words in the text,
S is the avg number of sentences per 100 words in the text.
"""


def grade(text):
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = letters / (words / 100)
    S = sentences / (words / 100)
    index = round(0.0588 * L - 0.296 * S - 15.8)
    if index > 16:
        return "Grade 16+"
    elif index < 1:
        return "Before Grade 1"
    else:
        return "Grade " + str(index)


text = cs50.get_string("Text: ")
print("%s" % grade(text))
