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


def  get_rated_problems():
  y = json.loads(requests.get(f'https://codeforces.com/api/problemset.problems').text)
  problems = (y['result']['problems'])
  val = 'rating'
  rated_problems = [d for d in problems if val in d]
  for i in rated_problems:
    i['link'] =  f'https://codeforces.com/problemset/problem/{i["contestId"]}/{i["index"]}'
    i['problem_id'] = f'{i["contestId"]}/{i["index"]}'
  return rated_problems
def get_tags(rated_problems):
  tags = []
  for i in rated_problems:
    tag_data = i['tags']
    for j in tag_data:
      if j not in  tags:
        tags.append(j)
  i = 1
  tag_dic ={}
  for v  in tags :
    tag_dic[v] = i
    i+=1;
  return tag_dic
def problem_by_id(rated_problems,tags):
  problems_rating_based = defaultdict(list)
  for i in rated_problems:
    rating = str(i['problem_id'])
    tag_data = i['tags']
    tag_val =[]
    for j  in tag_data:
      tag_val.append(tags[j])
    i['tags' ] = tag_val
    problems_rating_based[rating].append(i)
  return problems_rating_based
#creates a key value pair with problem id as key and tags as value
def create_qid_tid(problem_by_id):
  qid_tid= defaultdict(list)
  for i , val in problem_by_id.items():
    qid_tid[i] = val[0]['tags']
  return qid_tid

def get_submission_info_indv(username):
    # Sending a get request to cf api to get data and converting it to test and taking only result part
  user_prob = []

  submissions = json.loads(requests.get(f'https://codeforces.com/api/user.status?handle={username}').text)['result']
  for submission in submissions:
      if submission['verdict'] == 'OK':
          # try:
              if len(str(submission["problem"]["contestId"])) <= 4 and len(submission["author"]["members"]) == 1:
                v1 = (submission["problem"]["contestId"])
                v2 = submission["problem"]["index"]
                # prob_id  = f'{submission["problem"]["contestId"]}/{submission["problem"]["index"]}'
                prob_id = f'{v1}/{v2}'
                user_prob.append(prob_id)

          # except KeyError:
          #     pass

  return user_prob

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

