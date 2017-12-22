#!/bin/bash

. /utils.sh

# Configure proxy if needed
#echo "proxy=http://myproxy:80/" >> /etc/yum.conf
#export http_proxy=http://myproxy:80
#export https_proxy=https://myproxy:80

print_log "Installing required packages: lftp, openssh-clients, epel-release"
yum -y install lftp openssh-clients epel-release
yum -y install python2-pip
print_log "Done."

print_log "Installing Tetration Python Client"
pip install tetpyclient

print_log "Fetching Tetration Cleaner"

export parentJobName 
export STATEFILE="statefile_$parentJobName.json"

# The following are the credentials of the remote repo. It will be leveraged as sftp server
HOST=1.2.3.4
USER=root
PASS=myrootpwd

# The following must be configured according based on where you installed the service
# Take the following as an example, locate the required files and configure accordingl
lftp -u ${USER},${PASS} sftp://${HOST} <<EOF
cd /repo/services/tetration/scripts
get tetinj-configuration.json
get c3_deprovisioning_v2.py
get c3_integration_pvt18.json
cd /repo/services/tetration/statefiles
get $STATEFILE
bye
EOF

print_log "Cleaning up Tetration config..."


python c3_deprovisioning_v2.py

print_log "Removing statefile from the repository..."

# The following must be configured according based on where you installed the service
lftp -u ${USER},${PASS} sftp://${HOST} <<EOF
cd /repo/services/tetration/statefiles
rm $STATEFILE
bye
EOF

print_log "Configuration cleared"
