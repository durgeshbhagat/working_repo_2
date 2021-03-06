#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# This code is available under the MIT License.
# (c)2010-2011 Nakatani Shuyo / Cybozu Labs Inc.
# Modified By Durgesh Kumar
# Last Mofified date : 6th March 2017

import numpy
import time
import os
from datetime import datetime
import vocabulary


out_dir = 'results'

try:
    os.makedirs(out_dir)
except:
    print('%s dir exist' %(out_dir))


def check_for_negative_values(a):
        ''' return True if any value in 1 D array is -ve False otherwise '''
        new_a = (a>0.0).all()
        if new_a == False :
            print(' a : ' , a , False)
        # print('new_a :: ' , new_a)
        return (1-new_a)
            
class LDA:
       
    def __init__(self, K, alpha, eta1,eta2, docs,doc_ids, V1,V2, smartinit=True):
        self.K = K
        self.alpha =  numpy.full(K, alpha, dtype=float) # parameter of topics prior
        self.eta1 = eta1#numpy.full(V1, eta1, dtype=float)  # parameter of words prior  for Named Entity (N.E)
      
                
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
        self.n_z1 = numpy.zeros(K) +  sum(self.eta1)     # word count of each topic # mistake Found! sum(self.eta1) instead of V1 * sum(self.eta1)
        # Variables for n.n.e
        self.n_z_t2  = numpy.zeros((K, V2)) + eta2 # word count of each topic and vocabulary 
        self.n_z2 = numpy.zeros(K) +   sum(self.eta2)     # word count of each topic #Mistake Found,  sum(self.eta2)  instead V2 *  sum(self.eta2)   
        
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
                    # print(' P_Z shape : ', p_z.shape, p_z)
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
            
        # check_for_negative_values(self.n_m_z)
        for i in range(K):
            if(check_for_negative_values(self.n_z_t1[i])):
                print(' i : %d , n_z_t1 in initalization ' % (i))
                exit() 
        for i in range(K):
            if(check_for_negative_values(self.n_z_t2[i])):
                print(' i : %d , n_z_t2 in initalization ' % (i))
                exit() 
                
        # print(' self.z_m_n  in INIT :: ' , self.z_m_n)
        # print(' self.n_m_z :: in INIT :: ' , self.n_m_z)
        # print(' self.n_z_t1 ::  in INIT' , self.n_z_t1)
        # print('self.n_z_t2 :: in INIT ' , self.n_z_t2)
        # print('self.n_z1 :: INIT ' , self.n_z1)
        # print('self.n_z2 :: INIT ' , self.n_z2)
        
        # print ' \n END of INIT ::: ------------------- \n\n\n'
        
        #check_for_negative_values(self.n_z1)
        #check_for_negative_values(self.n_z2)
        
        
        
    def inference(self):
        """learning once iteration"""
        # print('Iternation no in inference :: ' , self.iter_count)
        for m, doc in enumerate(self.docs):
            #z_m_n = self.z_m_n
            #n_m_z = self.n_m_z
            for n, t in enumerate(doc[0]):
                # discount for n-th word t with topic z
                # print(' Cur z_m_n[m] ' , self.z_m_n[m])
                z = self.z_m_n[m][0][n]
                self.n_m_z[m][z] -= 1
                if self.n_m_z[m][z] < 0.0  :
                    print(' less than zero , prev value : %f ' % (1+ n_m_z[m][z]))
                # if it is n.e
                self.n_z_t1[z, t] -= 1
                if self.n_z_t1[z, t] < 0.0  :
                    print(' less than zero , prev value : %f '  %(1+ self.n_z_t1[z,t]))
                self.n_z1[z] -= 1
                
                # sampling topic new_z for t
                #if it is n.e
                p_z = (self.n_m_z[m] * self.n_z_t1[:, t] ) / self.n_z1
                if(check_for_negative_values(p_z)):
                    print(' NE ::' , m , n,z)
                    print('self.n_m_z  : ' , self.n_m_z)
                    print(' self.n_z_t1 : ' ,  self.n_z_t1)
                    print('self.n_z1 : ' , self.n_z1)
                    exit()
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                # set z the new topic and increment counters
                self.z_m_n[m][0][n] = new_z
                 
                #if m ==0 and n==0 :
                #    print(' new_z = %d for m=0 , n= 0 , self.n_z_t1[new_z][0]=%f ' % (new_z,self.n_z_t1[new_z][0]))
                self.n_m_z[m][new_z] += 1
                
                #if it is n.e
                self.n_z_t1[new_z, t] += 1 
                #if m ==0 and n==0 :
                #    print(' new_z = %d for m=0 , n= 0 , self.n_z_t1[new_z][0]=%f ' %(new_z,self.n_z_t1[new_z][0]))
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
                print('self.n_m_z  : ' , self.n_m_z[m])
                print(' self.n_z_t2 : ' ,  self.n_z_t2[:,t])
                print('self.n_z2 : ' , self.n_z2)
                
                '''
                p_z = ( self.n_m_z[m] * self.n_z_t2[:, t] ) / self.n_z2
                if(check_for_negative_values(p_z)):
                    print(' nne :: ' , m, n, z)
                    print('self.n_m_z  : ' , self.n_m_z[m])
                    print(' self.n_z_t2 : ' ,  self.n_z_t2[:,t])
                    print('self.n_z2 : ' , self.n_z2)
                    exit()
                # print(' p_z shape ::', p_z.shape, p_z)
                # print(' p_z sum  for Non Ner: ', p_z)
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                # print('new_z' , new_z)
        
                # set z the new topic and increment counters
                self.z_m_n[m][1][n] = new_z
                self.n_m_z[m][new_z] += 1
                
        
                #if it is n.n.e
                self.n_z_t2[new_z, t] += 1
                self.n_z2[new_z] += 1
                        
        # print(' self.z_m_n :: ' , self.z_m_n)
        # print(' self.n_m_z :: ' , self.n_m_z)
        # print(' self.n_z_t1 :: ' , self.n_z_t1)
        # print('self.n_z_t2 ::' , self.n_z_t2)
        # print('self.n_z1 :: ' , self.n_z1)
        # print('self.n_z2 :: ' , self.n_z2)
                    
        print(' - - End of iteration # %d --' %(self.iter_count))
    def worddist(self):
        ''' get topic-word distribution '''
        # print('self.n_z new axis' , self.n_z,self.n_z[:, numpy.newaxis].shape, self.n_z_t.shape)
        # print(self.n_z_t)
        # print(self.n_z_t / self.n_z[:,numpy.newaxis])
        
        # returns normalized P ( z| t) --- divided by row sum : numpy.newaxis extend the dimension 
        return self.n_z_t / self.n_z[:, numpy.newaxis]
    
    def worddist_sp(self):
        '''  get topic-word dist for ner  '''
        return self.n_z_t1 / self.n_z1[:,numpy.newaxis]
    
    def worddist_nsp(self):
        '''  get topic-word dist for Non  ner  '''
        return self.n_z_t2 / self.n_z2[:,numpy.newaxis]    
       
    def doc_topic_dist(self):
        # print(self.n_m_z)
        return self.n_m_z / self.n_m_z.sum(axis=1)[:,numpy.newaxis]

    def perplexity(self, docs=None):
        if docs == None: docs = self.docs
        #phi = self.worddist()
        
        phi_sp = self.worddist_sp()
        phi_nsp = self.worddist_nsp()
        log_per = 0
        N = 0
        Kalpha = self.K * self.alpha
        for m, doc in enumerate(docs):
            length_doc = len(self.docs[m][0]) + len(self.docs[m][1]) 
            theta = self.n_m_z[m] / ( length_doc + Kalpha)
            for w in doc[0]:
                log_per -= numpy.log(numpy.inner(phi_sp[:,w], theta))
            for w in doc[1]:
                log_per -= numpy.log(numpy.inner(phi_nsp[:,w], theta))
            N += length_doc
        return numpy.exp(log_per / N)
    

def lda_learning(lda, iteration, voca):
    
    pre_perp = lda.perplexity()
    print("initial perplexity=%f" % pre_perp)
    for i in range(iteration):
        t1 = time.time()
        lda.inference()
        perp = lda.perplexity()
        flog = '%s/log_file.txt' %(out_dir)
        f=open(flog,'a')
        
        # print(' lda.z_m_n[0] ' , lda.z_m_n[0])
        # print(' lda.n_z_t[:,0] ' ,lda.n_z_t1[:,0])
        f.write("-%d p=%f\n" % (i + 1, perp))
        f.close()
        print("-%d p=%f ," % (i + 1, perp), end=' '),
        if pre_perp:
            if pre_perp < perp:
                #output_word_topic_dist(lda, voca)
                pre_perp = None
            else:
                pre_perp = perp
        lda.iter_count +=1
        t2 = time.time()
        print('Iteration # ::  %d , time taken : %f '  %(lda.iter_count, (t2-t1)), end=' ,')
    output_word_topic_dist(lda, voca)
    output_doc_topic_dist(lda,voca)
    output_doc_topic_dist_all(lda,voca)
    
def output_doc_topic_dist(lda,voc):
    doc_topic_dist =  lda.doc_topic_dist()
    doc_topic_assignment =numpy.argmax( doc_topic_dist, axis= 1)
    # print(doc_topic_assignment.shape)
    fout = '%s/doc_topic_dist.txt' %(out_dir)
    f=open(fout,'w')
    for i,item in enumerate(doc_topic_assignment):
        # print("%s : Topic_%d" %(lda.doc_ids[i], item+1))
        f.write( "%s : Topic_%d \n" %(lda.doc_ids[i], item+1))
    f.close()
    # for item in doc_topic_assignment :
    #    print(item)
   
def output_doc_topic_dist_all(lda,voc):
    """ Store the score of doc topic matrix """
    doc_topic_dist =  lda.doc_topic_dist()
    st = 'Doc_Id '
    for i in range(lda.K):
        st +=' , Topic_%03d' %(i)
    st += '\n'
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
    wordcount_sp = [dict() for k in range(lda.K)]
    wordcount_nsp = [ dict() for k in range(lda.K)]
    # print('Type wordcount' , type(wordcount) , wordcount[0],wordcount[1])
    for xlist, zlist in zip(lda.docs, lda.z_m_n):
        # xlist_new = xlist[0] + xlist[1]
        # print('xlist , zlist' , xlist,zlist)
        for x, z in zip(xlist[0], zlist[0]):
            # print('x is ::   ' , x)
            # print(' Z is ::: ' , z)
            zcount[z] += 1
            if x in wordcount_sp[z]:
                wordcount_sp[z][x] += 1
            else:
                wordcount_nsp[z][x] = 1
        for x, z in zip(xlist[1], zlist[1]):
            # print('x is ::   ' , x)
            # print(' Z is ::: ' , z)
            zcount[z] += 1
            if x in wordcount_nsp[z]:
                wordcount_nsp[z][x] += 1
            else:
                wordcount_nsp[z][x] = 1     
    phi_sp = lda.worddist_sp()
    phi_nsp = lda.worddist_nsp()
    fout = '%s/topic_word_dist.txt' %(out_dir) 
    f=open(fout,'w')
    for k in range(lda.K):
        f.write("\n\n\n-- topic: %d (%d words)" % (k, zcount[k]))
        f.write(" \n*************  NER terms \n")
        # print("\n\n\n-- topic: %d (%d words)" % (k, zcount[k]))
        # print( " \n*************  NER terms ")
        for w in numpy.argsort(-phi_sp[k])[:30]:
            # print(w, voca.__getitem__(w,'sp'))
            # print("%s: %f (%d)" % (voca[w], phi_ner[k,w], wordcount_ner[k].get(w,0)))
            f.write("%s: %f (%d)\n" % (voca.__getitem__(w,'sp'), phi_sp[k,w], wordcount_sp[k].get(w,0)))
        # print(" \n+++++++++++++ Non Ner term ")
        f.write(" \n+++++++++++++ Non Ner term \n")
        for w in numpy.argsort(-phi_nsp[k])[:30]:
            # print(w, voca.__getitem__(w,'nsp'))
            # print("%s: %f (%d)" % (voca.__getitem__(w,'Nner'), phi_Nner[k,w], wordcount_Nner[k].get(w,0)))
            f.write("%s: %f (%d)\n" % (voca.__getitem__(w,'nsp').encode('ascii', 'ignore'), phi_nsp[k,w], wordcount_nsp[k].get(w,0)))    
    f.close()


def initialize_eta1(V1, voca,fname):
    ''' Intitalize the dicichlet paprameter of special word from the file '''
    eta1 =numpy.full(V1,0.001, dtype=float)  # parameter of words prior  for Named Entity (N.E)
    # Read file and initialize
    fname_total = '%s/%s' %('weightage_file',fname) 
    f=open(fname_total,'r')
    line_list =f.read().strip().split('\n')
    for i,line in enumerate(line_list):
        # print(' line:' , line)
        word, score = line.strip().split(' #,# ')
        if word in voca.vocas_id_sp:
            # print(' Found ::' , word)
            word_id = voca.vocas_id_sp[word]
            eta1[word_id] = score
        '''
        a) read line by line 
        b) word to word id 
        c) intialize eta1 for corresponding word id 
        '''
    return eta1   

def init_special_words(fname):
    special_words= {}
    fname_total = '%s/%s' %('weightage_file',fname)
    print('weighatge file ::', fname_total)
    f=open(fname_total,'r')
    line_list =f.read().strip().split('\n')
    for i,line in enumerate(line_list):
        # print(' line:' , line, i)
        word, score = line.strip().split(' #,# ')
        special_words[word] = score 
       
    return special_words  


def main():
    t1= time.time()
    import optparse

    global out_dir 
    parser = optparse.OptionParser()
    parser.add_option("--finp", dest="filename_ip", help="input filename")
    parser.add_option("--fsp", dest="filename_sp", help="special words filename")
    parser.add_option("-c", dest="corpus", help="using range of Brown corpus' files(start:end)")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
    parser.add_option("--eta1", dest="eta1", type="float", help="parameter eta for ner word", default=0.4)
    parser.add_option("--eta2", dest="eta2", type="float", help="parameter eta for Non-ner word", default=0.2) # No eta 2 here !!
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=10)
    parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document freaquency to cut words", default=0)
    parser.add_option("--dp", dest="dp", help="ditichlet prior sysmetric or asymmetric ?")
    parser.add_option("--setup", dest="setup", help="setup details")
    parser.add_option("--datasets", dest="did", help="setup details",default="dataset_1")
    (options, args) = parser.parse_args()
    #if not (options.filename_ip or options.corpus): parser.error("need corpus filename(-f) or corpus range(-c)")
    
    if options.filename_ip and options.filename_sp:
         special_words = init_special_words(options.filename_sp)
         if options.did == 'Dataset-1':
            corpus,doc_ids, event_list  =   vocabulary.load_file(options.filename_ip,special_words) 
         else:
            corpus,doc_ids, event_list  =   vocabulary.load_file_reuter(options.filename_ip,special_words)
         # print(' Line 420 ...')
    else:
        options.filename_ip = 'filtered_event_new2.pkl'
        options.filename_sp = ''
        special_words = init_special_words(options.filename_sp) 
        corpus,doc_ids, event_list  = vocabulary.load_file(options.filename_ip,special_words)
        # corpus = vocabulary.load_corpus(options.corpus)
        # if not corpus: parser.error("corpus range(-c) forms 'start:end'")
    if options.seed != None:
        numpy.random.seed(options.seed)
    # print(' Line 430')
    voca = vocabulary.Vocabulary(options.stopwords,special_words)
    # print(' Line 432')
    docs = [voca.doc_to_ids(doc) for doc in corpus]
    # print(' Line 433')
    
 
    if options.df > 0: docs = voca.cut_low_freq(docs, options.df)
    
    if event_list is not None : options.K  = options.K #len(event_list)
    suffix = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    V1,V2 = voca.size() # Total no of uniq word 
    # print(' Initialization of eta 1 started ..')
    eta1 = initialize_eta1(V1, voca,options.filename_sp) # Modify intialize_eta1 method
    # print(' Initialization of et1 done !!! ..')
    
    # out_dir = '%s/all_words/Topic_%d_alpha_%f_eta1_%f_eta2_%f_iter_%d/%s' %(out_dir,options.K,options.alpha, options.eta1,options.eta2, options.iteration, suffix)
    # out_dir = '%s/all_words/Topic_%d_alpha_%f_eta2_%f_%s_iter_%d/%s' %(out_dir,options.K,options.alpha,options.eta2,options.filename_sp, options.iteration, suffix) # Modify out_dir
    fname_sp = options.filename_sp.replace('/', '-')
    if 'ner_keywords' in options.setup:
        out_dir = '%s/%s/%s/%s_Topic-%d_alpha-%0.2f_eta2-%0.2f_eta1-%0.2f_iter_%d/%s' %(out_dir, options.did,
                                             options.setup, options.did, options.K, options.alpha, options.eta2, options.eta1, options.iteration, suffix)
    elif 'tf-df-icf' in options.setup:
        out_dir = '%s/%s/%s/%s_Topic-%d_alpha-%0.2f_eta2-%0.2f_eta1-%0.2f_iter_%d/%s' %(out_dir, options.did,
                                             options.setup, options.did, options.K, options.alpha, options.eta2, options.eta1, options.iteration, suffix)
    elif 'IG' in options.setup:
        out_dir = '%s/%s/%s/%s_Topic-%d_alpha-%0.2f_eta2-%0.2f_eta1-%0.2f_iter_%d/%s' %(out_dir, options.did,
                                             options.setup, options.did, options.K, options.alpha, options.eta2, options.eta1, options.iteration, suffix)
    else:
        print('Out Directory is not defined')
        return
    print(' out_dir line 448 : : ' , out_dir)
    try:
        os.makedirs(out_dir)
    except Exception as e:
        print(' %s Dir exist ' %(out_dir))
        # print('E MSG : ' , e)
    # lda = LDA(options.K, options.alpha, options.eta, docs, doc_ids, voca.size(), options.smartinit)
 
    print('V1 = %d , V2 = %d ' %(V1,V2)) # How to get V1 and V2
    '''
    print(' Docs :: ') 
    
    for i,doc in enumerate(docs):
        (print 'doc : ' , i, doc)
        
    print(' printing Doc Over  \n \n ')
    '''
    

    lda = LDA(options.K, options.alpha, eta1, options.eta2, docs, doc_ids, V1,V2, smartinit=True) # hv to rechechk and modify options.smartint here #Modify here and LDA class 
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'w')
    f.write("corpus=%d, V1_ner = %d , V2_Nner =%d, K=%d, alpha=%0.2f , eta_2_Nner = %0.2f,  iteration = %d \n" % (len(corpus), V1, V2, options.K, options.alpha, options.eta2, options.iteration))  # Modify here !
    f.write('Dataset-%s , input_file = %s, special word file = %s \n'  %(options.did, options.filename_ip, options.filename_sp) )
    f.close()

    print("corpus=%d, V1_ner = %d , V2_Nner =%d, K=%d, alpha=%0.2f, eta_2_Nner = %0.2f,  iteration = %d \n" % (len(corpus), V1, V2,
                                                                    options.K, options.alpha, options.eta2, options.iteration)) # Modify here @

    # import cProfile
    # cProfile.runctx('lda_learning(lda, options.iteration, voca)', globals(), locals(), 'lda.profile')
    lda_learning(lda, options.iteration, voca) #check this function
    t2= time.time()
    print(' Total time taken : %f ' %(t2-t1))
    flog = '%s/log_file.txt' %(out_dir)
    f=open(flog,'a')
    f.write(' TOtal time taken : %f ' %(t2-t1))
    f.close()
    
if __name__ == "__main__":
    main()
