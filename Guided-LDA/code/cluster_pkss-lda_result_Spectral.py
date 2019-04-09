
import os
import sys
import pickle
import json
import time


import numpy as np
from sklearn.cluster import KMeans, AffinityPropagation, SpectralClustering
import pandas as pd

from evaluation_reuter_parllel import evaluation_matrix

def prepare_numpy_array_from_csv(fname, threshold):
    # read file
    fin =open(fname,'r')
    line_list = fin.read().strip().split('\n')

    fin.close()
    doc_list = []

    # read the size of matrix
    topic_id_list = line_list[0].strip().strip(',').split(' , ')
    #print topic_id_list
    m = len(topic_id_list)
    n = len(line_list)-1

    #print m,n
    doc_topic =[]
    count = 0
    for i,line in enumerate(line_list[1:]):

        doc_topic.append([])
        cur_line_list = line.strip().strip(',').split(',')
        #print cur_line_list
        doc_id = cur_line_list[0].strip()
        doc_list.append(doc_id)

        for j, score  in enumerate(cur_line_list[1:]):
            #print doc_id, j+1 , score
            score = float(score.strip())
            if score < threshold:
                doc_topic[i].append(0.000)
            else:
                count +=1
                doc_topic[i].append(score)
        sum_row = sum(doc_topic[i])
        #print sum_row
        if sum_row != 0:
            doc_topic[i] = [x / sum_row for x in doc_topic[i]]
    doc_topic_matrix = np.asarray(doc_topic, dtype = float)


    #print 'Array size : ' , doc_topic_matrix.shape
    #print 'count of no-zero :', count
    return doc_topic_matrix, doc_list, doc_topic




def Spectral_cluster(doc_topic_array, no_of_cluster, doc_list):
    #kmeans_op = KMeans(n_clusters= no_of_cluster, random_state=0).fit_predict(topic_word_array)
    spectral_op = SpectralClustering(n_clusters=no_of_cluster, eigen_solver=None, random_state=None, n_init=10, gamma=1.0, affinity='rbf', n_neighbors=10, eigen_tol=0.0, assign_labels='kmeans', degree=3, coef0=1, kernel_params=None, n_jobs=1).fit_predict(doc_topic_array)
    spectralOp_dic = {}
    cluster_freq = {}
    for i, cluster in enumerate(spectral_op):
        doc_id = doc_list[i]
        topic_id = 'Spectral-%02d' %(spectral_op[i])
        spectralOp_dic [doc_id] = topic_id

        if topic_id in cluster_freq:
            cluster_freq[topic_id] +=1
        else:
            cluster_freq[topic_id] =1
    #for cluster in sorted(cluster_freq):
    #    print cluster_freq[cluster]
    return spectralOp_dic

def save_SpectralClustering_result(Op_dic, fname):
    st = ''
    for cluster in Op_dic:
        #print(cluster, kmeanOp_dic[cluster])
        st += '%s : %s \n' %(cluster, Op_dic[cluster])
    fout = open(fname, 'w')
    fout.write(st)
    fout.close()


