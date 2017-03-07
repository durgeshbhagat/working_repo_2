#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# This code is available under the MIT License.
# (c)2010-2011 Nakatani Shuyo / Cybozu Labs Inc.
#Modified By Durgesh Kumar 
#Last Mofified date : 6th March 2017

import numpy
import time
import os
from datetime import datetime

out_dir = 'results'

try:
    os.makedirs(out_dir)
except:
    print '%s dir exist' %(out_dir)


def check_for_negative_values(a):
        ''' return True if any value in 1 D array is -ve False otherwise '''
        new_a = (a>0.0).all()
        if new_a == False :
            print ' a : ' , a , False
        #print 'new_a :: ' , new_a
        return (1-new_a)
            
class LDA:
       
    def __init__(self, K, alpha, eta1,eta2, docs,doc_ids, V1,V2, smartinit=True):
        self.K = K
        self.alpha =  numpy.full(K, alpha, dtype=float) # parameter of topics prior
        self.eta1 =numpy.full(V1, eta1, dtype=float)  # parameter of words prior  for Named Entity (N.E)
        self.eta2 =numpy.full(V2, eta2, dtype=float)  # paramter of words prior for Non-Name Entity ( N.N.E)
        self.docs = docs # list of list , Actual Corpus
        self.doc_ids = doc_ids
        self.V1 = V1   # of Named Entity
        self.V2 = V2   # of Non Named Entity
        self.iter_count = 0
        
        self.z_m_n = [] # topics of words of documents
        self.n_m_z = numpy.zeros((len(self.docs), K)) + alpha     # word count of each document and topic
        
        # variables for n.e
        self.n_z_t1  = numpy.zeros((K, V1)) + eta1 # word count of each topic and vocabulary
        self.n_z1 = numpy.zeros(K) + V1 * sum(self.eta1)     # word count of each topic
        # Variables for n.n.e
        self.n_z_t2  = numpy.zeros((K, V2)) + eta2 # word count of each topic and vocabulary
        self.n_z2 = numpy.zeros(K) + V2 *  sum(self.eta2)     # word count of each topic
        
        self.N = 0
        for m, doc in enumerate(docs):
            self.N += len(doc)
            z_n = []
            z_ner = []
            for t in doc[0]:
                if smartinit:
                    # if it is n.e  ! How to determine wether a word is n.e 
                    p_z =  self.n_m_z[m] * self.n_z_t1[:, t] / self.n_z1
                    if(check_for_negative_values(p_z)):
                        exit()
                    #print ' P_Z shape : ', p_z.shape, p_z
                    z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                else:
                    z = numpy.random.randint(0, K)
                z_ner.append(z)
                self.n_m_z[m, z] += 1
                # if it is n.e
                self.n_z_t1[z, t] += 1
                self.n_z1[z] += 1
            z_n.append(z_ner)
            z_Nner=[]
            for t in doc[1]:
                if smartinit:
                    # else if it is nne
                    p_z =  self.n_m_z[m] * self.n_z_t2[:, t] / self.n_z2
                    if(check_for_negative_values(p_z)):
                        exit()
                    z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                else:
                    z = numpy.random.randint(0, K)
                    
                z_Nner.append(z)
                self.n_m_z[m, z] += 1
                # if it is n.n.e
                self.n_z_t2[z, t] += 1
                self.n_z2[z] += 1
            
            z_n.append(z_Nner)                    
            self.z_m_n.append(z_n)
            
        #check_for_negative_values(self.n_m_z)
        for i in range(K):
            if(check_for_negative_values(self.n_z_t1[i])):
                print ' i : %d , n_z_t1 in initalization ' %(i)
                exit() 
        for i in range(K):
            if(check_for_negative_values(self.n_z_t2[i])):
                print ' i : %d , n_z_t2 in initalization ' %(i)
                exit() 
                
        #print ' self.z_m_n  in INIT :: ' , self.z_m_n
        #print ' self.n_m_z :: in INIT :: ' , self.n_m_z
        #print ' self.n_z_t1 ::  in INIT' , self.n_z_t1
        #print 'self.n_z_t2 :: in INIT ' , self.n_z_t2
        #print 'self.n_z1 :: INIT ' , self.n_z1 
        #print 'self.n_z2 :: INIT ' , self.n_z2
        
        print ' \n END of INIT ::: ------------------- \n\n\n'
        
        #check_for_negative_values(self.n_z1)
        #check_for_negative_values(self.n_z2)
        
        
        
    def inference(self):
        """learning once iteration"""
        print 'Iternation no in inference :: ' , self.iter_count
        for m, doc in enumerate(self.docs):
            #z_m_n = self.z_m_n
            #n_m_z = self.n_m_z
            for n, t in enumerate(doc[0]):
                # discount for n-th word t with topic z
                #print ' Cur z_m_n[m] ' , self.z_m_n[m]
                z = self.z_m_n[m][0][n]
                self.n_m_z[m][z] -= 1
                if self.n_m_z[m][z] < 0.0  :
                    print ' less than zero , prev value : %f '  %(1+ n_m_z[m][z])
                #if it is n.e
                self.n_z_t1[z, t] -= 1
                if self.n_z_t1[z,t] < 0.0  :
                    print ' less than zero , prev value : %f '  %(1+ self.n_z_t1[z,t])
                self.n_z1[z] -= 1
                
                # sampling topic new_z for t
                #if it is n.e
                p_z = (self.n_m_z[m] * self.n_z_t1[:, t] ) / self.n_z1
                if(check_for_negative_values(p_z)):
                    print ' NE ::' , m , n,z
                    print 'self.n_m_z  : ' , self.n_m_z
                    print ' self.n_z_t1 : ' ,  self.n_z_t1
                    print 'self.n_z1 : ' , self.n_z1
                    exit()
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                # set z the new topic and increment counters
                self.z_m_n[m][0][n] = new_z
                 
                #if m ==0 and n==0 :
                #    print ' new_z = %d for m=0 , n= 0 , self.n_z_t1[new_z][0]=%f ' %(new_z,self.n_z_t1[new_z][0])
                self.n_m_z[m][new_z] += 1
                
                #if it is n.e
                self.n_z_t1[new_z, t] += 1 
                #if m ==0 and n==0 :
                #    print ' new_z = %d for m=0 , n= 0 , self.n_z_t1[new_z][0]=%f ' %(new_z,self.n_z_t1[new_z][0])
                self.n_z1[new_z] += 1
               
            for n, t in enumerate(doc[1],0):
                z = self.z_m_n[m][1][n]
                self.n_m_z[m][z] -= 1
                #if it is n.e
                #if it is n.n.e
                #t_n = t+ self.V1
                self.n_z_t2[z, t] -= 1
                self.n_z2[z] -= 1
                
                #if it is n.n.e
                '''
                print 'self.n_m_z  : ' , self.n_m_z[m]
                print ' self.n_z_t2 : ' ,  self.n_z_t2[:,t]
                print 'self.n_z2 : ' , self.n_z2
                
                '''
                p_z = ( self.n_m_z[m] * self.n_z_t2[:, t] ) / self.n_z2
                if(check_for_negative_values(p_z)):
                    print ' nne :: ' , m, n, z
                    print 'self.n_m_z  : ' , self.n_m_z[m]
                    print ' self.n_z_t2 : ' ,  self.n_z_t2[:,t]
                    print 'self.n_z2 : ' , self.n_z2
                    exit()
                #print ' p_z shape ::', p_z.shape, p_z
                #print ' p_z sum  for Non Ner: ', p_z 
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                #print 'new_z' , new_z
        
                # set z the new topic and increment counters
                self.z_m_n[m][1][n] = new_z
                self.n_m_z[m][new_z] += 1
                
        
                #if it is n.n.e
                self.n_z_t2[new_z, t] += 1
                self.n_z2[new_z] += 1
                        
        #print ' self.z_m_n :: ' , self.z_m_n
        #print ' self.n_m_z :: ' , self.n_m_z
        #print ' self.n_z_t1 :: ' , self.n_z_t1
        #print 'self.n_z_t2 ::' , self.n_z_t2
        #print 'self.n_z1 :: ' , self.n_z1 
        #print 'self.n_z2 :: ' , self.n_z2
                    
        print ' \n ------------- End of iteration Count %d ------- \n\n ' %(self.iter_count)
    def worddist(self):
        ''' get topic-word distribution '''
        #print 'self.n_z new axis' , self.n_z,self.n_z[:, numpy.newaxis].shape, self.n_z_t.shape
        #print self.n_z_t
        #print self.n_z_t / self.n_z[:,numpy.newaxis]
        
        # returns normalized P ( z| t) --- divided by row sum : numpy.newaxis extend the dimension 
        return self.n_z_t / self.n_z[:, numpy.newaxis]
    
    def worddist_ner(self):
        '''  get topic-word dist for ner  '''
        return self.n_z_t1 / self.n_z1[:,numpy.newaxis]
    
    def worddist_Nner(self):
        '''  get topic-word dist for Non  ner  '''
        return self.n_z_t2 / self.n_z2[:,numpy.newaxis]    
       
    def doc_topic_dist(self):
        #print self.n_m_z
        return self.n_m_z / self.n_m_z.sum(axis=1)[:,numpy.newaxis]

    def perplexity(self, docs=None):
        if docs == None: docs = self.docs
        #phi = self.worddist()
        
        phi_ner = self.worddist_ner()
        phi_Nner = self.worddist_Nner()
        log_per = 0
        N = 0
        Kalpha = self.K * self.alpha
        for m, doc in enumerate(docs):
            length_doc = len(self.docs[m][0]) + len(self.docs[m][1]) 
            theta = self.n_m_z[m] / ( length_doc + Kalpha)
            for w in doc[0]:
                log_per -= numpy.log(numpy.inner(phi_ner[:,w], theta))
            for w in doc[1]:
                log_per -= numpy.log(numpy.inner(phi_Nner[:,w], theta))
            N += length_doc
        return numpy.exp(log_per / N)
    

