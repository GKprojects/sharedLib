#!/usr/bin/env python
import os
import jenkins
import xml.etree.ElementTree as ET

ns = os.getenv("NAMESPACE")
cluster = os.getenv("CLUSTER_NS")
ROOT_DIR = os.getenv("ROOT_DIR")
folder = ROOT_DIR + "/build/" + cluster + "/jenkins/xml/Tools"
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

folder_name = ns
jenkins_url = f'https://seaeagle.zingworks.com/'
subfolder_name = "Tools"
job_name = "cleanup_pods"
job_config = ET.tostring(root, encoding="unicode")
jenkins_username = os.environ["jenkins_user"]
jenkins_password = os.environ["jenkins_pwd"]
server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
auth = (jenkins_username, jenkins_password)
headers = {
    "Content-Type": "application/json",
    "cleanup_pods-Crumb": "fb6e0bdad638670bf4f96affd5aa650ed015a069669ac5db5c09b4a4dd63140d",
    'Cookie': 'JSESSIONID.fb6e0bdad638670bf4f96affd5aa650ed015a069669ac5db5c09b4a4dd63140d',
}


def create_folder():
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    server.create_folder(folder_name)


def create_nested_folder():
    jenkins_url1 = f'https://seaeagle.zingworks.com/job/{folder_name}'
    server = jenkins.Jenkins(jenkins_url1, username=jenkins_username, password=jenkins_password)
    server.create_folder(subfolder_name)


def create_job_deletecron(name):
    script_path_elements = root.findall('./definition/scriptPath')
    for script_path_element in script_path_elements:
        script_path_element.text = 'Tools/cleanup_pods/Jenkinsfile'
    jenkins_url2 = f'https://seaeagle.zingworks.com/job/{name}/job/{subfolder_name}/'
    server = jenkins.Jenkins(jenkins_url2, username=jenkins_username, password=jenkins_password)
    server.create_job(job_name, job_config)


def create_job_crashloop(name):
    script_path_elements = root.findall('./definition/scriptPath')
    for script_path_element in script_path_elements:
        script_path_element.text = 'Tools/CrashLoopBackOff/Jenkinsfile'
    jenkins_url3 = f'https://seaeagle.zingworks.com/job/{name}/job/{subfolder_name}/'
    server = jenkins.Jenkins(jenkins_url3, username=jenkins_username, password=jenkins_password)
    server.create_job(job_name, job_config)


try:
    info = server.get_job_info(folder_name)
    jenkins_url2 = f'https://seaeagle.zingworks.com/job/{folder_name}/job/{subfolder_name}/'
    server = jenkins.Jenkins(jenkins_url2, username=jenkins_username, password=jenkins_password)
    if server.job_exists(job_name):
        server.reconfig_job(job_name, job_config)
    else:
        create_job_deletecron(name=folder_name)
        create_job_crashloop(name=folder_name)

except Exception as e:
    create_folder()
    create_nested_folder()
    create_job_deletecron(name=folder_name)
    create_job_crashloop(name=folder_name)
