#!/use/bin/python -tt

"""

 THis program find term frequency- inverse event/ topic ferwncy for a term and event/topic

Saare paap isi jaanm me dho dena Bhagwan !! :) . JGD 
"""


import pickle
import os
import sys
from datetime import datetime


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

base_dir = ['bomb_blast_datasets', 'Reuters-21578-R-8/pkl', '20-Newsgroup/pkl']
fname = ['restoredDate_filtered_event_new.pkl', 'restoredDate_filtered_event_new_v.2.1.pkl', 'restoredDate_filtered_event_new_v.2_0_900.pkl', 'Reuter-21578_r-8-train_no_stop.pkl', '20-Newsgroup_train_stemmed.pkl']# ['filtered_event_new2.pkl']
start_index_dir = 0
start_index_file = 2

# stop_word_list = ['and' , 'for' , 'that', 'reuter', 'this', 'mln', 'not', 'last', 'will'] # for Reuter 
stop_word_list = ['and', 'for', 'that', 'this', 'will', 'can', 'edu', 'not', 'you', 'don', 'article', 'writes', 'your'] # FOR 20-News Group

def read_pickle_file(index_dir, index_file):
    fname_total = '{:s}/{:s}'.format(base_dir[index_dir], fname[index_file])
    fin = open(fname_total, 'r')
    story_dic = pickle.load(fin)
    fin.close()
    return story_dic

def calculate_tf_ief(story_dic, dataset,topk, weight ):
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
            event = '_'.join(story.split('_')[:-1])
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
            if word in stop_word_list :
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
    tf_ief = {}
    for event in event_to_term:
        tf_ief[event] = {}
        for word in event_to_term[event]['term']:
            tf =  (event_to_term[event]['term'][word]['count'] *1.0) / event_to_term[event]['N']  # Event wise term frequency
            df = (len(event_to_term[event]['term'][word]['df_list']) * 1.0 ) / event_to_term[event]['D'] # Event wise document frequncy
            ief =  (len(event_list) *1.0 ) / len(term_to_event[word]) # Inverse event frequency
            tf_ief[event][word] = tf * df * ief
    

    
    st = ''
    #weight = float(sys.argv[1])
    #k= 40
    #out_dir = 'bomb_blast_event_analysis/title_content/top-%d' %(topk)

    #out_dir = '20-Newgroup_datasets_analysis/tf-df-ief/top-%d' %(topk)

    out_dir = os.path.join( '..','Special_words_LDA', 'weightage_file', dataset, 'tf-df-icf', 'top-%d' %(topk) )
    print out_dir
    try :
        os.makedirs(out_dir)
    except:
        pass 
    
    
    intersection_set = set()

    #Writing tokp k term of each cluster with given score in the weighatage file
    for event in sorted(event_to_term):
        #print event
        tf_df_ief_term_list = tf_ief[event].keys()
        tf_df_ief_term_score_list = tf_ief[event].items()
        ##print temp_list
        tf_df_ief_term_list.sort(key = lambda item : tf_ief[event][item], reverse = True)
        tf_df_ief_term_score_list.sort(key = lambda item : item[-1], reverse = True)
        temp_set = set(tf_df_ief_term_list[:topk])
        if len(intersection_set)  == 0:
            intersection_set = temp_set
        else:
            intersection_set = intersection_set & temp_set
        #print event + ' :: \n\t ' +str( tf_df_ief_term_score_list[:k])
        for term in tf_df_ief_term_list[:topk]:
          st += '%s #,# %f\n' %(term, weight)
    
    #print intersection_set
    
    fout_name_total = '%s/term_ief_weight_%0.2f' %(out_dir, weight) #title_ief_top_%d_%0.2f
    fout = open(fout_name_total, 'w')
    fout.write(st)
    fout.close()
    
    event_wise_uniq_term = {}
    for term in term_to_event:
        
         if len(term_to_event[term]) ==1:
            event = term_to_event[term][0]
            if event in event_wise_uniq_term:
                event_wise_uniq_term[event].append(term)
            else:
                event_wise_uniq_term[event] = [term]
            #print term, term_to_event[term]
            
    '''
    for event in sorted(event_wise_uniq_term):
        print event, event_wise_uniq_term[event]

    '''
    '''
    out_dir = 'bomb_blast_event_analysis'
    try :
        os.makedirs(out_dir)
    except:
        pass
    #Saving Event wise title
    fname= '%s/%s' %(out_dir,'event_wise_title_ner_keywords.txt')
    f=open(fname,'w')
    st = ''
    for event in sorted(event_to_title):
        event_to_title[event].sort(key = lambda item: datetime.strptime(item.split('\t')[1].strip(), "%B %d, %Y") )
        st_event = '\n\t'.join(event_to_title[event])
        st += '\n{:s} \n\t{:s}\n\n\n'.format(event, st_event)
        print event
    f.write(st)
    f.close()
    '''
    
    
