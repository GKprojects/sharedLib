import os

import requests
from jenkinsapi.jenkins import Jenkins
import xml.etree.ElementTree as ET

folder = "/Users/malavika/Desktop/PycharmProjects/Kf-Devops-Tools/kf-devops-tools/Tools/xml/"
filename = "cleanup_pods.xml"
filepath = os.path.join(folder, filename)
tree = ET.parse(filepath)
root = tree.getroot()

folder_name = "stg"
subfolder_name = "Tools"
job_name = "cleanup_pods"

jenkins_username = os.environ["jenkins_user"]
jenkins_password = os.environ["jenkins_pwd"]

headers = {
    'Content-Type': 'application/json',
    "Authorization": f"Basic {jenkins_username}:{jenkins_password}",
    'Cookie': 'JSESSIONID.fd0ba9f1=node084zc0jckw5cb1g631h6bp0ds342714.node0'
}


def create_folder():
    url = f'https://seaeagle.zingworks.com/createItem?name={folder_name}&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK'
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def create_nested_folder():
    url = f'https://seaeagle.zingworks.com/job/{folder_name}/createItem?name={subfolder_name}&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK'
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def create_job(name):
    jenkins_url = f'https://seaeagle.zingworks.com/job/{name}/job/{subfolder_name}/'
    username = jenkins_username
    password = jenkins_password
    server = Jenkins(jenkins_url, username=username, password=password)
    job_config = ET.tostring(root, encoding="unicode")
    server.create_job(job_name, job_config)


create_folder()
create_nested_folder()
create_job(name=folder_name)
