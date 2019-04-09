#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Latent Dirichlet Allocation + collapsed Gibbs sampling
# This code is available under the MIT License.
# (c)2010-2011 Nakatani Shuyo / Cybozu Labs Inc.
#Modified By Durgesh Kumar 
#  Last Modified Date : 21st Feb 2017, 21st novemember 2016
#  Used for LDA using Gibbs Sampling


import numpy as np
from scipy.sparse import csr_matrix
import time
import os
from datetime import datetime
import pandas as pd

import json

out_dir = '../results'
SEED_DIR = '../seed_word'




import guidedlda



try:
    os.makedirs(out_dir)
except:
    pass
    #print '%s dir exist' %(out_dir)


def load_seed_word(seed_topics_fname, vocas_id, event_list):
    fin = open(seed_topics_fname, 'r')
    event2term = json.load(fin)
    seed_topics = {}
    for event in event2term:
        for term in event2term[event]:
            if term in vocas_id:
                seed_topics[vocas_id[term]]  = event_list.index(event)
    # load seed word for ner case ; make setup ==NER
    return seed_topics

def main():
    t1= time.time()
    import optparse
    import vocabulary
    global out_dir 
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    parser.add_option("-c", dest="corpus", help="using range of Brown corpus' files(start:end)")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.1)
    parser.add_option("--eta1", dest="eta1", type="float", help="parameter eta for ner word", default=0.4)
    parser.add_option("--eta2", dest="eta2", type="float", help="parameter eta for Non-ner word", default=0.2)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document freaquency to cut words", default=0)
    parser.add_option("--setup", dest="setup", help="setup details : ner_keywords/tf-df-iec/IG", default="ner_keywords")
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
        np.random.seed(options.seed)

    # fname_sp = options.filename_sp.replace('/', '-')
    # if 'ner_keywords' in options.setup:
    #     out_dir = '%s/%s/%s/%s_Topic-%d_alpha-%0.2f_eta2-%0.2f_eta1-%0.2f_iter_%d/%s' %(out_dir, options.did,
    #                                          options.setup, options.did, options.K, options.alpha, options.eta2, options.eta1, options.iteration, suffix)
    # elif 'tf-df-icf' in options.setup:
    #     out_dir = '%s/%s/%s/%s_Topic-%d_alpha-%0.2f_eta2-%0.2f_eta1-%0.2f_iter_%d/%s' %(out_dir, options.did,
    #                                          options.setup, options.did, options.K, options.alpha, options.eta2, options.eta1, options.iteration, suffix)
    # else:
    #     print('Out Directory is not defined')
    #     return
    # print(' out_dir line 448 : : ' , out_dir)
    # try:
    #     os.makedirs(out_dir)
    # except Exception as e:
    #     print(' %s Dir exist ' %(out_dir))

    file_name_list = [options.did, 'Topic-' + str(options.K), 'alpha-' + str(options.alpha), 'eta1-' +  str(options.eta1),
                      'eta2-' +  str(options.eta2),   'iter_' + str(options.iteration)]
    suffix = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    out_dir = os.path.join( out_dir, options.did, options.setup, '_'.join(file_name_list), suffix)
    try:
        os.makedirs(out_dir)
    except:
        print('% dir exists !' %(out_dir))

    voca = vocabulary.Vocabulary(options.stopwords)
    docs = [voca.doc_to_ids(doc) for doc in corpus]
    if options.df > 0: docs = voca.cut_low_freq(docs, options.df)

    X = np.zeros((len(docs), len(voca.vocas)), dtype=np.int)


    for i,doc in enumerate(docs):
        for j, words in enumerate(doc):
            X[i][words] += 1

    for i in range(len(docs)):
        for j in range(len(voca.vocas)):
            if X[i][j] < 0:
                print(' Value less than zero :',i,j, X[i][j], voca.vocas[j])

    # Guided LDA with seed topics.

    # seed_topics = {}
    # for t_id, st in enumerate(seed_topic_list):
    #     for word in st:
    #         seed_topics[voca.vocas_id[word]] = t_id

    seed_topics_dir = os.path.join(SEED_DIR, options.did, options.setup)
    seed_topics_fname = '{}-{}.json'.format(options.did, options.setup)
    seed_topics_fname_total = os.path.join(seed_topics_dir, seed_topics_fname)
    seed_topics = load_seed_word(seed_topics_fname_total, voca.vocas_id, event_list)

    # saving to call graph

    model = guidedlda.GuidedLDA(n_topics= options.K, n_iter= options.iteration + 1 , alpha = options.alpha, eta = options.eta2, random_state= options.K, refresh=20)
    #model = guidedlda.GuidedLDA(n_topics= options.K, n_iter= options.iteration + 1 , alpha = options.alpha, eta = options.eta2, random_state= options.K, refresh=20)
    model.fit(X, seed_topics=seed_topics, seed_confidence=options.eta1) #
    #model.fit(X)


    # writing to file doc-topic
    doc_topic = model.transform(X)
    fout_doc_topic = '%s/doc_topic_dist.txt' %(out_dir)
    fdoc=open(fout_doc_topic,'w')
    st_doc_topic = ''
    for i,item in enumerate(docs):
        st_doc_topic += "{} : Topic_{}\n".format(doc_ids[i], doc_topic[i].argmax())
    fdoc.write(st_doc_topic)
    fdoc.close()

    # Writing to file doc_topic_dist_score.csv
    topic_list = []
    for i in range(options.K):
        topic_list.append('Topic_%03d'%(i))
    print(doc_topic.shape, len(topic_list), len(doc_ids))
    df = pd.DataFrame(data=doc_topic, columns=topic_list, index=doc_ids)
    #print(df.head)
    fout_doc_topic_score = os.path.join(out_dir, 'doc_topic_dist_score.csv')
    df.to_csv(fout_doc_topic_score)


    # Writing to file topic-word
    n_top_words = 20
    topic_word = model.topic_word_
    fout_topic_word = '%s/topic_word_dist.txt' %(out_dir)
    ftopic=open(fout_topic_word,'w')
    st_topic_word = ''
    for i, topic_dist in enumerate(topic_word):
        word_list = np.array(voca.vocas)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        score_list = np.argsort(topic_dist)[:-(n_top_words+1):-1]
        st_topic_word += '\n\n\nTopic : {}\n-------------------\n'.format(i)
        st =''
        for j, word in enumerate(word_list):
            st += '{}:{}\n'.format(word, topic_dist[score_list[j]])
        st_topic_word += st

    #print(docs)
    ftopic.write(st_topic_word)
    ftopic.close()

    # for i,doc in enumerate(docs) :
    #     print(" doc_ids: {} , {} , top topic: {}".format(i, doc_ids[i], doc_topic[i].argmax()))
    
if __name__ == "__main__":
    main()
