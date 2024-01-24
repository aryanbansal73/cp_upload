from collections import defaultdict, deque, namedtuple
from typing import Any, Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Tuple
import requests
import time
import json
from json.decoder import JSONDecodeError
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

API_BASE_URL = 'https://codeforces.com/api/'
CONTEST_BASE_URL = 'https://codeforces.com/contest/'
CONTESTS_BASE_URL = 'https://codeforces.com/contests/'
GYM_BASE_URL = 'https://codeforces.com/gym/'
PROFILE_BASE_URL = 'https://codeforces.com/profile/'
ACMSGURU_BASE_URL = 'https://codeforces.com/problemsets/acmsguru/'


class Rank(NamedTuple):
    """Codeforces rank."""
    low: Optional[int]
    high: Optional[int]
    title: str
    title_abbr: Optional[str]
    color_graph: Optional[str]
    color_embed: Optional[int]

RATED_RANKS = (
    Rank(-10 ** 9, 1200, 'Newbie', 'N', '#CCCCCC', 0x808080),
    Rank(1200, 1400, 'Pupil', 'P', '#77FF77', 0x008000),
    Rank(1400, 1600, 'Specialist', 'S', '#77DDBB', 0x03a89e),
    Rank(1600, 1900, 'Expert', 'E', '#AAAAFF', 0x0000ff),
    Rank(1900, 2100, 'Candidate Master', 'CM', '#FF88FF', 0xaa00aa),
    Rank(2100, 2300, 'Master', 'M', '#FFCC88', 0xff8c00),
    Rank(2300, 2400, 'International Master', 'IM', '#FFBB55', 0xf57500),
    Rank(2400, 2600, 'Grandmaster', 'GM', '#FF7777', 0xff3030),
    Rank(2600, 3000, 'International Grandmaster', 'IGM', '#FF3333', 0xff0000),
    Rank(3000, 10 ** 9, 'Legendary Grandmaster', 'LGM', '#AA0000', 0xcc0000)
)
UNRATED_RANK = Rank(None, None, 'Unrated', None, None, None)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}
def get_submission_info(username):
    submissions = json.loads(requests.get(f'https://codeforces.com/api/user.status?handle={username}').text)['result']
    for submission in submissions:
        if submission['verdict'] == 'OK':
            try:
                if len(str(submission["problem"]["contestId"])) <= 4 and len(submission["author"]["members"]) == 1:
                    yield {
                        'language': submission['programmingLanguage'],
                        'problem_code': f'{submission["problem"]["contestId"]}/{submission["problem"]["index"]}',
                        'solution_id': submission['id'],
                        'problem_name': submission['problem']['name'] if 'name' in submission['problem'] else '',
                        'problem_link': f'https://codeforces.com/contest/{submission["problem"]["contestId"]}/problem/{submission["problem"]["index"]}',
                        'link': f'https://codeforces.com/contest/{submission["contestId"]}/submission/{submission["id"]}?f0a28=2',
                    }
            except KeyError:
                pass



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
def  data_format_to_needed_form():
    rated_problems =  get_rated_problems()
    tags = get_tags(rated_problems)
    problem_by_id_ = problem_by_id(rated_problems , tags)
    return problem_by_id_




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

# def upload_to_mongo(problem_by_id_):
#     # print("start")

#     # Extract data for insert_many
#     documents_to_insert = [{'_id': key, **value[0]} for key, value in problem_by_id_.items()]

#     # Check if the documents with the same _id already exist
#     existing_documents = database.find({'_id': {'$in': [doc['_id'] for doc in documents_to_insert]}})

#     existing_ids = set(doc['_id'] for doc in existing_documents)

#     # Filter out documents with existing _ids
#     documents_to_insert = [doc for doc in documents_to_insert if doc['_id'] not in existing_ids]

#     # If there are documents to insert, use insert_many
#     if documents_to_insert:
#         database.insert_many(documents_to_insert)
#         print(f"{len(documents_to_insert)} documents inserted successfully.")
#     else:
#         print("No new documents to insert.")

#     end_time = time.time()
#     elapsed_time = end_time - start_time

    # print(f"Time elapsed: {elapsed_time} seconds")
# upload_to_mongo(data_format_to_needed_form())
# data=  database.find()
# print(type(data))