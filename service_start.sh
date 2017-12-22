#!/bin/bash

. /utils.sh

# Configure proxy if needed
#echo "proxy=http://myproxy:80/" >> /etc/yum.conf
#export http_proxy=http://myproxy:80
#export https_proxy=https://myproxy:80

print_log "Installing required packages: lftp, openssh-clients, epel-release"
yum -y install lftp openssh-clients epel-release
yum -y install python2-pip
print_log "Done. Installed pre-requisites."

print_log "Installing Tetration Python Client"
pip install tetpyclient

print_log "Fetching Tetration Injector..."

# The following are the credentials of the remote repo. It will be leveraged as sftp server
HOST=1.2.3.4
USER=root
PASS=myrootpwd

# The following must be configured according based on where you installed the service
# Take the following as an example, locate the required files and configure accordingly
lftp -u ${USER},${PASS} sftp://${HOST} <<EOF
cd /repo/services/tetration/scripts
get tetinj-configuration.json
get c3_provisioning_v2.py
get tetration_api.json.json
bye
EOF

print_log "Configuring Tetration..."

export parentJobName
python c3_provisioning_v2.py

STATEFILE=$(ls -1 statefile*json)


print_log "Uploading state file..."

lftp -u ${USER},${PASS} sftp://${HOST} <<EOF
cd /repo/services/tetration/statefiles
put $STATEFILE
bye
EOF

print_log "Done. See you at the deprovisioning phase"
