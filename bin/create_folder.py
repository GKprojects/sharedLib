#!/usr/bin/env python
import os
import jenkins
import xml.etree.ElementTree as ET

ns = os.getenv("NAMESPACE")
cluster = os.getenv("CLUSTER_NS")
ROOT_DIR = os.getenv("ROOT_DIR")
folder = ROOT_DIR+"/build/" + cluster + "/jenkins/xml/Tools"
filename = "templates.xml"
filepath = os.path.join(folder, filename)
tree = ET.parse(filepath)
root = tree.getroot()

url_elements = root.findall('.definition/scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url')
for url_element in url_elements:
    url_element.text = 'git@github.com:kf-avengers/kf-jenkins.git'

name_elements = root.findall('.definition/scm/branches/hudson.plugins.git.BranchSpec/name')
for name_element in name_elements:
    name_element.text = '*/main'

script_path_elements = root.findall('./definition/scriptPath')
for script_path_element in script_path_elements:
    script_path_element.text = 'Tools/cleanup_pods/Jenkinsfile'

folder_name = ns
subfolder_name = "Tools"
job_name = "cleanup_pods"
job_config = ET.tostring(root, encoding="unicode")

jenkins_username = os.environ["jenkins_user"]
jenkins_password = os.environ["jenkins_pwd"]
auth = (jenkins_username, jenkins_password)
headers = {
    "Content-Type": "application/json",
    "cleanup_pods-Crumb": "fb6e0bdad638670bf4f96affd5aa650ed015a069669ac5db5c09b4a4dd63140d",
    'Cookie': 'JSESSIONID.fb6e0bdad638670bf4f96affd5aa650ed015a069669ac5db5c09b4a4dd63140d',
}


def create_folder():
    jenkins_url = f'https://seaeagle.zingworks.com/'
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    server.create_folder(folder_name)


def create_nested_folder():
    jenkins_url = f'https://seaeagle.zingworks.com/job/{folder_name}/'
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    server.create_folder(subfolder_name)


def create_job(name):
    jenkins_url = f'https://seaeagle.zingworks.com/job/{name}/job/{subfolder_name}/'
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    server.create_job(job_name, job_config)


create_folder()
create_nested_folder()
create_job(name=folder_name)