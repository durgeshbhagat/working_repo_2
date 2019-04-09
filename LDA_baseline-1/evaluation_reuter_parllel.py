#!/usr/bin/python -tt

'''
This program finds precision, recall , accuracy , jacard coef ,Rand Index, purity for the LDA results 
'''
import os
import sys
import pickle
import json
from itertools import combinations
from datetime import datetime
import time

import pandas as pd
#from memory_profiler import profile


def evaluation_matrix(fname,  dataset='Dataset-1'):
    t1= time.time()
    f=open(fname,'r')
    line_list=f.readlines()
    doc2event={}
    doc_list =[]
    event_list=[]
    model_op = {}
    for i,line in enumerate(line_list):
        cur_line_list = line.strip().split(' : ')
        doc_id = cur_line_list[0]
        topic = cur_line_list[1]
        doc2event[doc_id] = topic
        doc_list.append(doc_id)
        #event_list.append(topic)
    #print 'Time taken in sorting : %f' %(t3-t2)
    tp=tn=fp=fn =0

    doc_pair_list = combinations(doc_list,2)

    t4=time.time()
    for doc1, doc2 in doc_pair_list:
        #print(doc1, doc2) #, ev1, ev2)
        if dataset == 'Dataset-1':
            ev1 =  '_'.join(doc1.strip().split('_')[:2])
            ev2 =  '_'.join(doc2.strip().split('_')[:2])
        elif dataset == 'Dataset-2':
            ev1 =  doc1.strip().split('_')[-2]
            ev2 =  doc2.strip().split('_')[-2]
        elif dataset == 'Dataset-3':
            ev1 = doc1.strip().split('_')[-2]
            ev2 = doc2.strip().split('_')[-2]
        else:
            pass


        #print(ev1, ev2)
        if ev1 not in event_list :
            event_list.append(ev1)
        if ev2 not in event_list :
            event_list.append(ev2)
        if doc2event[doc1] == doc2event[doc2] : #model label matched
            if ev1 == ev2 :# Original labele matched
                tp +=1
                cur_label = 'tp'
            else:
                fp +=1
                cur_label = 'fp'
        else: #Model label dont matched for pair of doc
            if ev1 == ev2 :
                fn +=1
                cur_label = 'fn'
            else:
                tn +=1
                cur_label = 'tn'
        #model_op[(doc1,doc2)] = { 'op' : doc2event[doc1] + ' : ' + doc2event[doc2]  , 'label' : cur_label }

    t5=time.time()
    print('time taken in looping :%f' %(t5-t4))
    #print 'tp : %d, fp : %d, fn : %d, tn : %d ' %(tp,fp,fn,tn)
    precision = ( tp * 1.0 ) / (tp + fp)

    recall =  ( tp * 1.0 ) / (tp + fn)

    f_measure = 2*( precision * recall) / (precision + recall)
    rand_index  =  ( 1.0 * tp + tn) / (tp + tn + fp + fn )

    jc = ( 1.0 * tp ) / ( tp + fp + fn)


    d ={}
    d['tp'] = tp
    d['tn'] =tn
    d['fn'] = fn
    d['fp'] = fp

    d['precision'] = round(precision, 4)
    d['recall'] = round(recall, 4)
    d['jc'] = round(jc, 4)
    d['rand_index'] = round(rand_index, 4)
    d['f_measure'] = round(f_measure, 4)
    d['accuracy'] = round(((tp+ tn) * 1.0) / (tp+ tn + fp + fn), 4)

    del doc_pair_list

    return d # , model_op


def main():


    # Form file list
    #base_dir = sys.argv[1]
    dataset_list  = ['Dataset-1', 'Dataset-2', 'Dataset-3']
    #setup_list = ['ner_keywords', 'tf-df-icf_top-40', 'IG_top-40']
    result_dir = 'results'
    for dataset in dataset_list[0:1]:
        t_start = time.time()
        ip_dir = os.path.join(result_dir, dataset)
        dir_list = os.listdir(ip_dir)
        #print( dir_list)
        dir_list_new  = [x for x in dir_list if (x.split('_')[-1] in ['100', '120']) ]
        print(dir_list_new)
        #continue
        #continue
        result_list = []
        for cur_dir in dir_list_new[:]:
            #if dir.endswith('_100') or dir.endswith('_120'):
            total_dir = os.listdir( os.path.join(ip_dir, cur_dir))
            # alpha, eta_1, eta_2 ,
            total_dir.sort()
            #print('line 130:', total_dir)
            parameter_list = cur_dir.split('_')
            print(parameter_list)
            alpha =  float(parameter_list[3])
            eta_1 = float(parameter_list[5])
            iteration_count = int(parameter_list[-1])
            topic = int(parameter_list[1])
            for time_dir in total_dir:
                fname_total = os.path.join(ip_dir, cur_dir, time_dir, 'doc_topic_dist.txt')
                print(dataset, fname_total)

                if not os.path.isfile(fname_total):
                    continue
                result = evaluation_matrix(fname = fname_total, dataset=dataset)
                print(result)

                result['fname'] = os.path.join(ip_dir, cur_dir, time_dir)
                result['time'] = time_dir

                result['alpha'] = alpha
                result['eta_1'] = eta_1
                result['iteration_count'] = iteration_count
                result['topic'] = topic

                result_json_fname = os.path.join(ip_dir, cur_dir, total_dir[-1], 'evaluation_result.josn')
                fout = open(result_json_fname, 'w')
                json.dump(result, fout, indent = 4)
                fout.close()
                result_list.append(result)

            #result_pkl_fname = os.path.join(cur_dir, dir, total_dir[-1], 'evaluation_result.pkl')
            #fout = open(result_pkl_fname, 'wb')
            #pickle.dump(result, fout)
            #fout.close()


            # Call Evaluation matrix function

            out_dir = os.path.join(result_dir, 'result_analysis_comparision' , 'xlsx')
            try:
                os.makedirs(out_dir)
            except:
                pass

            df = pd.DataFrame(result_list, columns=['fname', 'time', 'topic', 'alpha', 'eta_1', 'tp', 'tn', 'fn', 'fp', 'precision', 'recall',
                                                    'f_measure' , 'rand_index', 'jc','accuracy', 'iteration_count'])
            df.sort_values(['topic', 'alpha','eta_1'], inplace=True)
            fout_name_total = os.path.join(out_dir , 'LDA-' + dataset + '.xlsx')
            df.to_excel( fout_name_total,  sheet_name=dataset, index=False, startrow=0, startcol=0)

        t_end = time.time()
        print( ' Total time taken for %s : %f' %(dataset, (t_end-t_start)))


if __name__ == '__main__':
    main()      
    
