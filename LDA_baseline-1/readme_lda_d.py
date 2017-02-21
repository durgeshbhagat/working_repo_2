import vocabulary




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