def calculate_tf_ief_old(story_dic):
    """
    c-urrently doing for unigram 
        
    """

    event_to_title = {}
    term_to_event = {}
    event_to_term = {}
    event_list = []
    for story in story_dic:
        event = '_'.join(story.split('_')[:2])
        if event not in event_to_term:
            event_to_term[event] =  {'term': { }, 'N': 0}
        if event not in event_list:
            event_list.append(event)
        if event not in event_to_title:
            print type(story_dic[story]['TIME_PUB'])
            event_to_title[event] =   ['{:s} \t {:s} \t {:s} \t {:s}'.format(story, story_dic[story]['TIME_PUB'], \
                                       story_dic[story]['TITLE'], story_dic[story]['LINK'].strip() )]
        else:
            event_to_title[event] += ['{:s} \t {:s} \t {:s} \t {:s}'.format(story, story_dic[story]['TIME_PUB'], \
                                         story_dic[story]['TITLE'], story_dic[story]['LINK'].strip() )]
        word_list = story_dic[story]['TITLE'].split()
        for j, word in enumerate(word_list):
            if len(word) >2:
                word_list[j] = str(word_list[j].strip(',z:'))
        for word in word_list:
            if word in event_to_term[event]['term']:
                event_to_term[event]['term'][word] += 1
                event_to_term[event]['N'] += 1
            else:
                event_to_term[event]['term'][word] = 1
                event_to_term[event]['N'] += 1

            if word not in term_to_event:
                term_to_event[word] = []
            if event not  in term_to_event[word]:
                term_to_event[word].append(event)
    tf_ief = {}
    for event in event_to_term:
        tf_ief[event] = {}
        for word in event_to_term[event]['term']:
            tf_ief[event][word] = ( event_to_term[event]['term'][word] *1.0 / event_to_term[event]['+N'] ) # *  ( len(event_list) *1.0 / len(term_to_event[event]) )
    for event in event_to_term:
        print event
        temp_list = tf_ief[event].items()
        temp_list.sort(key = lambda item : item[-1], reverse = True)
        print temp_list[:30]
    
    event_wise_uniq_term = {}
    for term in term_to_event:
        
         if len(term_to_event[term]) ==1:
            event = term_to_event[term][0]
            if event in event_wise_uniq_term:
                event_wise_uniq_term[event].append(term)
            else:
                event_wise_uniq_term[event] = [term]
            #print term, term_to_event[term]
    
    for event in sorted(event_wise_uniq_term):
        print event, event_wise_uniq_term[event]

    out_dir = 'bomb_blast_event_analysis'
    try :
        os.makedirs(out_dir)
    except:
        pass
    #Saving Event wise title
    fname= '%s/%s' %(out_dir,'event_wise_title.txt')
    f=open(fname,'w')
    st = ''
    for event in sorted(event_to_title):
        event_to_title[event].sort(key = lambda item: datetime.strptime(item.split('\t')[1].strip(), "%B %d, %Y") )
        st_event = '\n\t'.join(event_to_title[event])
        st += '\n{:s} \n\t{:s}\n\n\n'.format(event, st_event)
        print event
    f.write(st)
    f.close()

def main():
    dataset_list = [ 'Dataset-1','Dataset-2', 'Dataset-3']
    score_list = [ 0.2, 0.2, 0.2]
    for i, dataset in enumerate(dataset_list):
        for score in range(1,5):
            story_dic = read_pickle_file(index_dir = start_index_dir + i , index_file = start_index_file + i )
            calculate_tf_ief(story_dic, dataset= dataset, topk=40, weight= score * 0.1)


if __name__ == '__main__':
    main()
