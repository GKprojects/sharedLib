# kf-jenkins

## Usage Steps

### Activate the Cluster Namespace for which you want to create the jobs for from kf-configs
source activate cluster-ns 

**Note:** Make sure to validate the JENKINS_AUTOMATION section under env.sh, you can update JENKINS_GIT_BRANCH to the feature branch you want to test

### Perform make jenkins to download Jenkins charts similar to make charts
make jenkins

### Jump to Jenkins directory
tojen

### Deploy Jenkins jobs
./bin/deploy.py

### Enter your Jenkins username (kissflow mail id) and API token as password
