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



IP_DIR = 'ip'
base_out_dir = 'seed_word'

TMP_OUT_DIR = 'TMP_RESULTS'
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
    print(fname_total)
    fin = open(fname_total, 'rb')
    print(type(fin))
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

    inverted_term2doc_list = {}
    inverted_class2doc_list = {}


    ig_dic = {}
    IG = {}
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
        if class_label not in inverted_class2doc_list:
            inverted_class2doc_list[class_label] = []
        if story not in inverted_class2doc_list[class_label]:
            inverted_class2doc_list[class_label].append(story)

        if class_label not in class_list:
            class_list.append(class_label)

        if class_label not in ig_dic:
            ig_dic[class_label] = {}
        for new_word in word_list:
            word = new_word.encode('ascii','ignore').decode('UTF-8')
            if word not in inverted_term2doc_list:
                inverted_term2doc_list[word] = []
            if story not in inverted_term2doc_list[word]:
                inverted_term2doc_list[word].append(story)

            if word not in voca_list:
                voca_list.append(word)

            if word not in ig_dic[class_label]:
                ig_dic[class_label][word] = 0.0

    for class_label in ig_dic:
        for word in ig_dic[class_label]:
            # Calculate ig_dic[class][word]

            # ig_tc
            n_t = len(inverted_term2doc_list[word])
            n_c = len(inverted_class2doc_list[class_label])
            n_tc = len(list(set(inverted_term2doc_list[word]) & set(inverted_class2doc_list[class_label])))
            p_tc = n_tc * 1.0 / len(doc_list)
            p_c = (len(inverted_class2doc_list[class_label]) * 1.0) / len(doc_list)
            p_t = (len(inverted_term2doc_list[word]) * 1.0) / len(doc_list)


            if  p_tc == 0.0:
                ig_tc = 0.0
            else:
                ig_tc = p_tc * (log_modified(p_tc, 2) - log_modified(p_c,2) - log_modified(p_t, 2))

            # ig_tbar_c
            p_tbar_c  = (len(inverted_class2doc_list[class_label]) - n_tc ) / ( len(doc_list) * 1.0)
            p_tbar = 1 - p_t

            if p_tbar_c == 0.0 :
                ig_tbar_c = 0.0
            else:
                ig_tbar_c = p_tbar_c * ( log_modified(p_tbar_c, 2) - log_modified(p_tbar, 2) - log_modified(p_c) )

            if word in check_word_list:
                print(' class_label= %s, term = %s, ig_tbar_c = %f, p_tbar_c = %f , p_c =%f, p_tbar= %f' %(class_label, word, ig_tbar_c, p_tbar_c, p_c, p_tbar))


            # ig_t_cbar
            p_t_cbar = (len(inverted_term2doc_list[word]) - n_tc ) / (len(doc_list) * 1.0)
            p_cbar = 1 - p_c

            if p_t_cbar == 0.0:
                ig_t_cbar = 0.0
            else:
                ig_t_cbar = p_t_cbar * ( log_modified(p_t_cbar, 2) - log_modified(p_t, 2) - log_modified(p_cbar, 2))

            if word in check_word_list:
                print(' class_label= %s, term = %s, ig_t_cbar=%f, p_t_cbar = %f , p_cbar =%f, p_t= %f' %(class_label, word, ig_t_cbar, p_t_cbar, p_cbar, p_t))


            # ig_tbar_cbar
            n_tbar_cbar = len(doc_list)  - len(inverted_term2doc_list[word]) - len(inverted_class2doc_list[class_label]) + n_tc
            p_tbar_cbar = n_tbar_cbar / ( len(doc_list) * 1.0)

            if p_tbar_cbar ==0.0:
                ig_tbar_cbar = 0.0
            else:
                ig_tbar_cbar = p_tbar_cbar * ( log_modified(p_tbar_cbar, 2) - log_modified(p_tbar, 2) - log_modified(p_cbar, 2))

            #if word in check_word_list:
            #    print(' class_label= %s, term = %s, ig_tbar_cbar = %f, p_tbar_cbar = %f , p_cbar =%f, p_tbar= %f' %(class_label, word, ig_tbar_cbar, p_tbar_c, p_cbar, p_tbar))



            ig_dic[class_label][word] = ig_tc + ig_tbar_c + ig_t_cbar + ig_tbar_cbar
            if ig_dic[class_label][word] < 0.0 :
                print('word=%s, ig = %f, ig_tc = %f, ig_tbar_c = %f ,ig_t_cbar=%f,  ig_tbar_cbar=%f  ' \
                      %(word, ig_dic[class_label][word], ig_tc, ig_tbar_c, ig_t_cbar, ig_tbar_cbar ))

    t2 = time.time()

    print(' Total time taken : %f ' %(t2-t1))

    return ig_dic


