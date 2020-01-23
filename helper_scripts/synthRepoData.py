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
def synthRepoDataWithHttp(repo_data_file, git_url, outfile):
    with open(repo_data_file) as json_file:
        data = json.load(json_file)
        git_data = httpToJson(git_url)
        
        data['description.sk'].append(git_data['description'])

        with open(outfile, 'w') as output:
            json.dump(data, output)

#for testing purposes
#synthRepoDataWithHttp(repo, git, out)
