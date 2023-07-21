#!/usr/bin/env python3
import os
import jenkins
import getpass
from pathlib import Path
import os
import re
import sys
import requests

script_name = os.path.basename(sys.argv[0])

def prepare_xml(template_file, jenkins_file_path):
    template_xml = Path(template_file).read_text()
    replacements = {
        "{git_repo_url}": os.getenv("KF_JENKINS_GIT_REPO_URL", "git@github.com:kf-avengers/kf-jenkins.git"),
        "{git_credential}": os.environ["KF_JENKINS_GIT_CREDENTIAL"],
        "{git_branch}": os.getenv("KF_JENKINS_GIT_BRANCH", "main"),
        "{jenkins_file_path}": jenkins_file_path + "/Jenkinsfile",
    }
    for key, value in replacements.items():
        template_xml = template_xml.replace(key, value)
    return template_xml


def create_jenkins_folder(server: jenkins.Jenkins, folders_list: list):
    for folder in folders_list:
        print("Creating Folder:", folder)
        server.create_job(folder, jenkins.EMPTY_FOLDER_XML)


def create_jenkins_job(server: jenkins.Jenkins, jobs_list: list, jenkins_parent_folder, template_file):
    pattern = re.compile(f"^{jenkins_parent_folder}/(KF4|KF3)")
    for job in jobs_list:
        job_sytem_path = pattern.sub("jobs", job)
        template_xml = prepare_xml(template_file, job_sytem_path)
        print("Creating Job:", job)
        server.create_job(job, template_xml)


def get_folder_tree(folders_list, jobs_list, jobs_folder, jenkins_parent_folder):
    for root, dirs, files in os.walk(jobs_folder):
        if "Jenkinsfile" in files:
            jobs_list.append(root.replace(jobs_folder, jenkins_parent_folder))
        else:
            # exclude jobs folder form jenkins folder creation
            if root == jobs_folder:
                continue
            folders_list.append(root.replace(jobs_folder, jenkins_parent_folder))

def send_notification(message):
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAASAnfTNY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Z9u9vLWAS_Ri74xEIsw9z17lbA6sSbl6Qpn9iyiMvF4"
    headers = {"Content-Type": "application/json"}
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")


from pathlib import Path
import os
import jenkins
import getpass


def main():
    # Get root path of kf-jenkins folder; this the base path for all folder walks
    root_path = Path(__file__).parent.parent.absolute()
    jobs_folder = os.path.join(root_path, "jobs")
    template_file = os.path.join(root_path, "bin/JOB_TEMPLATE.xml")

    # Fetch Jenkins configurations from environment variables
    jenkins_url = os.environ["JENKINS_URL"]
    jenkins_parent_folder = os.environ["CLUSTER_NS"]
    jenkins_username = os.getenv("JENKINS_USERNAME") or input("Enter Jenkins Username: ")
    jenkins_password = os.getenv("JENKINS_PASSWORD") or getpass.getpass("Enter Jenkins Password: ")

    # Connect to Jenkins server
    server = jenkins.Jenkins(
        url=jenkins_url, username=jenkins_username, password=jenkins_password
    )
    try:
        user = server.get_whoami()
        version = server.get_version()
        print(f"Hello {user['fullName']} from Jenkins {version}")
    except Exception as e:
        print(f"Error in Connecting to Jenkins server {jenkins_url}\n{e}")
        exit(1)

    # Delete the Jenkins parent folder if it exists and create a new one
    try:
        server.delete_job(jenkins_parent_folder)
    except:
        pass
    
    # Send a notification & Exit the If undeploy.py is executed 
    if script_name == "undeploy.py":
        print(f"Undeploy script is executed, hence deleted {jenkins_parent_folder} & exiting")
        print(f"Execute deploy.py to create jobs in {jenkins_parent_folder}")
        message = f"Undeploy script is executed, {user['fullName']} removed {jenkins_parent_folder} folder from Jenkins server {jenkins_url}"
        print(message)
        send_notification(message)
        sys.exit(0)
        
    server.create_folder(folder_name=jenkins_parent_folder)

    # Define required lists
    system_folders_list = []
    system_jobs_list = []
    jenkins_jobs_list = []
    jenkins_folders_list = [f"{jenkins_parent_folder}/KF3", f"{jenkins_parent_folder}/KF4"]

    get_folder_tree(system_folders_list, system_jobs_list, jobs_folder, jenkins_parent_folder)

    # Append system folders and jobs to their respective Jenkins lists
    for item in system_folders_list:
        jenkins_folders_list.extend([f"{jenkins_parent_folder}/KF3/{'/'.join(item.split('/')[1:])}",
                                      f"{jenkins_parent_folder}/KF4/{'/'.join(item.split('/')[1:])}"])
    for item in system_jobs_list:
        kf3_item = item.replace(f'{jenkins_parent_folder}/', f'{jenkins_parent_folder}/KF3/')
        kf4_item = item.replace(f'{jenkins_parent_folder}/', f'{jenkins_parent_folder}/KF4/')
        jenkins_jobs_list.extend([kf3_item, kf4_item])

    create_jenkins_folder(server, jenkins_folders_list)
    create_jenkins_job(server, jenkins_jobs_list, jenkins_parent_folder, template_file)

    print("All set, Jenkins jobs are configured successfully.")
    print(f"Jobs Folder url: {jenkins_url}/job/{jenkins_parent_folder}")
if __name__ == "__main__":
    main()
