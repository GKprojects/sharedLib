# kf-jenkins

## Usage Steps

### Activate the Cluster Namespace for which you want to create the jobs for
source activate <cluster-ns>

### Perform make jenkins to download Jenkins charts similar to make charts
make jenkins

### Jump to Jenkins directory
tojen

### Deploy Jenkins jobs
./bin/deploy.py

### Enter your Jenkins username (kissflow mail id) and API token as password
