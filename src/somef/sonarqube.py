import requests

# Configure SonarCloud URL and authentication token
sonarcloud_url = "https://sonarcloud.io"
auth_token = "fd6d7824c26262e284585b17766385063fa74928"

def upload_file(file_path):
    url = f"{sonarcloud_url}/api/ce/submit"
    headers = {"Authorization": f"Bearer {auth_token}"}

    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print(f"File '{file_path}' uploaded successfully")
    else:
        print(f"Failed to upload file '{file_path}'")
        print(response.text)

def trigger_analysis(project_key):
    url = f"{sonarcloud_url}/api/qualitygates/project_status"
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"projectKey": project_key}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Analysis triggered successfully")
    else:
        print("Failed to trigger the analysis")
        print(response.text)
