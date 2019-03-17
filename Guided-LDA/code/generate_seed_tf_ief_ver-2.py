#!/use/bin/python -tt

"""

 THis program find term frequency- inverse event/ topic ferwncy for a term and event/topic

Saare paap isi jaanm me dho dena Bhagwan !! :) . JGD 
"""


import pickle
import os
import sys
from datetime import datetime
import time
import json


'''
 setup variation : 
        1) ALL CONTENT : 
                    a) unigram with stop word 
                    b) unigram without stop word
                    c) bigram with stop word
                    d) bigram without stop word
                    e) Tri-gram with stop word 
                    f) Trigram without stop word
        2) TITLE only
        
        3) NER only :
                a) PER
                b) LOC 
                c) ORG 
                d) Date and Time 

'''

IP_DIR = '../ip'
base_out_dir = '../seed_word'
setup = 'tf-df-ief'
base_dir = ['bomb_blast_datasets', 'Reuter-21578-R-8', '20-Newsgroup']
fname = ['restoredDate_filtered_event_new_v.2_0_900.pkl', 'Reuter-21578_r-8-train_no_stop.pkl', '20-Newsgroup_train_stemmed.pkl']# ['filtered_event_new2.pkl']
start_index_dir = 0
start_index_file = 0

stop_word_list = {  'Dataset-1': [],
                    'Dataset-2': ['and' , 'for' , 'that', 'reuter', 'this', 'mln', 'not', 'last', 'will'] , # for Reuter
                    'Dataset-3':['and', 'for', 'that', 'this', 'will', 'can', 'edu', 'not', 'you', 'don', 'article', 'writes', 'your'] # FOR 20-News Group
                 }
def read_pickle_file(index_dir, index_file):
    fname_total = '{}/{:s}/{:s}'.format(IP_DIR,base_dir[index_dir], fname[index_file])
    fin = open(fname_total, 'r')
    story_dic = pickle.load(fin)
    fin.close()
    return story_dic