def lda_learning(lda, iteration, voca):
    pre_perp = lda.perplexity()
    print ("initial perplexity=%f" % pre_perp)
    for i in range(iteration):
        '''for item_name  in lda.__dict__.keys():
            print ' Printing Item :: ' , item_name
            temp_dic = lda.__dict__[item_name]
            #print ' Type of temp_dic ' , type(temp_dic)
            if type(temp_dic) == int or type(temp_dic) == float or type(temp_dic) == list :
                continue
            else:
                #t= (0,0)
                t   = temp_dic.shape
                if len(t) >1 :
                    for m in range(t[0]):
                        for n in range(t[1]):
                            if temp_dic[m][n] < 0 :
                                print  ' ---- Negative ---- '
                                return
                else:
                    for m in range(t[0]):
                        if temp_dic[m] < 0 :
                            print ' --Negative --'
                            return
                #print 'temp_dic size : ' , temp_dic.shape()
                #elif type(temp_dic) == np.a'''
        lda.inference()
        perp = lda.perplexity()
        flog = '%s/log_file.txt' %(out_dir)
        f=open(flog,'a')
        
        #print ' lda.z_m_n[0] ' , lda.z_m_n[0]
        #print ' lda.n_z_t[:,0] ' ,lda.n_z_t1[:,0]
        f.write("-%d p=%f\n" % (i + 1, perp))
        f.close()
        print ("-%d p=%f" % (i + 1, perp))
        if pre_perp:
            if pre_perp < perp:
                #output_word_topic_dist(lda, voca)
                pre_perp = None
            else:
                pre_perp = perp
        lda.iter_count +=1
        print ' No of iteration Count :: ' , lda.iter_count
    output_word_topic_dist(lda, voca)
    output_doc_topic_dist(lda,voca)

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
    #for item in doc_topic_assignment :
    #    print item
