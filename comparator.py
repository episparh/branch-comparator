import urllib.request
import urllib.error
import json
import itertools

url_branches = 'https://api.github.com/repos/{owner}/{project}/branches'
url_commits = 'https://api.github.com/repos/{owner}/{project}/commits'
url_branch_commits = 'https://api.github.com/repos/{owner}/{project}/commits?sha={branch}'
project = []
all_branches = []


def get_response(url):
    return json.load(urllib.request.urlopen(url))


def get_branch_names(data):
    return list(map(lambda x: x['name'], data))


def get_branch_commits(branch_name):
    data = json.load(
        urllib.request.urlopen(url_branch_commits.format(owner=project[0], project=project[1], branch=branch_name)))
    return list(map(lambda x: x['commit'], data))


def get_branch_diff(branch_A, branch_B):
    return list(itertools.filterfalse(lambda x: x in branch_A, branch_B)) + list(
        itertools.filterfalse(lambda x: x in branch_B, branch_A))


def get_commits_sha(data):
    return list(map(lambda x: x['tree']['sha'], data))


def get_sha_dif(sha_A, sha_B):
    return list(list(set(sha_A) - set(sha_B)))


def get_input_for_branch_name(msg, branch_list):
    name = None
    while name is None:
        print(msg, branch_list)
        name = str(input(msg))
        if name not in branch_list:
            name = None
    branch_list.remove(name)
    return name


def get_input_for_project():
    global all_branches
    while len(all_branches) == 0:
        retval = [str(input('Repository owner. Example: pallets\n')),
                  str(input('Repository name. Example: flask\n'))]
        try:
            all_branches = get_branch_names(get_response(url_branches.format(owner=retval[0], project=retval[1])))
        except urllib.error.HTTPError:
            print("Non existing owner or project! Try again:")
    return retval


def get_diff_report(sha_diff_list, sum_commit):
    retval = []
    for commit in sum_commit:
        if commit['tree']['sha'] in sha_diff_list:
            retval.append([commit['tree']['sha'], commit['message']])
    return retval


if __name__ == '__main__':
    project = get_input_for_project()
    branch_A_name = get_input_for_branch_name('Select first branch from existing values:\n ', all_branches)
    branch_B_name = get_input_for_branch_name('Select second branch from existing values:\n ', all_branches)
    branch_A = get_branch_commits(branch_A_name)
    branch_B = get_branch_commits(branch_B_name)
    diff_sha = get_sha_dif(get_commits_sha(branch_A), get_commits_sha(branch_B))
    report = get_diff_report(diff_sha, branch_A + branch_B)
    print('The diff between {branch_A} and {branch_A} is: '.format(branch_A=branch_A_name, branch_B=branch_B_name))
    print(*report, sep='\n')
