import requests
import json
from json.decoder import JSONDecodeError
from collections import defaultdict
import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import time
from codeforces_api import *


def make_problem_weight_matrix( user_info ,  problem_by_id_,prob_data_in_matrix):
  rating = int (user_info['rating']/100)
  tags_length = 37
  user_weight_matrix = []
  for prob_id in problem_by_id_:
    dic  = problem_by_id_[prob_id]
    if(len(dic)> 0):
      prob_data_in_matrix.append(prob_id)

      # print((dic))
      rating_prob = dic[0]['rating']
      w_prob = rating_prob/100
      # print(w_prob)
      tag_dat = dic[0]['tags']
      row = [0]*tags_length
      for j in tag_dat:
        row[j-1] = w_prob-rating+0.5
      user_weight_matrix.append(row)
  return user_weight_matrix

def make_user_prob_matrix(user_info , problem_by_id_ ,user_prob_data ):
  rating = (int(user_info['rating']/100))
  handle = user_info['handle']
  # user_prob_data = get_submission_info_indv(handle)
  weight = 100
  tags_length = 37
  user_weight_matrix = []
  for prob_id in user_prob_data:
    dic  = problem_by_id_[prob_id]
    if(len(dic)> 0):

      # print((dic))
      rating_prob = dic[0]['rating']
      w_prob = rating_prob/100
      # print(w_prob)
      tag_dat = dic[0]['tags']
      row = [0]*tags_length
      for j in tag_dat:
        row[j-1] = (w_prob-rating +0.5 )
      user_weight_matrix.append(row)
  return user_weight_matrix

def make_user_prob_vector(user_prob_matrix):
    user_problem_vector = [0] * len(user_prob_matrix[0])
    for weights in user_prob_matrix:
        for i, w in enumerate(weights):
            user_problem_vector[i] += w
    user_problem_vector = [w/len(user_prob_matrix) for w in user_problem_vector]
    return user_problem_vector
def dot(u, v):
  assert len(u) == len(v)
  sum = 0
  for i in range(len(u)):
    sum +=( u[i] * v[i] )*10
  return sum

def make_selection_of_probs(user_problem_vector , problem_weight_matrix,prob_data_in_matrix,user_prob_data,problem_by_id_):
  scores = [
      dot(problem_tags, user_problem_vector)
      for problem_tags in problem_weight_matrix
  ]
  selected = []
  rating_sele = []
  for index , id in enumerate(prob_data_in_matrix):
    # print(index)
    if(id not in user_prob_data):
      if ((scores[index]<10 and scores[index] >=0   )  or (scores[index]<-20)  or (scores[index]<=0  and scores[index]>=-5) ):
        rating = problem_by_id_[id][0]['rating']
        rating_sele.append(rating)
        pair= (rating,id)
        selected.append(pair)

  lis_of_viable_probs = defaultdict(list)
  for i in selected:
    lis_of_viable_probs[i[0]].append(i[1])
  return lis_of_viable_probs

def get_problems(rating , count,lis_of_viable_probs):
  mean  = rating+100
  percentage_count = [0.1 , 0.2 , 0.4 , .2 , .1]
  recommended_probs = defaultdict(list)
  for i  ,  per_count in  enumerate(percentage_count):
    rating_val  = mean + 100*(i-2)
    selec = random.sample(lis_of_viable_probs[rating_val]  , int(count*per_count))
    recommended_probs[rating_val].append(selec)
  return recommended_probs


def working_mod(user_info):
  handle = user_info['handle']
  rated_problems =  get_rated_problems()
  tags = get_tags(rated_problems)
  problem_by_id_ = problem_by_id(rated_problems , tags)
  qid = create_qid_tid((problem_by_id_))
  user_prob_data = get_submission_info_indv(handle)
  user_prob_matrix = make_user_prob_matrix(user_info, problem_by_id_  ,user_prob_data)
  prob_data_in_matrix =[]
  problem_weight_matrix = make_problem_weight_matrix(user_info ,problem_by_id_,prob_data_in_matrix)
  user_problem_vector = make_user_prob_vector(user_prob_matrix)
  lis_of_viable_probs = make_selection_of_probs(user_problem_vector,problem_weight_matrix,prob_data_in_matrix,user_prob_data,problem_by_id_)
  return lis_of_viable_probs

def final():
  user_info = {'rating': 1568, 'handle': "gabagopesh"}
  lis_of_viable_probs=working_mod(user_info)
  rating = rating =( int((user_info['rating']+50)/100))*100

  count = 15 
  r = get_problems(rating,count,lis_of_viable_probs)
  print(r)
  

if __name__ == '__main__':
    start_time = time.time()
    final()
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time} seconds")