#!/bin/bash


. /usr/local/osmosix/etc/.osmosix.sh
. /usr/local/osmosix/etc/userenv
. /usr/local/osmosix/service/utils/agent_util.sh

source /usr/local/cliqr/etc/userenv
# Add proxy settings if needed
#echo "proxy=http://myproxy/" >> /etc/yum.conf

# Disable local repos if needed
# cat /etc/yum.repos.d/cliqr.repo | sed 's/enabled=1/enabled=0/g' > /etc/yum.repos.d/cliqr.repo

REPO_PROTOCOL="http"
REPO_TET_SENSOR="REPOIP/path/to/dir"
SENSOR_LIST="sensors-list.txt"

agentSendLogMessage "TET: Installing ${TET_SENSOR_TYPE} sensor..."
# Sensor list must be generated on the repo and must have the following format
#
# Example:
#root@package-repo:/repo/tetration/scripts/sensors# ls -1 *.rpm > sensors-list.txt
#root@package-repo:/repo/tetration/scripts/sensors# cat sensors-list.txt
#tet-sensor-2.0.2.17-1.el6-PLX.enforcer.x86_64.rpm
#tet-sensor-2.0.2.17-1.el6-PLX.sensor.x86_64.rpm
#tet-sensor-2.0.2.17-1.el7-PLX.enforcer.x86_64.rpm
#tet-sensor-2.0.2.17-1.el7-PLX.sensor.x86_64.rpm
#


# Fetch sensor list from the repo

wget --proxy=off $REPO_PROTOCOL://$REPO_TET_SENSOR/$SENSOR_LIST

download_install_sensor () {
        # curl -O $REPO_PROTOCOL://$TET_SENSORS_REPO/$1
        wget $REPO_PROTOCOL://$REPO_TET_SENSOR/$1 --proxy=off 
	if [ "$OSTYPE" == "RH" ]; then
          # sudo yum update -y
          sudo yum install -y dmidecode openssl cpio ipset
          sudo yum install -y redhat-lsb
          sudo rpm -Uvh $1
        fi
}

# Only CentOS is supported at the moment

case $imageName in
        "CentOS 6.x" )
                OSTYPE="RH"
                if [ "$TET_SENSOR_TYPE" == "Deep Visibility with Enforcement" ]; then
                        SENSOR_FILENAME=$(cat $SENSOR_LIST | grep el6 | grep enforcer.x86)
                        download_install_sensor $SENSOR_FILENAME
                elif [ "$TET_SENSOR_TYPE" == "Deep Visibility" ]; then
                        SENSOR_FILENAME=$(cat $SENSOR_LIST | grep el6 | grep sensor.x86)
                        download_install_sensor $SENSOR_FILENAME
                else echo "Unknown sensor type. The script will now quit"
                        exit 1
                fi
                ;;
        "CentOS 7.x" )
                OSTYPE="RH"
                if [ "$TET_SENSOR_TYPE" == "Deep Visibility with Enforcement" ]; then
                        SENSOR_FILENAME=$(cat $SENSOR_LIST | grep el7 | grep enforcer.x86)
                        download_install_sensor $SENSOR_FILENAME
                elif [ "$TET_SENSOR_TYPE" == "Deep Visibility" ]; then
                        SENSOR_FILENAME=$(cat $SENSOR_LIST | grep el7 | grep sensor.x86)
                        download_install_sensor $SENSOR_FILENAME
                else echo "Unknown sensor type. The script will now quit"
                        exit 1
                fi
                ;;
        *)
                echo "OS not supported"
                exit 1
esac
agentSendLogMessage "TET: Installed ${TET_SENSOR_TYPE} sensor."

