import vocabulary

vocabulary.py
   
    def load_corpus(range): # Load from brown Corpus
    
    def load_file(filename):#modified load_file
    
    def is_stopword(w)
    
    def lemmatize(w0)
    
    class Vocabulary
        def __init__(self, excluds_stopwords=False)
        def term_to_id(self, term0) 
        def doc_to_ids(self, doc)
        def cut_low_freq(self, corpus, threshold=1)
            def conv(doc)
        def __getitem__(self, v)
        def size(self)
        def is_stopword_id(self, id)




lda_d.py
    class LDA
            def __init__(self, K, alpha, eta, docs,doc_ids, V, smartinit=True)
            def inference(self)  """learning once iteration"""
            def worddist(self)    """get topic-word distribution"""
            def doc_topic_dist(self) 
            def perplexity(self, docs=None)
            

    def lda_learning(lda, iteration, voca)

    def output_doc_topic_dist(lda,voc)

    def output_word_topic_dist(lda, voca)


    def main()
