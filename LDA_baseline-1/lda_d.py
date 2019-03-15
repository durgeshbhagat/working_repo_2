#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# This code is available under the MIT License.
# (c)2010-2011 Nakatani Shuyo / Cybozu Labs Inc.
#Modified By Durgesh Kumar 
#  Last Modified Date : 21st Feb 2017, 21st novemember 2016
#  Used for LDA using Gibbs Sampling


import numpy
import time
import os
from datetime import datetime

out_dir = 'results'

try:
    os.makedirs(out_dir)
except:
    pass
    #print '%s dir exist' %(out_dir)

class LDA:
    def __init__(self, K, alpha, eta, docs,doc_ids, V, smartinit=True):
        self.K = K
        self.alpha =  numpy.full(K, alpha, dtype=float) # parameter of topics prior
        self.eta =numpy.full(V, eta, dtype=float)  # parameter of words prior
        self.docs = docs
        self.doc_ids = doc_ids
        self.V = V

        self.z_m_n = [] # topics of words of documents
        self.n_m_z = numpy.zeros((len(self.docs), K)) + self.alpha     # Modify here to consider for vector :: # word count of each document and topic
        self.n_z_t = numpy.zeros((K, V)) + self.eta   # Modify here to consider for Vector :: # word count of each topic and vocabulary
        self.n_z = numpy.zeros(K) + sum(self.eta)  ## Modify here to consider for Vector :: #   word count of each topic

        #print 'self.n_z : ' , self.n_z
        self.N = 0
        for m, doc in enumerate(docs):
            self.N += len(doc)
            z_n = []
            for t in doc:
                if smartinit:
                    #print self.n_z_t[:,t].shape , self.n_m_z[m].shape , self.n_z.shape, (self.n_z_t[:,t] * self.n_m_z[m]).shape
                    #print self.n_z_t[:,t] , self.n_m_z[m] , self.n_z_t[:,t] * self.n_m_z[m]
                    p_z = self.n_z_t[:, t] * self.n_m_z[m] / self.n_z
                    #print ' P_Z shape : ', p_z.shape, p_z
                    z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                else:
                    z = numpy.random.randint(0, K)
                z_n.append(z)
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1
            self.z_m_n.append(numpy.array(z_n))

    def inference(self):
        """learning once iteration"""
        for m, doc in enumerate(self.docs):
            z_n = self.z_m_n[m]
            n_m_z = self.n_m_z[m]
            for n, t in enumerate(doc):
                # discount for n-th word t with topic z
                z = z_n[n]
                n_m_z[z]-= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1

                # sampling topic new_z for t
                p_z = self.n_z_t[:, t] * n_m_z / self.n_z
                #print ' p_z shape ::', p_z.shape, p_z
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                #print 'new_z' , new_z

                # set z the new topic and increment counters
                z_n[n] = new_z
                n_m_z[new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

    def worddist(self):
        """get topic-word distribution"""
        #print 'self.n_z new axis' , self.n_z,self.n_z[:, numpy.newaxis].shape, self.n_z_t.shape
        #print self.n_z_t
        #print self.n_z_t / self.n_z[:,numpy.newaxis]
        return self.n_z_t / self.n_z[:, numpy.newaxis]
    def doc_topic_dist(self):
        #print self.n_m_z
        return self.n_m_z / self.n_m_z.sum(axis=1)[:,numpy.newaxis]

    def perplexity(self, docs=None):
        if docs == None: docs = self.docs
        phi = self.worddist()
        log_per = 0
        N = 0
        Kalpha = self.K * self.alpha
        for m, doc in enumerate(docs):
            theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
            for w in doc:
                log_per -= numpy.log(numpy.inner(phi[:,w], theta))
            N += len(doc)
        return numpy.exp(log_per / N)


def lda_learning(lda, iteration, voca):
    pre_perp = lda.perplexity()
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'a')
    print("initial perplexity=%f" %(pre_perp), end=' ,')
    for i in range(iteration):
        t_start = time.time()
        lda.inference()
        perp = lda.perplexity()
        t_end =time.time()
        f.write("-%d p=%f\t time taken : %f\n" %(i + 1, perp,(t_end-t_start)))
        #print "-%d p=%f \t Time taken : %f" %(i + 1, perp, (t_end-t_start) )
        '''if pre_perp:
            if pre_perp < perp:
                #output_word_topic_dist(lda, voca)
                pre_perp = None
            else:
                pre_perp = perp
        '''
        print('\tTime taken for iteration %d : %f, perplexity : %f' %(i, (t_end - t_start), perp))
    f.close()
    perp = lda.perplexity()
    print(' | Final Perplexity : %f ' %(perp), end=' ,')
    output_word_topic_dist(lda, voca)
    output_doc_topic_dist(lda,voca)
    output_doc_topic_dist_all(lda,voca)

def output_doc_topic_dist(lda,voc):
    doc_topic_dist =  lda.doc_topic_dist()
    doc_topic_assignment =numpy.argmax( doc_topic_dist, axis= 1)
    #print doc_topic_assignment.shape
    fout = '%s/doc_topic_dist.txt' %(out_dir)
    f=open(fout,'w')
    for i,item in enumerate(doc_topic_assignment):
        #print "%s : Topic_%d" %(lda.doc_ids[i], item+1)
        f.write( "%s : Topic_%d \n" %(lda.doc_ids[i], item+1))
    f.close()

