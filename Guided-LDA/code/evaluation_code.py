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
#from memory_profiler import profile

#base_dir = '%s/all_words' %('results')
#base_dir = '%s/Reuters-21578/R-8-train-train_no-stop' %('results')
base_dir = '%s/Reuters-21578/R-8-train-train_withStopwords' %('results')

result_dir = '../results'

def evaluation_matrix(fname, parameter, dataset='Dataset-1'):
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
    t2= time.time()
    #print 'time taken in reading the file :%f' %(t2-t1)
    #doc_list.sort()
    t3=time.time()
    #print 'Time taken in sorting : %f' %(t3-t2)
    tp=tn=fp=fn =0

    doc_pair_list = combinations(doc_list,2)
    #doc_pair_list.sort()
    #print('len of list ', len(doc_pair_list)) #, doc_pair_list)
    cur_label = ''
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



    #temp_item = '%0.2f_%0.2f_%0.2f' %(cur_l_per)

    #print ' \t\t Line 73'
    #print('{:s} \t {:0.7f} \t {:0.7f} \t {:0.7f} \t {:0.7f} \t {:0.7f}'.format(parameter,precision, recall, f_measure, rand_index, jc))
    #print ' {:14s}| {:8d}| {:8d}| {:8d}| {:8d}| {:5.7f}| {:4.7f} | {:4.7f} | {:4.7f} | {:4.7f}|'.format(parameter,tp,fp,tn,fn,precision,recall,f_measure,rand_index,jc)
    #print ' tp =%d , fp=%d, tn =%d, fn =%d , precision =%f , recall =%f, rand_index = %f, jc=%f' %(tp,fp,tn,fn,precision,recall,rand_index,jc)
    #print '{:10s} {:3d}  {:7.2f}'.format('xxx', 123, 98)

    #print 'Length of Doc : %d , len of TOpic : %d ' %(len(doc_list), len(event_list))


    d ={}
    d['tp'] = tp
    d['tn'] =tn
    d['fn'] = fn
    d['fp'] = fp

    d['precision'] = precision
    d['recall'] = recall
    d['jc'] = jc
    d['rand_index'] = rand_index
    d['f_measure'] = f_measure
    '''fname = sys.argv[1] + '_result.pkl'
    f=open(fname,'w')
    pickle.dump(d,f)
    f.lcose()


    fname = sys.argv[1] + '_result.json'
    f=open(fname,'w')
    json.dump(d,f,indent=4)
    f.lcose()
    '''
    return d # , model_op


