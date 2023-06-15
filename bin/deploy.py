#!/usr/bin/env python3
import os
import jenkins
from pathlib import Path
import getpass
from pathlib import Path
import os


def prepare_xml(template_file, jenkins_file_path):
    template_xml = Path(template_file).read_text()
    git_repo_url = os.getenv(
        "KF_JENKINS_GIT_REPO_URL", "git@github.com:kf-avengers/kf-jenkins.git"
    )
    git_credential = os.environ["KF_JENKINS_GIT_CREDENTIAL"]
    git_branch = os.getenv("KF_JENKINS_GIT_BRANCH", "main")
    template_xml = template_xml.replace("{git_repo_url}", git_repo_url)
    template_xml = template_xml.replace("{git_credential}", git_credential)
    template_xml = template_xml.replace("{git_branch}", git_branch)
    template_xml = template_xml.replace("{jenkins_file_path}", jenkins_file_path+"/Jenkinsfile")
    return template_xml


def create_jenkins_folder(server: jenkins.Jenkins, folders_list: list):
    for folder in folders_list:
        print("Folder:", folder)
        server.create_job(folder, jenkins.EMPTY_FOLDER_XML)


def create_jenkins_job(
    server: jenkins.Jenkins, jobs_list: list, jenkins_parent_folder, template_file
):
    for job in jobs_list:
        template_xml = prepare_xml(
            template_file, job.replace(jenkins_parent_folder, "jobs")
        )
        server.create_job(job, template_xml)


def populate_jenkins_folders_jobs(folders_list, jobs_list, jobs_folder, jenkins_parent_folder):
    for root, dirs, files in os.walk(jobs_folder):
        if "Jenkinsfile" in files:
            jobs_list.append(root.replace(jobs_folder, jenkins_parent_folder))
        else:
            # exclude jobs folder form jenkins folder creation
            if root == jobs_folder:
                continue
            folders_list.append(root.replace(jobs_folder, jenkins_parent_folder))


def main():
    # get root path kf-jenkins folder; this the base path all folder walks
    root_path = Path(__file__).parent.parent.absolute()
    jobs_folder = os.path.join(root_path, "jobs")
    template_file = os.path.join(root_path, "bin/JOB_TEMPLATE.xml")

    jenkins_url = os.environ["JENKINS_URL"]
    jenkins_parent_folder = os.environ["CLUSTER_NS"]
    jenkins_username = os.getenv("JENKINS_USERNAME")
    jenkins_password = os.getenv("JENKINS_PASSWORD")

    if not jenkins_username:
        jenkins_username = input("Enter Jenkins Username: ")
    if not jenkins_password:
        jenkins_password = getpass.getpass("Enter Jenkins Password: ")

    server = jenkins.Jenkins(
        url=jenkins_url, username=jenkins_username, password=jenkins_password
    )
    try:
        user = server.get_whoami()
        version = server.get_version()
        print("Hello %s from Jenkins %s" % (user["fullName"], version))
    except Exception as e:
        print("Error in Connecting to Jenkins server", jenkins_url)
        print(e)
        exit(1)

    try:
        server.delete_job(jenkins_parent_folder)
    except:
        pass
    server.create_folder(folder_name=jenkins_parent_folder)

    folders_list = []
    jobs_list = []
    populate_jenkins_folders_jobs(folders_list, jobs_list, jobs_folder, jenkins_parent_folder)
    create_jenkins_folder(server, folders_list)
    create_jenkins_job(server, jobs_list, jenkins_parent_folder, template_file)


if __name__ == "__main__":
    main()
