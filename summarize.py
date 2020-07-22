from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

import bs4 as bs
import urllib.request
import re
import nltk

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

    f = open("video_summary.txt", "a")
    # Step 5 - Offcourse, output the summarize texr
    a = ". ".join(summarize_text)
    if(a):
        print("\n\n\nye hai Summarize Text: \n",a)
        f.write("\n\nVIDEO\n")
        f.write(a)

def summarize_caption(filepath):
	generate_summary(filepath)

def summarize_htmlpage(link):

	scraped_data = urllib.request.urlopen(link)
	article = scraped_data.read()

	parsed_article = bs.BeautifulSoup(article,'lxml')

	paragraphs = parsed_article.find_all('p')

	article_text = ""

	for p in paragraphs:
	    article_text += p.text



	# Removing Square Brackets and Extra Spaces
	article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
	article_text = re.sub(r'\s+', ' ', article_text)


	# Removing special characters and digits
	formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
	formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


	sentence_list = nltk.sent_tokenize(article_text)


	stopwords = nltk.corpus.stopwords.words('english')

	word_frequencies = {}
	for word in nltk.word_tokenize(formatted_article_text):
	    if word not in stopwords:
	        if word not in word_frequencies.keys():
	            word_frequencies[word] = 1
	        else:
	            word_frequencies[word] += 1


	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():
	    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


	sentence_scores = {}
	for sent in sentence_list:
	    for word in nltk.word_tokenize(sent.lower()):
	        if word in word_frequencies.keys():
	            if len(sent.split(' ')) < 30:
	                if sent not in sentence_scores.keys():
	                    sentence_scores[sent] = word_frequencies[word]
	                else:
	                    sentence_scores[sent] += word_frequencies[word]

	import heapq
	summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

	summary = ' '.join(summary_sentences)
	print(summary)

# def summarize3(filepath):
#     from gensim.summarization.summarizer import summarize 
#     from gensim.summarization import keywords 
#     import wikipedia 
    

#     with open(filepath) as fp:
#         for line in enumerate(fp):
           
#             # query
#             query = line[1].split().pop()
#             query = "".join(query)


#             # Get wiki content. 
#             wikisearch = wikipedia.page(query) 
#             wikicontent = wikisearch.content 
#             nlp = en_core_web_sm.load() 
#             doc = nlp(wikicontent) 
              
#             # Save the wiki content to a file 
#             # (for reference). 
#             f = open("wikicontent.txt", "w") 
#             f.write(wikicontent) 
#             f.close() 
            
#             # Summary (0.5% of the original content). 
#             summ_per = summarize(wikicontent, ratio = 0.05) 
#             print("Percent summary") 
#             print(summ_per) 
              
#             # Summary (200 words) 
#             summ_words = summarize(wikicontent, word_count = 200) 
#             print("Word count summary") 
#             print(summ_words)

# if __name__ == "__main__":
#     # summarize_htmlpage("https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/")
#     summarize3("words.txt")