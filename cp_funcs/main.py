# import CodeChefScraper
# import AtcoderScraper
from time import sleep
import logging
from github import Github
import CodeForcesScraper
from github.GithubException import UnknownObjectException
from UploadToGithub import upload_to_github
import inspect

# from multiprocessing import Process

EXTENSIONS = {
    'c++': 'cpp',
    'clang': 'cpp',
    'gcc': 'c',
    'py': 'py',
    'javascript': 'js',
    'java': 'java',
    'c#': 'cs',
    'go': 'go',
    'haskell': 'hs',
    'kotlin': 'kt',
    'delphi': 'dpr',
    'pascal': 'pas',
    'perl': 'pl',
    'php': 'php',
    'rust': 'rs',
    'scala': 'sc',
    'node': 'js',
}


def upload_solution(website, solution, repo):
    try:
        s = solution["language"].lower()

        extension = 'txt'
        for key, value in EXTENSIONS.items():
            if key in s:
                extension = value
                break

        if solution.get('problem_name', ''):
            path = f'{website}/{solution["language"]}/{solution["problem_code"]} | {solution["problem_name"]}/{solution["solution_id"]}.{extension}'
        else:
            path = f'{website}/{solution["language"]}/{solution["problem_code"]}/{solution["solution_id"]}.{extension}'

        problem_info = ''
        if solution.get('problem_link', ''):
            if not solution.get('problem_name', ''):
                problem_info = f"""
                # An Aryan Bansal solution

                Link: {solution['problem_link']}
                """

            else:
                problem_info = f"""
                # An Aryan Bansal solution

                Problem: {solution['problem_name']}
                Link: {solution['problem_link']}
                """
        if(solution['solution'] == ""):
            return False 
        # print(solution)
        upload_to_github(repo, path, solution['solution'], inspect.cleandoc(problem_info))
        return True

    except Exception as e:
        logging.error(f'{e} FOR {solution}')
        return False


def codeforces_uploader(codeforces_username, repo):
    failed_codeforces = []
    for solution in CodeForcesScraper.get_solutions(codeforces_username):
        if not upload_solution('CodeForces', solution, repo):
            #print("hi")
            failed_codeforces.append(solution)

    for _ in range(3):
        if failed_codeforces:
            sleep(4)

            new_failed_codeforces = []
            for solution in CodeForcesScraper.get_solutions(codeforces_username, failed_codeforces):
                if not upload_solution('CodeForces', solution, repo):
                    new_failed_codeforces.append(solution)

            failed_codeforces = new_failed_codeforces




# def codechef_uploader(codechef_username, repo):
#     for solution in CodeChefScraper.get_solutions(codechef_username):
#         upload_solution('CodeChef', solution, repo)


# def atcoder_uploader(atcoder_username, repo):
#     for solution in AtcoderScraper.get_solutions(atcoder_username):
        # upload_solution('Atcoder', solution, repo)


def main():
    codeforces_username = input('Enter codeforces username (Press enter if N/A): ')
    # codechef_username = input('Enter codechef username (Press enter if N/A): ')
    # atcoder_username = input('Enter atcoder username (Press enter if N/A): ')
    access_token = input('Enter github access token: ')

    repo_name = input('Enter repository name (Press enter to use "CP-Solutions"): ')
    if repo_name.isspace() or not repo_name:
        repo_name = 'CP-Solutions'

    g = Github(access_token)

    try:
        repo = g.get_user().get_repo(repo_name)

    except UnknownObjectException:
        repo = g.get_user().create_repo(repo_name, private=True)

    # if atcoder_username:
    #     atcoder_uploader(atcoder_username, repo)
    #     # atcoder_process = Process(target=atcoder_uploader, args=(atcoder_username, repo))
    #     # atcoder_process.start()

    # if codechef_username:
    #     codechef_uploader(codechef_username, repo)
        # codechef_process = Process(target=codechef_uploader, args=(codechef_username, repo))
        # codechef_process.start()

    if codeforces_username:
        codeforces_uploader(codeforces_username, repo)
        # codeforces_process = Process(target=codeforces_uploader, args=(codeforces_username, repo))
        # codeforces_process.start()
def module_func(codeforces_username ,access_token ,repo_name = None ,  added_already = []):
    if repo_name.isspace() or not repo_name:
        repo_name = 'CP-Solutions'

    g = Github(access_token)

    try:
        repo = g.get_user().get_repo(repo_name)

    except UnknownObjectException:
        repo = g.get_user().create_repo(repo_name, private=True)

    # if atcoder_username:
    #     atcoder_uploader(atcoder_username, repo)
    #     # atcoder_process = Process(target=atcoder_uploader, args=(atcoder_username, repo))
    #     # atcoder_process.start()

    # if codechef_username:
    #     codechef_uploader(codechef_username, repo)
    #     # codechef_process = Process(target=codechef_uploader, args=(codechef_username, repo))
    #     # codechef_process.start()

    if codeforces_username:
        codeforces_uploader(codeforces_username, repo)

if __name__ == '__main__':
    main()
