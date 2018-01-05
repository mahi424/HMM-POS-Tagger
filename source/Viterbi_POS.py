from __future__ import division 
from operator import itemgetter
import math


with open("training.txt", "r") as input_file:
	data = input_file.read()
data_list = data.split()
count_data_list = len(data_list)

 
data_list_words = ['']
data_list_words*= count_data_list


data_list_tags = ['']
data_list_tags*= count_data_list

#seperating words and saving them and tags in the array
for i in range(count_data_list):
    temp_li = data_list[i].split("/")
    data_list_words[i] = temp_li[0]
    data_list_tags[i] = temp_li[1]



lang2tag_follow_tag_ = {}
lang2tag = {}
lang_word_tag_baseline = {}

#applying the assumptions
for i in range(count_data_list-1):
    index = data_list_tags[i]
    key_val = data_list_tags[i+1]
    lang2tag_follow_tag_[index]=lang2tag_follow_tag_.get(index,{})
    lang2tag_follow_tag_[index][key_val] = lang2tag_follow_tag_[index].get(key_val,0)
    lang2tag_follow_tag_[index][key_val]+=1

    index = data_list_words[i]
    key_val = data_list_tags[i]
    lang2tag[index]=lang2tag.get(index,{})
    lang2tag[index][key_val] = lang2tag[index].get(key_val,0)
    lang2tag[index][key_val]+=1


#handling the period sign

lang2tag_follow_tag_['.'] = lang2tag_follow_tag_.get('.',{})
lang2tag_follow_tag_['.'][data_list_tags[0]] = lang2tag_follow_tag_['.'].get(data_list_tags[0],0)
lang2tag_follow_tag_['.'][data_list_tags[0]]+=1


last_index = count_data_list-1

#Accounting for the last word-tag pair
index = data_list_words[last_index]
key_val = data_list_tags[last_index]
lang2tag[index]=lang2tag.get(index,{})
lang2tag[index][key_val] = lang2tag[index].get(key_val,0)
lang2tag[index][key_val]+=1

for key in lang2tag_follow_tag_:
    di = lang2tag_follow_tag_[key]
    s = sum(di.values())
    for innkey in di:
        di[innkey] /= s
    di = di.items()
    di = sorted(di,key=lambda x: x[0])
    lang2tag_follow_tag_[key] = di


for key in lang2tag:
    di = lang2tag[key]
    lang_word_tag_baseline[key] = max(di, key=di.get)
    s = sum(di.values())
    for innkey in di:
        di[innkey] /= s
    di = di.items()
    di = sorted(di,key=lambda x: x[0])
    lang2tag[key] = di



#accesing the test set 

with open("test.txt", "r") as input_file:
    test_str = input_file.read()

#extracting word tag pair from input 
test_str_list = test_str.split()
num_words_test = len(test_str_list)

test_li_words = ['']
test_li_words*= num_words_test

test_li_tags = ['']
test_li_tags*= num_words_test

output_li = ['']
output_li*= num_words_test

output_li_baseline = ['']
output_li_baseline*= num_words_test

num_errors = 0
num_errors_baseline = 0

#seperating words and tags
for i in range(num_words_test):
    temp_li = test_str_list[i].split("/")
    test_li_words[i] = temp_li[0]
    test_li_tags[i] = temp_li[1]

    output_li_baseline[i] = lang_word_tag_baseline.get(temp_li[0],'')
   #handeling the exception case of no tag or unknown tag
    if output_li_baseline[i]=='':
        output_li_baseline[i]='NNP'
        
        


    if output_li_baseline[i]!=test_li_tags[i]:
        num_errors_baseline+=1

    
    if i==0:    #Accounting for the 1st word in the test document for the Viterbi
        di_transition_probs = lang2tag_follow_tag_['.']
    else:
        di_transition_probs = lang2tag_follow_tag_[output_li[i-1]]
        
    di_emission_probs = lang2tag.get(test_li_words[i],'')

   
    if di_emission_probs=='':
        output_li[i]='NNP'
        
    else:
        max_prod_prob = 0
        counter_trans = 0
        counter_emis =0
        prod_prob = 0
        while counter_trans < len(di_transition_probs) and counter_emis < len(di_emission_probs):
            tag_tr = di_transition_probs[counter_trans][0]
            tag_em = di_emission_probs[counter_emis][0]
            if tag_tr < tag_em:
                counter_trans+=1
            elif tag_tr > tag_em:
                counter_emis+=1
            else:
                prod_prob = di_transition_probs[counter_trans][1] * di_emission_probs[counter_emis][1]
                if prod_prob > max_prod_prob:
                    max_prod_prob = prod_prob
                    output_li[i] = tag_tr
                    #print "i=",i," and output=",output_li[i]
                counter_trans+=1
                counter_emis+=1    
    
#handling the exception of no match with highest probable tag
    if output_li[i]=='':
        output_li[i] = max(di_emission_probs,key=itemgetter(1))[0]  
        
    if output_li[i]!=test_li_tags[i]:
        num_errors+=1

                    

print "Fraction of errors (Viterbi):",(num_errors/num_words_test)
print "Accuracy:",(str(1-(num_errors/num_words_test)) + "%")
print "Tags suggested by Viterbi Algorithm:", output_li
print "Correct tags:",test_li_tags