def output_word_topic_dist(lda, voca):
    zcount = numpy.zeros(lda.K, dtype=int)
    wordcount_ner = [dict() for k in range(lda.K)]
    wordcount_Nner = [ dict() for k in range(lda.K)]
    #print 'Type wordcount' , type(wordcount) , wordcount[0],wordcount[1]
    for xlist, zlist in zip(lda.docs, lda.z_m_n):
        #xlist_new = xlist[0] + xlist[1]	
        #print 'xlist , zlist' , xlist,zlist
        for x, z in zip(xlist[0], zlist[0]):
            #print 'x is ::   ' , x
            #print ' Z is ::: ' , z
            zcount[z] += 1
            if x in wordcount_ner[z]:
                wordcount_ner[z][x] += 1
            else:
                wordcount_ner[z][x] = 1
        for x, z in zip(xlist[1], zlist[1]):
            #print 'x is ::   ' , x
            #print ' Z is ::: ' , z
            zcount[z] += 1
            if x in wordcount_Nner[z]:
                wordcount_Nner[z][x] += 1
            else:
                wordcount_Nner[z][x] = 1     
    phi_ner = lda.worddist_ner()
    phi_Nner = lda.worddist_Nner()
    fout = '%s/topic_word_dist.txt' %(out_dir) 
    f=open(fout,'w')
    for k in range(lda.K):
        f.write("\n\n\n-- topic: %d (%d words)" % (k, zcount[k]))
        f.write(" \n*************  NER terms \n")
        print ("\n\n\n-- topic: %d (%d words)" % (k, zcount[k]))
        print ( " \n*************  NER terms ")
        for w in numpy.argsort(-phi_ner[k])[:30]:
            print ("%s: %f (%d)" % (voca[w], phi_ner[k,w], wordcount_ner[k].get(w,0)))
            f.write("%s: %f (%d)\n" % (voca[w], phi_ner[k,w], wordcount_ner[k].get(w,0)))
        print (" \n+++++++++++++ Non Ner term ")
        f.write(" \n+++++++++++++ Non Ner term \n")
        for w in numpy.argsort(-phi_Nner[k])[:30]:
            print ("%s: %f (%d)" % (voca.__getitem__(w,'Nner'), phi_Nner[k,w], wordcount_Nner[k].get(w,0)))
            f.write("%s: %f (%d)\n" % (voca.__getitem__(w,'Nner').encode('ascii', 'ignore'), phi_Nner[k,w], wordcount_Nner[k].get(w,0)))    
    f.close()