def calculate_tf_df_ief(story_dic, dataset,topk):
    """
     Calculate tf-df-icf ( term-frequency-document-frequency-inverse-cluster-frequency for each cluster from a dataset
    :param story_dic: 
    :param dataset:
    :param topk : No of top term for each cluster
    : param weight : weight of each term
    :return: Save the  the tf-df-icf for each cluster in the respective file
    """
    
    event_to_title = {}
    term_to_event = {}
    """
        term_to_event = { 'term_1' : [ ev_1, ev_2 , ev_3 ]
                            .
                            .
                        }
    """
    event_to_term = {}  #
    """"    { event_1 : 
                        { 'term_1' : 
                                    { 'word_1' : { 'count': 5 , 'df_list' : [ doc_1, doc_5, ..., doc_20] }   }
                                        .
                                        .
                                    }
                              .
                              .
                        }
                    .
                    .
            }      
    """
    event_list = []
    count = 0
    for story in story_dic:
        if dataset == 'Dataset-1':
            event = '_'.join(story.split('_')[:2])
        elif dataset=='Dataset-2' or dataset =='Dataset-3':
            event = story.split('_')[-2]
        else:
            print('Rule to extarct event name is not known! Esiting the program !!')
            return
        if event not in event_to_term:
            event_to_term[event] =  {'term': {}, 'N': 0, 'D' : 0}
        if event not in event_list:
            event_list.append(event)
        if dataset == 'Dataset-1' :
            word_list = story_dic[story]['NER']['TITLE_CONTENT']['PER'] + story_dic[story]['NER']['TITLE_CONTENT']['LOC'] \
                        + story_dic[story]['NER']['TITLE_CONTENT']['ORG'] + story_dic[story]['NER']['TITLE_CONTENT']['ONS']

        else:
            word_list =  story_dic[story]['content']

        for word in word_list:
            if word in stop_word_list[dataset] :
                continue
            if word in event_to_term[event]['term']:
                event_to_term[event]['term'][word]['count'] += 1
                event_to_term[event]['N'] += 1
                if story not in event_to_term[event]['term'][word]['df_list'] :
                    event_to_term[event]['term'][word]['df_list'].append(story)
            else:
                event_to_term[event]['term'][word] = { 'count' : 1  , 'df_list' : [story] }
                event_to_term[event]['N'] += 1

            if word not in term_to_event:
                term_to_event[word] = []
            if event not  in term_to_event[word]:
                term_to_event[word].append(event)
        event_to_term[event]['D'] +=1

    tf_df_ief = {}
    for event in event_to_term:
        tf_df_ief[event] = {}
        for word in event_to_term[event]['term']:
            tf =  (event_to_term[event]['term'][word]['count'] *1.0) / event_to_term[event]['N']  # Event wise term frequency
            df = (len(event_to_term[event]['term'][word]['df_list']) * 1.0 ) / event_to_term[event]['D'] # Event wise document frequncy
            ief =  (len(event_list) *1.0 ) / len(term_to_event[word]) # Inverse event frequency
            tf_df_ief[event][word] = tf * df * ief
    
    # got the tf-df-ief score for each pair of term and event
    # sort the term for each event according to the score and consider the  top K disjoint term for each event

    seed_words = {}
    for event in event_to_term:
        word_list = tf_df_ief[event].items()
        word_list.sort(key =lambda item : item[1], reverse=True)
        for word,score in word_list[:topk]:
            if len(term_to_event[word]) ==1:
                if event not in seed_words:
                    seed_words[event] = []
                seed_words[event].append(word)

    # Saving seed_word to json file
    fout_dir = '%s/%s/%s' % (base_out_dir, dataset, setup)

    try:
        os.makedirs(fout_dir)
    except:
        pass
    fout_name_total = '%s/%s-%s.json' % (fout_dir, dataset, setup)
    print('Writing in file :', fout_name_total)
    fout_seed = open(fout_name_total, 'w')
    json.dump(seed_words, fout_seed, indent=4, )
    fout_seed.close()

    st = ''
    #weight = float(sys.argv[1])
    #k= 40
    #out_dir = 'bomb_blast_event_analysis/title_content/top-%d' %(topk)

    #out_dir = '20-Newgroup_datasets_analysis/tf-df-ief/top-%d' %(topk)

    # out_dir = os.path.join( '..','Special_words_LDA', 'weightage_file', dataset, 'tf-df-icf', 'top-%d' %(topk) )
    # print(out_dir)
    # try :
    #     os.makedirs(out_dir)
    # except:
    #     pass
    #
    #
    # intersection_set = set()
    #
    # # Writing tokp k term of each cluster with given score in the weighatage file
    # for event in sorted(event_to_term):
    #     #print event
    #     tf_df_ief_term_list = tf_ief[event].keys()
    #     tf_df_ief_term_score_list = tf_ief[event].items()
    #     ##print temp_list
    #     tf_df_ief_term_list.sort(key = lambda item : tf_ief[event][item], reverse = True)
    #     tf_df_ief_term_score_list.sort(key = lambda item : item[-1], reverse = True)
    #     temp_set = set(tf_df_ief_term_list[:topk])
    #     if len(intersection_set)  == 0:
    #         intersection_set = temp_set
    #     else:
    #         intersection_set = intersection_set & temp_set
    #     #print event + ' :: \n\t ' +str( tf_df_ief_term_score_list[:k])
    #     for term in tf_df_ief_term_list[:topk]:
    #       st += '%s #,# %f\n' %(term, weight)
    #
    # # print intersection_set
    #
    # fout_name_total = '%s/%s-tf-df-icf_weight_%0.2f' %(out_dir, dataset, weight) #title_ief_top_%d_%0.2f
    # fout = open(fout_name_total, 'w')
    # fout.write(st)
    # fout.close()
    #
    # event_wise_uniq_term = {}
    # for term in term_to_event:
    #
    #      if len(term_to_event[term]) ==1:
    #         event = term_to_event[term][0]
    #         if event in event_wise_uniq_term:
    #             event_wise_uniq_term[event].append(term)
    #         else:
    #             event_wise_uniq_term[event] = [term]
    #         #print term, term_to_event[term]
    #
    #
    # for event in sorted(event_wise_uniq_term):
    #     print event, event_wise_uniq_term[event][:40]

    

    


def main():
    t_start = time.time()
    dataset_list = [ 'Dataset-1','Dataset-2', 'Dataset-3']
    for i, dataset in enumerate(dataset_list,0):
            story_dic = read_pickle_file(index_dir = start_index_dir + i , index_file = start_index_file + i )
            calculate_tf_df_ief(story_dic, dataset= dataset, topk=100)

    t_end = time.time()
    print('Total time taken : %f' %(t_end-t_start))
if __name__ == '__main__':
    main()