def output_doc_topic_dist_all(lda,voc):
    """ Store the score of doc topic matrix """
    doc_topic_dist =  lda.doc_topic_dist()
    st = 'Doc_Id '
    for i in range(lda.K):
        st +=' , Topic_%03d' %(i)
    st +='\n'
    for i, doc_id in enumerate(lda.doc_ids):
        st += '%s' %(doc_id)
        for j,topic_id in enumerate(doc_topic_dist[i]):
            st +=', %f' %(doc_topic_dist[i][j])
        st +='\n'
    fout = '%s/doc_topic_dist_score.csv' %(out_dir)
    f=open(fout,'w') 
    f.write(st)
    f.close()
    
    
def output_word_topic_dist(lda, voca):
    zcount = numpy.zeros(lda.K, dtype=int)
    wordcount = [dict() for k in range(lda.K)]
    #print 'Type wordcount' , type(wordcount) , wordcount[0],wordcount[1]
    for xlist, zlist in zip(lda.docs, lda.z_m_n):
        #print 'xlist , zlist' , xlist,zlist
        for x, z in zip(xlist, zlist):
            zcount[z] += 1
            if x in wordcount[z]:
                wordcount[z][x] += 1
            else:
                wordcount[z][x] = 1

    phi = lda.worddist()
    fout = '%s/topic_word_dist.txt' %(out_dir) 
    f=open(fout,'w')
    for k in range(lda.K):
        f.write("\n\n-- topic: %d (%d words)\n" % (k, zcount[k]))
        #print ("\n-- topic: %d (%d words)" % (k, zcount[k]))
        for w in numpy.argsort(-phi[k])[:50]:
            #print ("%s: %f (%d)" % (voca[w], phi[k,w], wordcount[k].get(w,0)))
            f.write("%s: %f (%d)\n" % (voca[w], phi[k,w], wordcount[k].get(w,0)))
    f.close()

def main():
    t1= time.time()
    import optparse
    import vocabulary
    global out_dir 
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    parser.add_option("-c", dest="corpus", help="using range of Brown corpus' files(start:end)")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.1)
    parser.add_option("--eta", dest="eta", type="float", help="parameter eta", default=0.2)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document freaquency to cut words", default=0)
    #parser.add_option("--setup", dest="setup", help="setup details", default="uniform")
    parser.add_option("--dataset", dest="did", help="setup details : Dataset-1/Dataset-2/Dataset-3",default="Dataset-1")
    (options, args) = parser.parse_args()
    if not (options.filename or options.corpus): parser.error("need corpus filename(-f) or corpus range(-c)")

    if options.filename:
        if options.did == 'Dataset-1':
            corpus,doc_ids, event_list, total_no_word  = vocabulary.load_file(options.filename)
        else:
            corpus,doc_ids, event_list, total_no_word  = vocabulary.load_file_reuter(options.filename)
    else:
        corpus = vocabulary.load_corpus(options.corpus)
        if not corpus: parser.error("corpus range(-c) forms 'start:end'")
    if options.seed != None:
        numpy.random.seed(options.seed)
    
    voca = vocabulary.Vocabulary(options.stopwords)
    docs = [voca.doc_to_ids(doc) for doc in corpus]
    if options.df > 0: docs = voca.cut_low_freq(docs, options.df)
    
    if event_list is not None : options.K  = options.K #len(event_list)
    suffix = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    #out_dir = '%s/all_words/Topic_%d_alpha_%f_eta_%f_iter_%d/%s' %(out_dir,options.K,options.alpha, options.eta, options.iteration, suffix)
    #out_dir = '%s/Dataset-1/Topic_%d_alpha_%f_eta_%f_iter_%d/%s' %(out_dir,options.K,options.alpha, options.eta, options.iteration, suffix)
    out_dir = '%s/%s/Topic_%d_alpha_%f_eta_%f_iter_%d/%s' %(out_dir, options.did, options.K, options.alpha, options.eta, options.iteration, suffix)
    
    #out_dir = '%s/Reuters-21578/R-8-train-train_no-stop/Topic_%d_alpha_%f_eta_%f_iter_%d/%s' %(out_dir,options.K,options.alpha, options.eta, options.iteration, suffix)
    #out_dir = '%s/20-Newsgroup/20-Newsgroup_train-train_all_term/Topic_%d_alpha_%f_eta_%f_iter_%d/%s' %(out_dir,options.K,options.alpha, options.eta, options.iteration, suffix)
    print('out_dir: ', out_dir)
    try:
        os.makedirs(out_dir)
    except Exception as e:
        print(' %s Dir exist ' %(out_dir))
        print('E MSG : ' , e)
    lda = LDA(options.K, options.alpha, options.eta, docs, doc_ids, voca.size(), options.smartinit)
    t_int = time.time()
    #print 'Intialization time : %f' %(t_int-t1) 
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'w')
    f.write("corpus(# of doc)=%d, no of event = %d , Uniq words=%d, Toal # of word =%d, K=%d, a=%f, b=%f , iteration = %d \n" % (len(corpus), len(event_list), len(voca.vocas), total_no_word, options.K, options.alpha, options.eta,options.iteration))
    f.close()
    print("corpus=%d, no of event =%d , uniq words=%d, K=%d, a=%f, b=%f" % (len(corpus), len(event_list), len(voca.vocas), options.K, options.alpha, options.eta)),

    #import cProfile
    #cProfile.runctx('lda_learning(lda, options.iteration, voca)', globals(), locals(), 'lda.profile')
    lda_learning(lda, options.iteration, voca)
    t2= time.time()
    print(' Total time taken : %f ' %(t2-t1))
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'a')
    f.write(' TOtal time taken : %f ' %(t2-t1))
    f.close()
    
if __name__ == "__main__":
    main()