def main():
    t1= time.time()
    import optparse
    import vocabulary 
    global out_dir 
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    parser.add_option("-c", dest="corpus", help="using range of Brown corpus' files(start:end)")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
    parser.add_option("--eta1", dest="eta1", type="float", help="parameter eta for ner word", default=0.4)
    parser.add_option("--eta2", dest="eta2", type="float", help="parameter eta for Non-ner word", default=0.2)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document freaquency to cut words", default=0)
    (options, args) = parser.parse_args()
    #if not (options.filename or options.corpus): parser.error("need corpus filename(-f) or corpus range(-c)")

    if options.filename:
         corpus,doc_ids, event_list  = vocabulary.load_file(options.filename)
    else:
        options.filename = 'filtered_event_new2.pkl'
        corpus,doc_ids, event_list  = vocabulary.load_file(options.filename)
        #corpus = vocabulary.load_corpus(options.corpus)
        #if not corpus: parser.error("corpus range(-c) forms 'start:end'")
    if options.seed != None:
        numpy.random.seed(options.seed)
    
    voca = vocabulary.Vocabulary(options.stopwords)
    docs = [voca.doc_to_ids(doc) for doc in corpus]
    
    '''for  i in range(5):
        print docs[i] 
    
    return'''
    if options.df > 0: docs = voca.cut_low_freq(docs, options.df)
    
    if event_list is not None : options.K  = len(event_list)
    suffix = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    out_dir = '%s/all_words/Topic_%d_alpha_%f_eta1_%f_eta2_%f_iter_%d/%s' %(out_dir,options.K,options.alpha, options.eta1,options.eta2, options.iteration, suffix)
    
    try:
        os.makedirs(out_dir)
    except Exception, e :
        print ' %s Dir exist ' %(out_dir)
        print 'E MSG : ' , e
    #lda = LDA(options.K, options.alpha, options.eta, docs, doc_ids, voca.size(), options.smartinit)
    V1,V2 = voca.size()
    print 'V1 = %d , V2 = %d ' %(V1,V2)
    '''
    print ' Docs :: ' 
    
    for i,doc in enumerate(docs):
        print 'doc : ' , i, doc
        
    print ' printing Doc Over  \n \n ' 
    '''
    
    
    lda = LDA(options.K, options.alpha, options.eta1,options.eta2,docs,doc_ids, V1,V2, smartinit=True) # hv to rechechk and modify options.smartint here
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'w')
    f.write("corpus=%d, V1_ner = %d , V2_Nner =%d, K=%d, alpha=%f, eta1_ner=%f , eta_2_Nner = %f,  iteration = %d \n" % (len(corpus), V1, V2, options.K, options.alpha, options.eta1, options.eta2, options.iteration))
    f.close()
    print "corpus=%d, V1_ner = %d , V2_Nner =%d, K=%d, alpha=%f, eta1_ner=%f , eta_2_Nner = %f,  iteration = %d \n" % (len(corpus), V1, V2, options.K, options.alpha, options.eta1, options.eta2, options.iteration)

    #import cProfile
    #cProfile.runctx('lda_learning(lda, options.iteration, voca)', globals(), locals(), 'lda.profile')
    lda_learning(lda, options.iteration, voca)
    t2= time.time()
    print ' TOtal time taken : %f ' %(t2-t1)
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'a')
    f.write(' TOtal time taken : %f ' %(t2-t1))
    f.close()
    
if __name__ == "__main__":
    main()