def write_to_file(ig_dic, dataset):

    result_dir  = os.path.join(TMP_OUT_DIR,  'IG_results'  ) # dataset + '_all_ig')
    try:
        os.makedirs(result_dir)
    except:
        pass
    fname_total = os.path.join(result_dir, dataset + '-IG.json')
    fout = open(fname_total, 'w')
    json.dump(ig_dic, fout, indent=4, sort_keys= True)
    fout.close()

def write_to_text_file(ig_dic, dataset, topk, eta1):
    excluded_word_list = [ '']
    st = ''
    topic_list = list(ig_dic.keys())
    topic_list.sort()
    for topic in topic_list:
        for word in ig_dic[topic]:
            if word in excluded_word_list:
                continue
            st += '%s #,# %f\n' %(word, eta1)
    result_dir = os.path.join(TMP_OUT_DIR, 'IG_results')  # dataset + '_all_ig')
    try:
        os.makedirs(result_dir)
    except:
        pass
    fname_total = os.path.join(result_dir, dataset + '-IG_weight_%0.2f'%(eta1) )
    fout = open(fname_total, 'w')
    fout.write(st)
    fout.close()



def entropy(vector, name ='default'):
    entropy_sum = 0
    for item in vector:
        if item == 0.0 :
                print('Zero value encountered , name :{0} , item ; {1}'.format(name, item))
                continue
        entropy_sum += item * log(item,2)
    return(entropy_sum)


def find_topk_IG_terms(ig_dic, k=40):
    top_ig = {}
    topic_list = list(ig_dic.keys())
    topic_list.sort()
    for topic in topic_list:
        #print (topic, len(ig_dic[topic]))
        term_list = list(ig_dic[topic].keys())
        term_list.sort(key=lambda item : ig_dic[topic][item] , reverse =True)
        top_ig[topic] = term_list[:k]

    uniq_top_ig = {}
    for topic in topic_list:
        set_item = set(top_ig[topic])
        set_all = union_item(top_ig, topic)
        uniq_top_ig[topic]= list(set_item - set_all)
    for topic in topic_list:
        print(topic, len(uniq_top_ig[topic]))
    return uniq_top_ig

def union_item(top_ig, except_key):
    l = []
    for item in top_ig:
        if item != except_key:
            l+= top_ig[item]
    #print(l)
    l = set(l)
    return(l)

def main():
    t_start = time.time()
    dataset_list = [ 'Dataset-1','Dataset-2', 'Dataset-3']
    score_list = [ 0.2, 0.2, 0.2]
    topk = 40
    eta1_list = [0.1, 0.2, 0.1]
    for i, dataset in enumerate(dataset_list[1:2],1):
        for score in range(1,2):
            story_dic = read_pickle_file(index_dir = start_index_dir + i , index_file = start_index_file + i )
            ig_dic = calculate_IG(story_dic, dataset= dataset, topk=100)
            top_ig = find_topk_IG_terms(ig_dic, k=40)
            #print(top_ig)
            write_to_file(top_ig, dataset)
            write_to_text_file(top_ig, dataset, topk, eta1_list[i])
    t_end = time.time()
    print('Total time taken : %f' %(t_end-t_start))
if __name__ == '__main__':
    main()
