def generate_keywords_file():
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    stemmer = PorterStemmer()
    import gensim
    import nltk
    import os

    datadir = "/home/tanishq/MAVIS/DotSlash2020/Working_code/main/finalworkingcode/"
    #categories = ["bsearch.txt","sort.txt","queue.txt","stack.txt","tries_n.txt","graph_n.txt","neural-net_n.txt","dbms_n.txt"]
    #categories = ["sort.txt"]
    categories = ["captions.txt"]
    topics = ["bsearch","sort","queue","stack","trie","graph","Neural-Networks","sorted","tries","search","dbms"]

    #def lemmatize_stemming(text):
    #   return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    # Tokenize and lemmatize
    def preprocess(text):
        result=[]
        for token in gensim.utils.simple_preprocess(text) :
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(WordNetLemmatizer().lemmatize(token, pos='v'))
                
        return result

    processed_docs = []

    for doc in categories:
        f = open(os.path.join(datadir,doc))
        processed_docs.append(preprocess(f.read()))


    dictionary = gensim.corpora.Dictionary(processed_docs)
    #dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    sum_v=[]

    for j in range(len(bow_corpus)):
        curr=0
        for i in range(len(bow_corpus[j])):
            curr+= bow_corpus[j][i][1]
        sum_v.append(curr)
        
    sum_v=[]

    for j in range(len(bow_corpus)):
        curr=0
        for i in range(len(bow_corpus[j])):
            curr+= bow_corpus[j][i][1]
        sum_v.append(curr)
        

    indexes=[]
    for i in range(len(bow_corpus)):
        #bow_doc = bow_corpus[i]
        for j in range(len(bow_corpus[i])):
            y = list(bow_corpus[i][j]) 
            y[1]= round((y[1]/sum_v[i]),3)
            bow_corpus[i][j]= tuple(y)

    for i in range(len(bow_corpus)):
        bow_corpus[i] = sorted(bow_corpus[0],key = lambda x:x[1])

    percentage = []

    for i in range(len(bow_corpus)):
        val = len(bow_corpus[i])
        val = int(val*2/100)
        percentage.append(val)

    arr=[]
    val =[]
    flag=0
    for i in range(len(bow_corpus)):
        #print(arr)
        if(flag==1):
            break
        arr=[]
        for j in range(len(bow_corpus[i])):
            if(dictionary[bow_corpus[i][j][0]] in topics):
                #print(i,j)
                val.append(dictionary[bow_corpus[i][j][0]])
                flag=1
            else:
                arr.append(dictionary[bow_corpus[i][j][0]])
    arr=[]
    for i in range(len(val)):
        arr.append(val[i])

    #dictionary[bow_corpus[0][115][0]]
    val =[]

    for i in range(len(bow_corpus)):
        for j in range(percentage[i]):
            val.append(dictionary[bow_corpus[i][j][0]])


    for i in range(len(arr)):
        val.insert(0,arr[i])
        
    file = open("words.txt","w")
    file.write("")
    file.close()
    file1 = open("words.txt","a")

    for i in val:
        file1.write(i+"\n")

    file1.close()
