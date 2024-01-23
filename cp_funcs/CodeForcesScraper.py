import requests
import json
from json.decoder import JSONDecodeError
import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from codeforces_api import *
logging.getLogger('WDM').setLevel(logging.NOTSET)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

# def get_submission_info(username):
#     submissions = json.loads(requests.get(f'https://codeforces.com/api/user.status?handle={username}').text)['result']
#     for submission in submissions:
#         if submission['verdict'] == 'OK':
#             try:
#                 if len(str(submission["problem"]["contestId"])) <= 4 and len(submission["author"]["members"]) == 1:
#                     yield {
#                         'language': submission['programmingLanguage'],
#                         'problem_code': f'{submission["problem"]["contestId"]}{submission["problem"]["index"]}',
#                         'solution_id': submission['id'],
#                         'problem_name': submission['problem']['name'] if 'name' in submission['problem'] else '',
#                         'problem_link': f'https://codeforces.com/contest/{submission["problem"]["contestId"]}/problem/{submission["problem"]["index"]}',
#                         'link': f'https://codeforces.com/contest/{submission["contestId"]}/submission/{submission["id"]}?f0a28=2',
#                     }
#             except KeyError:
#                 pass

def get_code(driver):
    lines = driver.find_elements(By.CSS_SELECTOR, '#program-source-text > ol > li')
    return '\n'.join(line.text for line in lines)

def get_solutions(username, all_info=None):
    try:
        if all_info is None:
            all_info = list(get_submission_info(username))
    except JSONDecodeError:
        logging.error("CodeForces API is currently unavailable. Please try again later.")
        return

    sub_id_info = {info['link']: info for info in all_info}

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(options=options)

    try:
        for link, info in sub_id_info.items():
            driver.get(link)
            
            # Use WebDriverWait to wait for the code element to be present
            code_element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#program-source-text > ol > li'))
            )
            code = get_code(driver)
            info['solution'] = code
            yield info

    except Exception as e:
        logging.error(f"Error: {str(e)}")

    finally:
        # Quit the WebDriver in a finally block to ensure it is closed even if an exception occurs
        driver.quit()


