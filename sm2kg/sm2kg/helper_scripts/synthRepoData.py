import requests
import json

#for testing purposes
repo = '../data/output2.json'
out = '../data/synth_output.json'
git = 'https://api.github.com/repos/quiteaniceguy/ChaoskeyDaemon'

def httpToJson(url):
    r = requests.get(url)
    if(r.status_code == 200):
            return r.json()

#synthesizes repo json with gitub description(using api) and outputs to another json
#should check if actually git url probably
def synthRepoDataWithHttp(git_data, repo_data, outfile):   
    
    for i in git_data.keys():
        if(i == 'description'):
            repo_data['description.sk'].append(git_data[i])
        else:
            repo_data[i] = git_data[i]

    with open(outfile, 'w') as output:
        json.dump(repo_data, output)

#for testing purposes
#synthRepoDataWithHttp(repo, git, out)
with open(repo) as file_one:
    repo_data = json.load(file_one)
with open('output.json') as file_two:
    git_data = json.load(file_two)

synthRepoDataWithHttp(git_data, repo_data, out)