def main():

    # Form file list
    #base_dir = sys.argv[1]
    dataset_list  = ['Dataset-1', 'Dataset-2', 'Dataset-3']
    setup_list = ['ner_keywords', 'tf-df-ief']
    for dataset in dataset_list[1:2]:
        for setup in setup_list[0:2]:
            cur_dir = os.path.join(result_dir, dataset, setup)
            dir_list = os.listdir(cur_dir)
            for dir in dir_list[:1]:
                if dir.endswith('_100') or dir.endswith('_120'):
                   total_dir = os.listdir( os.path.join(cur_dir, dir))
                   # alpha, eta_1, eta_2 ,
                   total_dir.sort()
                   print(total_dir)
                   fname_total = os.path.join(cur_dir, dir, total_dir[-1], 'doc_topic_dist.txt')
                   result = evaluation_matrix(fname = fname_total, parameter = [], dataset=dataset)
                   print(result)

                   result_json_fname = os.path.join(cur_dir, dir, total_dir[-1], 'evaluation_result.josn')
                   print( 'result_json : ' , result_json_fname)
                   fout = open(result_json_fname, 'w')
                   json.dump(result, fout, indent = 4)
                   fout.close()

                   result_pkl_fname = os.path.join(cur_dir, dir, total_dir[-1], 'evaluation_result.pkl')
                   fout = open(result_pkl_fname, 'wb')
                   pickle.dump(result, fout)
                   fout.close()
                   # Call Evaluation matrix function


    """
    dir_list = os.listdir(base_dir)
    dir_list.sort()
    dir_total = []
    parameter_list=[]
    print(dir_list)

    for i,cur_dir in enumerate(dir_list):
        temp_list = cur_dir.strip().split('_')
        st= '%0.1f-%0.1f' %(float(temp_list[3]),float(temp_list[5]))
        #st= 'alpha-%0.1f_eta-%0.1f' %(float(temp_list[3]),float(temp_list[5]))
        #print 'st=%s ' %(st)
        parameter_list.append(st)
        

    for i,cur_dir in enumerate(dir_list):
        cur_dir_total ='%s/%s' %(base_dir,cur_dir)
        cur_dir_list = os.listdir(cur_dir_total)
        cur_dir_list.sort()
        t = '%s/%s' %(cur_dir_total,cur_dir_list[0])
        dir_total.append(t)

    p_list=[]    
    for i,cur_dir in enumerate(dir_total):
        #print 'Processing %d , cur_dir =%s' %(i,cur_dir)
        p_list.append([])
        fname_log_dir ='%s/%s' %(cur_dir,'log_file.txt')
       
       
   
   
    print('dir_total:' , dir_total)
    
    print('\n Total no of Dir : %d ' %(len(dir_total)))
    print(' {:13s} | {:7s} | {:7s} | {:7s} | {:7s} | {:9s}| {:9s} | {:9s} | {:9s}| {:10s} |'.format('Alpha_Eta',
                                        'TP','FP','TN','FN','Precision','Recall','F_measure', 'Rand_index','Jaccard_Coefficient'))
    #print ' {:13s} | {:7s} | {:7s} | {:7s} | {:7s} | {:9s}| {:9s} | {:9s} | {:9s}| {:10s} |'.format('Alpha_Eta', 'TP','FP','TN','FN','Precision','Recall','F_measure', 'Rand_index','Jaccard_Coefficient')
    #fname_evaluation  = 'LDA_base_line_evaluation.txt'
    #f=open(fname_evaluation,'w')
    """
    #st = 'Alpha_Eta \t Precision \t Recall \t F-measure \t    JC    \t Rand index\n'
   # f.write(st)



    #start_dir = int(raw_input('Enter the ith directory to process: '))
    #end_dir = start_dir + 1

    # evaluation_dir = 'evaluation_temp'
    # try:
    #     os.mkdir(evaluation_dir)
    # except:
    #     print(' %s dir exists' %(evaluation_dir))
    #
    # for i,cur_dir in enumerate(dir_total[:]):
    #     #part = int(raw_input('Enter the part to be done : 0/1/2/3... :'))
    #     #start_index = part * 1000000
    #     #end_index = -1 #(part+1) *1000000
    #     #end_index = int(raw_input('Enter the end index: : '))
    #     cur_fname ='%s/%s' %(cur_dir,'doc_topic_dist.txt')
    #     lda_ev  = evaluation_matrix(cur_fname,parameter_list[i])
    #
    #     #fname = '%s/%s_%d_%d.pkl' %(evaluation_dir, parameter_list[start_dir])
    #     #f=open(fname,'w')
    #     #pickle.dump(lda_ev,f) #save lda_ev
    #     #f.close()
    #
    #
    #
    #
    #     st = '%s \t %0.7f \t %0.7f \t %0.7f \t %0.7f \t %0.7f\n' %(i,lda_ev['precision'], lda_ev['recall'],
    #                                                                lda_ev['f_measure'], lda_ev['jc'], lda_ev['rand_index'])
    #     #exit()
    #     #f.write(st)
    #     # cur_fname = 'Topic_53_alpha_0.100000_eta1_0.200000_eta2_0.400000_per_%0.2f_loc_%0.2f_org_%0.2f_iter_100' %(item)
    #
    #     cur_dir = '%s/%s' %(result_dir,cur_fname)
    #     inner_dir_list= os.listdir(cur_dir)
    #     inner_dir_list.sort()
    #     print ' inner dir list :' ,inner_dir_list
    #     fname_total = '%s/%s/%s' %(cur_dir,inner_dir_list[-1],'doc_topic_dist.txt')
    #     fname_list.append(fname_total)
    #
    #f.close()
    #Topic_53_alpha_0.500000_eta1_0.400000_eta2_0.200000_per_0.3_loc_0.2_org_0.1_iter_100

    #fname_lda =sys.argv[1]


    #fname_tot_lda = sys.argv[2]

    #for i,fname in enumerate(fname_list):
    #    lda_ev , model_op_lda = evaluation_matrix(fname,l_per[i])
        #print fname
        #print lda_ev
    #tot_ev , model_op_tot_lda = evaluation_matrix(fname_tot_lda)
    '''
    suffix = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    fname = 'tot_lda_ev_%s.csv' %(suffix)
    f=open(fname,'w')
    st = ' , LDA, TOT_LDA\n\n'
    f.write(st)
    
    ev_list =[ 'tp', 'tn' , 'fp', 'fn', 'precision' , 'recall', 'rand_index', 'jc']
  
    for i,item in enumerate(ev_list,1):
        if i <5:
            st = st = '%s, %d  \n' %(item, lda_ev[item])
            #st = st = '%s, %d, %d \n' %(item, lda_ev[item], tot_ev[item])
        else:
            st = '%s, %0.6f \n' %(item, lda_ev[item]) #, tot_ev[item])
            #st = '%s, %0.6f, %0.6f \n' %(item, lda_ev[item], tot_ev[item])
        f.write(st)
    f.close()
    '''


if __name__ == '__main__':
    main()

