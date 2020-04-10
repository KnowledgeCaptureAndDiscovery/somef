
from flask import render_template, flash, send_from_directory, send_file
from app.giturl_class.url_form import UrlForm
from app.giturl_class.download_form import DownloadButton
from app.giturl_class import bp
import json
import os

USE_TEST_FILE = False
if(os.getenv('SM2KG_TEST_MODE') == 'TRUE'):
    USE_TEST_FILE = True
    print('SM2KG in Test Mode')
if(not USE_TEST_FILE): 
    #from sm2kg import cli
    from somef import cli 
from somef import cli

dirname = os.path.dirname(__file__)


@bp.route('/index', methods = ['GET', 'POST'])
def urlPage():
    urlForm = UrlForm()
    downloadForm = DownloadButton()

    citation_list = []
    installation_list = []
    invocation_list = []
    description_list = []
    description_conf_list = None
    showDownload = None
    git_name = None
    git_owner = None
    git_topics = None
    git_languages = None
    git_license = None
    git_forks_url = None
    git_topics = []
    git_languages = []
    git_readme_url = None

    

    if downloadForm.submit_download.data:
        output_file = os.path.join(dirname, '../data/output.txt')
        return send_file("../data/output.json", as_attachment=True)
        #flash("Download")
        
    if urlForm.validate_on_submit() and urlForm.submit.data:
        #flash("Classifying data")

        showDownload = True
        try: 
            cli.run_cli(urlForm.giturl.data, .8, 'data/output.json')
        except Exception as e: 
            print("Error: " + e) 
            flash("There must be a problem with your link")
            showDownload = False 
        inputFile = 'data/output.json'
        if(USE_TEST_FILE):
            inputFile = 'data/test.json'
            showDownload = True
        with open(inputFile) as json_file:
            data = json.load(json_file)
            for i in data['citation']:
                if type(i) is dict:
                    citation_list.append(i['excerpt'])
            for i in data['installation']:
                if type(i) is dict:
                    installation_list.append(i['excerpt'])
            for i in data['invocation']:
                if type(i) is dict:
                    invocation_list.append(i['excerpt'])
            
            for i in data['description']: 
                #some aren't dictionaries because pulled git data is appended, to make uniform maybe add pulled data with 100% confidence
                if type(i) is dict:
                    description_list.append(i['excerpt'])
                else:
                    description_list.append(i)

            
            git_name = data["name"]["excerpt"]
            git_owner = data["owner"]["excerpt"]
            git_topics = data["topics"]["excerpt"]
            git_languages = data['languages']["excerpt"]
            git_license = data['license']["excerpt"] 
            git_forks_url = data['forks_url']['excerpt']
            git_topics = data['topics']['excerpt']
            git_languages = data['languages']['excerpt']
            git_readme_url = data['readme_url']['excerpt']


        

    return render_template('giturl_class/giturl.html',
                           form = urlForm,
                           downloadForm = downloadForm,
                           showDownload = showDownload,
                           citation = citation_list,
                           installation = installation_list,
                           invocation = invocation_list,
                           description = description_list,
                           git_name = git_name,
                           git_owner = git_owner,
                           git_languages = git_languages,
                           git_license = git_license,
                           git_forks_url = git_forks_url,
                           git_topics = git_topics, 
                           git_readme_url = git_readme_url)


@bp.route('/about', methods = ['GET'])
def aboutPage():
    return render_template('aboutpage/aboutpage.html')


@bp.route('/help', methods = ['GET'])
def helpPage():
    return render_template('helppage/helppage.html')
