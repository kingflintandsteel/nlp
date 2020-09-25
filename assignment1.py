import string

import nltk
import os
import re
import math
from nltk.corpus import stopwords

unigrams = []
bigrams = []
trigrams = []
quadgrams = []

unigram_dic = {}
bigram_dic = {}
trigram_dic = {}
quadgram_dic = {}


def cleanup(line):
    line.lower()
    text = nltk.word_tokenize(line)
    text2 = text.copy()
    stemmer = nltk.PorterStemmer()
    punction = [",", "\"", "\'", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "\\",
                "/", "{", "}", "[", "]", "<", ">", "`", "~", "\n", "\t"]
    for word in text:
        if word in stopwords.words("english"):
            text2.remove(word)
            continue
        if word in punction:
            text2.remove(word)
    for x in range(0, len(text2)):
        text2[x] = stemmer.stem(text2[x])
    return text2


def count_dic(dictionary, gram):
    for item in gram:
        if item in dictionary.keys():
            dictionary[item] = dictionary[item] + 1
        else:
            dictionary[item] = 1
    return


def get_text(lines):
    new_lines = []
    in_text = False
    for line in lines:
        if line == '<TEXT>\n':
            in_text = True
            continue
        if line == '</TEXT>\n':
            break
        if in_text:
            new_lines.append(line)
            continue
    return new_lines


def probability_word(gram, n):
    global unigram_dic, bigram_dic, trigram_dic, quadgram_dic
    """
    :param gram:
    gram for probability
    :param n:
    looks n-1 into the past
    :return:
    returns the probability of the word
    """
    count_of_history = 0
    counting_dic = {}
    if n == 1:
        counting_dic = unigram_dic
    elif n == 2:
        counting_dic = bigram_dic
    elif n == 3:
        counting_dic = trigram_dic
    else:
        counting_dic = quadgram_dic
    count_of_gram = counting_dic[gram]
    history = list(gram)[:n-1]
    for key in counting_dic.keys():
        if list(key)[:n-1] == history:
            count_of_history += counting_dic[key]
    return count_of_gram / count_of_history


def probability(phrase, n):
    """
    :param phrase:
    this is the phrase you want to see the probability of
    :param n:
    n is the gram of the phrase you want to test
    :return:
    the probabilty of the phrase
    """
    probabilities = []
    grams = nltk.ngrams(cleanup(phrase), n)
    for gram in grams:
        probabilities.append(probability_word(gram, n))
    sum = 0
    if n > 1:
        for number in probabilities:
            sum += math.log(number)
            sum = math.exp(sum)
    else:
        for number in probabilities:
            sum *= number
    return sum


if __name__ == '__main__':
    os.chdir(os.path.join(os.getcwd(), 'TrainingSet'))
    parent = os.getcwd()
    for directory in os.listdir(parent):
        os.chdir(os.path.join(parent, directory))
        for file in os.listdir(os.getcwd()):
            read_file = open(file, 'r')
            text = get_text(read_file.readlines())
            text2 = []
            for line in text:
                text2.append(" ".join(cleanup(line)))
            text2 = " ".join(text2)
            text2 = re.split('[.?!]', text2)
            for line in text2:
                scentence = line
                line = line.split(" ")
                unigrams.extend(list(nltk.ngrams(line, 1)))
                bigrams.extend(list(nltk.ngrams(line, 2)))
                trigrams.extend(list(nltk.ngrams(line, 3)))
                quadgrams.extend(list(nltk.ngrams(line, 4)))
                probability(scentence, 1)
                probability(scentence, 2)
                probability(scentence, 3)
                probability(scentence, 4)
    count_dic(unigram_dic, unigrams)
    count_dic(bigram_dic, bigrams)
    count_dic(trigram_dic, trigrams)
    count_dic(quadgram_dic, quadgrams)
    print(probability("when the prosecution is expected to offer a rebuttal", 3))
