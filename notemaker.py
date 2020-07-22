import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import subprocess

from summarize import summarize_htmlpage, summarize_caption

from scrape import generate_scraped_content

from nlp import generate_keywords_file

from youtube_search import generate_transcripts_for_youtube


def debug(x="is this"):
    print("debug msg",x)
 
def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=1000):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(len(ranked_sentence)):
        summarize_text.append(" ".join(ranked_sentence[i][1]))


    # Step 5 - Offcourse, output the summarize texr
    print("\n\n\nSummarize Text: \n", ". ".join(summarize_text))


def make_para(i):
    f = open(i+".txt", "r")
    f2 = open(i+"_n.txt", "a")
    for line in f:
        line = line.rstrip()
        f2.write(line)


def extract_caption(filepath):
    command = "ffmpeg -i "+filepath+" -ab 160k -ac 2 -ar 44100 -vn audio.wav"

    subprocess.call(command, shell=True)

    r = sr.Recognizer()

    PATH = 'audio.wav'

    with sr.AudioFile(PATH) as source:
        audio = r.record(source)

    captions = r.recognize_google(audio)
    print(captions)
    f = open("captions.txt", "w")
    f.write(captions)

# generate_scraped_content("words.txt")


filename = "captions"
caption_filename =  filename + "_n.txt"

extract_caption("test1.mp4")

make_para(filename)

generate_keywords_file()

generate_transcripts_for_youtube("words.txt")

generate_summary(caption_filename)

generate_scraped_content("words.txt")
            
# _-------------- Scarpin here _______________#






