from flask import render_template, flash, send_from_directory, send_file
from app.giturl_class.url_form import UrlForm
from app.giturl_class.download_form import DownloadButton
from app.giturl_class import bp
import json

@bp.route('/index', methods = ['GET', 'POST'])
def urlPage():
    urlForm = UrlForm()
    downloadForm = DownloadButton()

    citation = None
    installation = None
    invocation = None
    description = None
    showDownload = None
    git_name = None
    git_owner = None
    git_topics = None
    git_languages = None

    if downloadForm.submit_download.data:
        return send_file("giturl_class/testfile.txt", as_attachment=True)
        #flash("Download")
        
    if urlForm.validate_on_submit() and urlForm.submit.data:
        #flash("Classifying data")

        with open('data/output.json') as json_file:
            data = json.load(json_file)
            citation = data['citation.sk']
            installation = data['installation.sk']
            invocation = data['invocation.sk']
            description = data['description.sk']
            git_name = data["name"]
            git_owner = data["owner"]
            git_topics = data["topics"]
            git_languages = data['languages']
            showDownload = True

    return render_template('giturl_class/giturl.html',
                           form = urlForm,
                           downloadForm = downloadForm,
                           showDownload = showDownload,
                           citation = citation,
                           installation = installation,
                           invocation = invocation,
                           description = description,
                           git_name = git_name,
                           git_owner = git_owner,
                           git_languages = git_languages)


@bp.route('/about', methods = ['GET'])
def aboutPage():
    return render_template('aboutpage/aboutpage.html')


@bp.route('/help', methods = ['GET'])
def helpPage():
    return render_template('helppage/helppage.html')
