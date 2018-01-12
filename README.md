# Tetration Analytics injector service for Cisco Cloudcenter
**Disclaimer**: This is NOT an official Cisco application and comes with absolute NO WARRANTY!<br>
It doesn't represent an official and production ready integration system but it's only a concept that highlights
the programmability features of CloudCenter, Tetration Analytics and AppDynamics.

This repository contains the required scripts and resources needed to create a custom
 external service in Cloudcenter in order to add Tetration telemetry support to your new or existing
 Application Profiles.
<br>
<br>
Long story short: deploy applications (new or existing ones) in Cloudcenter and have them onboarded in 
Tetration automatically.<br>
The system will create everything is needed in Tetration based on the name you give in the deployment 
phase, each deployment will have its own space and ADM (with the right sensors in it) and everything 
will be cleared up when deprovisioning.<br>
It will also install the sensors automatically based on the OS/version detected and type of sensor 
(Deep visibility or Enforcement) selected by the user at the deployment phase, 
the idea is to deploy and don’t configure anything on Tetration. <br>

**Note**: This repository also includes scripts to deploy AppDynamics sensors as well as Tetration sensors. <br>
Unlike Tetration sensors, they are bound to the application itself and need to be selected based on the 
application technology (i.e. .NET, Java, PHP, etc...). <br>
Keep this in mind when using these scripts in your setup.

### How to use these scripts
Though the usage and configuration are pretty straightforward, it is assumed to have a good knowledge of CloudCenter,
Tetration and AppDynamics. <br>
If you are not sure, engage with Cisco to have guidance on the integration of Cloudcenter, Tetration Analytics 
and AppDynamics.



### Resources
[Cisco CloudCenter](https://www.cisco.com/c/en/us/products/cloud-systems-management/cloudcenter/index.html "Cisco CloudCenter") docs.<br>
[Cisco Tetration Analytics](https://www.cisco.com/c/en/us/products/data-center-analytics/tetration-analytics/index.html "Cisco Tetration Analytics") docs.<br>
[Cisco AppDynamics](https://www.appdynamics.com/ "AppDynamics") docs.

Connect to [dcloud](https://dcloud.cisco.com/ "Cisco dCloud") to access free labs with detailed walkthroughs on Tetration and CloudCenter!<br>

### Prerequisites and caveats

- CloudCenter hostname strategy must be hostname callout, therefore target cloud must be VMWare 
(Openstack not supported at present time)
- CloudCenter Repository should be writable using sftp
- Repository password will be stored in clear text

Tested platforms:
- CloudCenter 4.8 CCO running Centos7 (virtual appliance downloaded from cisco.com) 
- Cisco Tetration Analytics 2.2.1<br><br>

Supported nodes for sensor installation: 
- Linux CentOS and RHEL 6 and 7

### Before you start
* From Tetration UI, you need to generate an API key. This key needs to be stored in a file called tetration_api.json
in the same directory of c3-provisioning_v2.py script. Ensure the key has enough rights to create scopes, 
inventory filters, sensor profiles and application workspace.
* Ensure your repository can be accessed using sftp with a user that can read/write
* Create an Application Profile like you would normally do in your environment
* Clone this from a directory in your repo. These scripts will need to be accessed by the CloudCenter orchestrator (CCO)
* Tetration sensors cannot be downloaded from cisco.com as they embed credentials and certificates so they won't need
any configuration after installation. From your Tetration cluster, download Deep Visibility and Enforcement sensors for 
CentOS/RHEL 6 and 7. Store them in the repo under the sensors/ directory of this repo
* In the same directory you uploaded your sensors rpm, generate the sensors list as follows:

Example:
```
#root@package-repo:/repo/tetration/scripts/sensors# ls -1 *.rpm > sensors-list.txt
#root@package-repo:/repo/tetration/scripts/sensors# cat sensors-list.txt
tet-sensor-2.0.2.17-1.el6-PLX.enforcer.x86_64.rpm
tet-sensor-2.0.2.17-1.el6-PLX.sensor.x86_64.rpm
tet-sensor-2.0.2.17-1.el7-PLX.enforcer.x86_64.rpm
tet-sensor-2.0.2.17-1.el7-PLX.sensor.x86_64.rpm
```
## To be continued :)