def main():
    t1 =time.time()
    no_of_cluster = [53,8,20]
    threshold_list = [ 0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
    setup_list = [ ['53_53_53', '53_150_53' , '53_20_53'] , ['8_8_8', '8_30_8' , '8_4_8'] , ['20_20_20', '20_60_20' , '20_8_20'] ]
    op_dir = 'op_dir_Doc_topic'

    dataset_list = ['Dataset-1' , 'Dataset-2' , 'Dataset-3']
    setup_list = ['ner_keywords', 'tf-df-ief', 'IG']
    cluster_count = [53, 8, 20]
    result_dir = os.path.join('..',  'results')

    for i, dataset in enumerate(dataset_list[0:1], 1):
        t_start = time.time()
        for setup in setup_list[0:1]:

            cur_dir = os.path.join(result_dir, dataset, setup)
            dir_list = os.listdir(cur_dir)
            #print( dir_list)
            dir_list_new  = [x for x in dir_list if ( x.endswith('_100') or x.endswith('_120')) ]
            dir_list_new.sort()
            print(dir_list_new)
            result_list = []
            for dir in dir_list_new[:]:
                #if dir.endswith('_100') or dir.endswith('_120'):
                total_dir = os.listdir( os.path.join(cur_dir, dir))
                # alpha, eta_1, eta_2 ,
                total_dir.sort()
                #print('line 130:', total_dir)
                parameter_list = dir.split('_')
                #print('parameter list', parameter_list)
                alpha = float(parameter_list[2].split('-')[1])
                eta_1 = float(parameter_list[4].split('-')[1])
                eta_2 = float(parameter_list[3].split('-')[1])
                iteration_count = int(parameter_list[-1])
                topic = parameter_list[1].split('-')[-1]
                for time_dir in total_dir:
                    fname_total = os.path.join(cur_dir, dir, time_dir, 'doc_topic_dist_score.csv')
                    # print(dataset, fname_total)
                    if not os.path.isfile(fname_total):
                        print('%s File does not exist', fname_total)
                        continue
                    else:
                        out_dir = os.path.join(cur_dir, dir, time_dir, 'KMean_LDA')
                        try:
                            os.mkdir(out_dir)
                        except:
                            pass
                    for threshold in threshold_list[1:]:
                        topic_word_array , doc_list, doc_topic_list = prepare_numpy_array_from_csv(fname_total, threshold)
                        Op_dic  = Spectral_cluster(topic_word_array, cluster_count[i] , doc_list)
                        fname_out = os.path.join(out_dir, 'KMean_doc_topic_%0.3f.txt'%(threshold))
                        save_SpectralClustering_result(Op_dic, fname_out)
                        result = evaluation_matrix(fname_out, dataset= dataset)
                        result['fname'] = os.path.join(cur_dir, dir, time_dir)
                        result['time'] = time_dir

                        result['alpha'] = alpha
                        result['eta_1'] = eta_1
                        result['eta_2'] = eta_2
                        result['iteration_count'] = iteration_count
                        result['topic'] = topic
                        result['threshold'] = threshold
                        print(result)
                        result_list.append(result)
                        print('clusterMethod=Spectral, dataset =%s, setup =%s, eta_1= %0.2f, eta_2=%0.2f, threshold=%0.3f ,' %(dataset, setup, eta_1, eta_2, threshold))
            out_dir = os.path.join(result_dir, 'result_analysis_comparision' , 'xlsx')
            try:
                os.makedirs(out_dir)
            except:
                pass

            df = pd.DataFrame(result_list, columns=['fname', 'time', 'topic', 'alpha', 'eta_1', 'eta_2', 'threshold', 'tp', 'tn', 'fn', 'fp', 'precision', 'recall',
                                                    'f_measure' , 'rand_index', 'jc','accuracy', 'iteration_count'])
            df.sort_values(['topic', 'alpha','eta_1', 'eta_2' , 'threshold'], inplace=True)
            fout_name_total = os.path.join(out_dir , 'Spectral-PKSS-LDA-' + dataset + '_' + setup + '.xlsx')
            df.to_excel( fout_name_total,  sheet_name=dataset, index=False, startrow=0, startcol=0)
                        #print(kmeanOp_dic)

    """
   
    for threshold in threshold_list[:1]:
        for i,dataset in enumerate(dataset_list[:]):
            fname = 
            for j,setup in enumerate(setup_list[i]):
            # 1. Read doc_topic_score.csv
            # 2. convert_tonumpy_array and get doc_list
            # 3. Apply K mean Clustering
            # 4. Save the doc -K-meantopic Relationship
                print 'Processing %s , setup %s,  threshold %f ' %(dataset, setup, threshold)
                dir_list = os.listdir(LDA_ip_dir[i][j])
                dir_list.sort()
                dir_total = '%s/%s' %(LDA_ip_dir[i][j], dir_list[-1])
                #print dir_total
                fname_total = '%s/%s' %(dir_total, 'doc_topic_dist_score.csv')
                print fname_total
                topic_word_array , doc_list, doc_topic_list = prepare_numpy_array_from_csv(fname_total, threshold)

                base_dir_out = '%s/%s/%s' %(op_dir,dataset,'LDA_doc_topic_threshold_normalized') #'LDA_doc_topic_threshold'
                try:
                    os.makedirs(base_dir_out)
                except:
                    pass
                fname_out_total = '%s/LDA_doctopicIP_setup-%sthreshold-%03f.csv' %(base_dir_out, setup, threshold)

                save_intermediate_matrix_with_threhold(doc_topic_list, doc_list, fname_total=fname_out_total)

                kmeanOp_dic  = k_mean_cluster(topic_word_array, no_of_cluster[i] , doc_list)
                #print kmeanOp_dic

                base_dir_out = '%s/%s/%s' %(op_dir,dataset,'LDA_doc_Kmeantopic_results_normalized') #'LDA_doc_Kmeantopic_results'
                try:
                    os.makedirs(base_dir_out)
                except:
                    pass
                fname_out_total = '%s/LDA_doc2Kmeantopic_setup-%sthreshold-%03f.pkl' %(base_dir_out, setup, threshold)
                fout = open(fname_out_total, 'w')
                pickle.dump(kmeanOp_dic,fout)
                fout.close()

    """

    t2=time.time()
    print('Total time taken : %f' %(t2-t1))
    pass


if __name__ == '__main__':
    main()
