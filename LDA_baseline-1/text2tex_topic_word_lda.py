import os
import sys


topic_sep = '\n'*3
line_sep = '\n'
word_Sep = ': '
k = 20
index = 2

dataset_list= [ 'Dataset-1', 'Dataset-2', 'Dataset-3']
file_list = [  'results/Dataset-1/Topic_53_alpha_0.100000_eta_0.200000_iter_100/2017-11-14_10:24:34/topic_word_dist.txt',  'results/Dataset-2/Topic_8_alpha_0.100000_eta_0.300000_iter_100/2017-11-14_11:22:53/topic_word_dist.txt', 'results/Dataset-3/Topic_20_alpha_0.100000_eta_0.200000_iter_100/2017-11-14_11:59:57/topic_word_dist.txt' ]

model = 'LDA'
setup = ''

fname =  file_list[index] #sys.argv[1]
dataset = dataset_list[index]

f = open(fname, 'r')
s = f.read()
topic_list = s.split(topic_sep)

topic_word = {}
for i, topic in enumerate(topic_list[:8]):
    line_list = topic.strip().split(line_sep)
    topic_word[i] =  []
    for j, line in enumerate(line_list[1:k+1]):
        word = line.strip().split(word_Sep)[0]
        topic_word[i].append(word)
        
        
print(topic_word)

topic_list = topic_word.keys()
topic_list.sort()
print(topic_list)

s = ''
for j in range(k):

    for i,topic in enumerate(topic_list):
        s += ' & '  + topic_word[i][j]  
    s += ' \\\\ \\hline' + '\n'

out_dir = 'topic_word_tex_dir'    
try :
    os.mkdir(out_dir)
except  Exception as e:
    print (e)
    
    
fout_total = '%s/%s_%s_topic_word.tex' %(out_dir, dataset, model)
fout = open(fout_total, 'w')
fout.write(s)
fout.close()

 
