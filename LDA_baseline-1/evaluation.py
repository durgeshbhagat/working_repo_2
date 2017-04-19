#!/usr/bin/python -tt

'''
This program finds precision, recall , accuracy , jacard coef ,Rand Index, purity for the LDA results 
'''
import os
import sys
import pickle
from itertools import combinations
import itertools
from datetime import datetime



def evaluation_matrix(fname,parameter):
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
    doc_list.sort()
    tp=tn=fp=fn =0

    doc_pair_list = list(combinations(doc_list,2))
    doc_pair_list.sort()
    #print 'len of list ', len(doc_pair_list)
    cur_label = ''
    for doc1,doc2 in doc_pair_list:
        ev1 = '_'.join( doc1.strip().split('_')[:2])
        ev2 = '_'.join( doc2.strip().split('_')[:2])
        #print ev1, ev2
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
        model_op[(doc1,doc2)] = { 'op' : doc2event[doc1] + ' : ' + doc2event[doc2]  , 'label' : cur_label }
        
    precision = ( tp * 1.0 ) / (tp + fp)

    recall =  ( tp * 1.0 ) / (tp + fn)
    
    f_measure = 2*( precision * recall) / (precision + recall)
    rand_index  =  ( 1.0 * tp + tn) / (tp + tn + fp + fn ) 

    jc = ( 1.0 * tp ) / ( tp + fp + fn)
    
    
    #temp_item = '%0.2f_%0.2f_%0.2f' %(cur_l_per)

    
    print ' {:14s}| {:8d}| {:8d}| {:8d}| {:8d}| {:5.7f}| {:4.7f} | {:4.7f} | {:4.7f} | {:4.7f}|'.format(parameter,tp,fp,tn,fn,precision,recall,f_measure,rand_index,jc)
    #print ' tp =%d , fp=%d, tn =%d, fn =%d , precision =%f , recall =%f, rand_index = %f, jc=%f' %(tp,fp,tn,fn,precision,recall,rand_index,jc)
    #print '{:10s} {:3d}  {:7.2f}'.format('xxx', 123, 98)

    #print 'Length of Doc : %d , len of TOpic : %d ' %(len(doc_list), len(event_list))


    d ={}
    d['tp'] = tp
    d['tn'] =tn
    d['fn'] = fn
    d['fp'] = fp

    d['precision'] =precision
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
    return d, model_op


def main():

    # Form file list
    #base_dir = sys.argv[1]
    base_dir = '%s/all_words' %('results')
    dir_list = os.listdir(base_dir)
    dir_list.sort()
    dir_total = []
    parameter_list=[]
  
    for i,cur_dir in enumerate(dir_list):
        temp_list = cur_dir.strip().split('_')
        st= '%0.1f_%0.1f' %(float(temp_list[3]),float(temp_list[5]))
        print 'st=%s ' %(st)
        parameter_list.append(st)
        

    for i,cur_dir in enumerate(dir_list):
        cur_dir_total ='%s/%s' %(base_dir,cur_dir)
        cur_dir_list = os.listdir(cur_dir_total)
        cur_dir_list.sort()
        t = '%s/%s' %(cur_dir_total,cur_dir_list[0])
        dir_total.append(t)

    p_list=[]    
    for i,cur_dir in enumerate(dir_total):
        print 'Processing %d , cur_dir =%s' %(i,cur_dir)
        p_list.append([])
        fname_log_dir ='%s/%s' %(cur_dir,'log_file.txt')
       
       
   
   
   
    print ' {:13s} | {:7s} | {:7s} | {:7s} | {:7s} | {:9s}| {:9s} | {:9s} | {:9s}| {:10s} |'.format('Alpha_Eta', 'TP','FP','TN','FN','Precision','Recall','F_measure', 'Rand_index','Jaccard_Coefficient')
    fname_evaluation  = 'LDA_base_line_evaluation.txt'
    f=open(fname_evaluation,'w')
    st = 'Alpha_Eta \t Precision \t Recall \t F-measure \t    JC    \t Rand index\n'
    f.write(st)
    for i,cur_dir in enumerate(dir_total):
        #print item
        cur_fname ='%s/%s' %(cur_dir,'doc_topic_dist.txt')
        lda_ev , model_op_lda = evaluation_matrix(cur_fname,parameter_list[i])
        st = '%s \t %0.7f \t %0.7f \t %0.7f \t %0.7f \t %0.7f\n' %(parameter_list[i],lda_ev['precision'] , lda_ev['recall'] , lda_ev['f_measure'], lda_ev['jc'] , lda_ev['rand_index'])
        f.write(st)
        # cur_fname = 'Topic_53_alpha_0.100000_eta1_0.200000_eta2_0.400000_per_%0.2f_loc_%0.2f_org_%0.2f_iter_100' %(item)
        '''
        cur_dir = '%s/%s' %(result_dir,cur_fname)
        inner_dir_list= os.listdir(cur_dir)
        inner_dir_list.sort()
        print ' inner dir list :' ,inner_dir_list
        fname_total = '%s/%s/%s' %(cur_dir,inner_dir_list[-1],'doc_topic_dist.txt')
        fname_list.append(fname_total)
        '''
    f.close()
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
    
