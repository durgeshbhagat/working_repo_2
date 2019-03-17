#!/use/bin/python -tt

"""
 JGD

 This program calculate Information gain of each term for a given Class

 IC(t) = H(C) - H(C|t)

 IG( c_i,t) = H(c_i) - H(t|c_i)

 ... Fill it later with detail description of formulae

"""


import pickle
import os
import sys
from datetime import datetime
import time
import json


from math import log

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_selection import mutual_info_classif

IP_DIR = 'ip'
base_out_dir = 'seed_word'

TMP_OUT_DIR = 'TMP_RESULTS_IG_Scikit'
setup = 'IG'
base_dir = ['bomb_blast_datasets', 'Reuter-21578-R-8', '20-Newsgroup']
fname = ['restoredDate_filtered_event_new_v.2_0_900.pkl', 'Reuter-21578_r-8-train_no_stop.pkl', '20-Newsgroup_train_stemmed.pkl']# ['filtered_event_new2.pkl']
start_index_dir = 0
start_index_file = 0

stop_word_list = {  'Dataset-1': [],
                    'Dataset-2': ['and' , 'for' , 'that', 'reuter', 'this', 'mln', 'not', 'last', 'will'] , # for Reuter
                    'Dataset-3':['and', 'for', 'that', 'this', 'will', 'can', 'edu', 'not', 'you', 'don', 'article', 'writes', 'your'] # FOR 20-News Group
                 }


check_word_list = ['train' , 'car' , 'killed']
def read_pickle_file(index_dir, index_file):
    fname_total = '{}/{:s}/{:s}'.format(IP_DIR,base_dir[index_dir], fname[index_file])
    fin = open(fname_total, 'r')
    story_dic = pickle.load(fin)
    fin.close()
    return story_dic


def log_modified(x, base = 2):
    if x == 0.0 or x == 0:
        return 0.0
    else:
        return log(x, base)

def calculate_IG(story_dic, dataset, topk):
    """

    :param story_dic:
    :param dataset:
    :param topk:
    :return:
    """
    """ 
    term_count :                                          |
        {
            tc:                                         |
                  {  't1':  ,                             |
                    't2':  ,                              |
                    't3':  ,
                    .
                    .
                    .
                    'tv':
                   } 
            total_count : 
    
         }
    
     
    class_term_count:
    
    {
        c1: 
            { 'tc' : 
                    { 't1':
                              't2' :
                              
                              
                    }
               total_count :
            }
            
            
        c2:
        
        .
        .
        .
        ,
        
        total_classs_count : 
    } 
    """
    t1 = time.time()

    term_count = {  'tc' : {} , 'total_count' : 0}
    class_term_count = { 'total_class_count' : 0}

    event_list = []

    voca_list = []
    doc_list = []
    class_list = []

    indptr = [0]
    indices = []
    data = []
    vocabulary = {} # term_id to term mapping

    for story in story_dic:
        if dataset == 'Dataset-1':
            class_label = '_'.join(story.split('_')[:2])
        elif dataset=='Dataset-2' or dataset =='Dataset-3':
            class_label = story.split('_')[-2]
        else:
            print('Rule to extarct event name is not known! Esiting the program !!')
            return

        if dataset == 'Dataset-1' :
            word_list = story_dic[story]['NER']['TITLE_CONTENT']['PER'] + story_dic[story]['NER']['TITLE_CONTENT']['LOC'] \
                        + story_dic[story]['NER']['TITLE_CONTENT']['ORG'] + story_dic[story]['NER']['TITLE_CONTENT']['ONS']

        else:
            word_list =  story_dic[story]['content']

        doc_list.append(story)
        class_list.append(class_label)

        for word in word_list:
            index = vocabulary.setdefault(word, len(vocabulary))
            indices.append(index)
            data.append(1)
        indptr.append(len(indices))

    doc_term_matrix = csr_matrix((data, indices, indptr), dtype=int)

    mutual_info =  mutual_info_classif(doc_term_matrix , class_list , discrete_features=True),

    """

    result_dir  = os.path.join(TMP_OUT_DIR,  'IG_results'  ) # dataset + '_all_ig')
    try:
        os.makedirs(result_dir)
    except:
        pass
    fname_total = os.path.join(result_dir, dataset + 'ig.json')
    fout = open(fname_total, 'w')
    json.dump(ig_dic, fout, indent=4, sort_keys= True)
    fout.close()
    """

    t2 = time.time()

    print(' Total time taken : %f ' %(t2-t1))


def entropy(vector, name ='default'):
    entropy_sum = 0
    for item in vector:
        if item == 0.0 :
                print('Zero value encountered , name :{0} , item ; {1}'.format(name, item))
                continue
        entropy_sum += item * log(item,2)
    return(entropy_sum)


def main():
    t_start = time.time()
    dataset_list = [ 'Dataset-1','Dataset-2', 'Dataset-3']
    score_list = [ 0.2, 0.2, 0.2]
    for i, dataset in enumerate(dataset_list[:1],0):
        for score in range(1,2):
            story_dic = read_pickle_file(index_dir = start_index_dir + i , index_file = start_index_file + i )
            calculate_IG(story_dic, dataset= dataset, topk=100)

    t_end = time.time()
    print('Total time taken : %f' %(t_end-t_start))
if __name__ == '__main__':
    main()
