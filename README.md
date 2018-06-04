<<<<<<< HEAD
#Moved to: https://gitlab.com/rtortori/cisco-c3-tetration-injector
=======
# Warning: This repo has been moved to https://gitlab.com/rtortori/cisco-c3-tetration-injector.git

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
- In Tetration, you are required to have at least an existing scope bound with a VRF. 
You are also required to preconfigure a sensor profile

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
 The sensor list will be downloaded by the deployed nodes in order to pick the right sensor based on user choice 
 (Deep Visibility vs Deep Visibility with Enforcement) and target OS.<br>
 
### Fetch required configuration details from Tetration
Under the directory **support**, a few python scripts have been provided in order to fetch the required
configuration item from Tetration.
You are required to have a working Tetration API key file inside the same directory where you will run the scripts.
This needs to be referenced in the CREDENTIALS_FILE. You will also need to specify your API_ENDPOINT
#### Examples:
Running the *get_soft_sens_profile.py* script will generate an output similar to the following (output truncated):
```
[...]
    {
        "auto_upgrade_opt_out": false, 
        "cpu_quota_mode": 1, 
        "cpu_quota_pct": 3, 
        "cpu_quota_us": 30000, 
        "created_at": 1512573137, 
        "data_plane_disabled": false, 
        "enable_pid_lookup": true, 
        "enforcement_disabled": false, 
        "id": "5a2808d1755f025d8ccb4eb9", 
        "name": "c3-profile", 
        "updated_at": 1512573137
    }
[...]
```

Identify your exiting sensor profile name and its ID (in the example: "id": "5a2808d1755f025d8ccb4eb9", 
        "name": "c3-profile")
<br>
Running the *get_soft_sens_profile.py* script will generate an output similar to the following (output truncated):
```
[...]
{
        "child_app_scope_ids": [
            "59f99b18755f023679cb4eb6"
        ], 
        "description": null, 
        "dirty": false, 
        "dirty_short_query": null, 
        "filter_type": "AppScope", 
        "id": "59e4b74a497d4f36417521c2", 
        "name": "Default", 
        "parent_app_scope_id": "", 
        "policy_priority": 1, 
        "priority": "001:Z", 
        "query": {
            "field": "vrf_id", 
            "type": "eq", 
            "value": 1
        }, 
        "short_name": "Default", 
        "short_priority": 1, 
        "short_query": {
            "field": "vrf_id", 
            "type": "eq", 
            "value": 1
        }, 
        "vrf_id": 1
    }, 
[...]
```

Identify your Default scope ID and your parent scope ID (in the example: "id": "59e4b74a497d4f36417521c2", 
        "name": "Default")

### Configuration
* Clone into your favourite C3 repository directory
* Open the **scripts/tetinj-configuration.json** configuration file and fill with your setup details
    * API_ENDPOINT is your target Tetration FQDN
    * CREDENTIALS_FILE is your Tetration API key file
    * PARENT_SCOPE is the ID of your parent scope. Use the support script to fetch the ID
    * PARENT_SCOPE_VRF_ID is the numeric ID of your parent scope VRF (i.e. 43)
    * DEFAULT_SCOPE_ID is the ID of your Default scope in Tetration. This is needed because some 
    inventory filters will be created to steer sensors in the right VRF. Use the support script to fetch the
    Default scope ID
     **Note:** If you are using Remote VRF
    to support NAT, this might be not required as the sensors will go automatically into the right VRF based
    on their gateway IP
    * SENSOR_CONFIG_PROF_ID is the ID of your sensor config profile. A new configuration intent will be 
    created automatically and will be bound to an existing sensor configuration profile. Use the support
    script to fetch the ID
    
## Cloudcenter configuration
As specified in the prerequisites and caveats section, you will need to have a working setup with 
hostname callout strategy configuration.<br>
The name of your deployment will be reflected in the node names and will also be referenced within Tetration to
setup scopes and filters.<br>

The following are the required configuration steps to enable Tetration injector in CloudCenter. The process is
also documented in the Integration Video Resources section below:
* Create a new external service
    * Add a logo, a name and a service ID
    * Configure a Start and Stop script as follows:
        * Start: select your CloudCenter repository and reference the service_start.sh script. <br>Pay attention 
        to the path
        * Stop: select your CloudCenter repository and reference the service_stop.sh script. <br>Pay attention 
        to the path
    * Save the Tetration Injector service
    * Open a new or existing application profile and drag into the topology panel the new Tetration 
    Injector service. Create inter-dependencies so that Tetration Injector will be the first service to start. 
    You will find it in the *Custom Service* folder
    * Create a new global parameter called *TET_SENSOR_TYPE*, configure it as a list of elements and 
    paste the following:<br>
        > Deep Visibility,Deep Visibility with Enforcement<br>
    
        Specify a default value or leave it blank if you want to manually specify the sensor type
        on each deployment.<br>
        The parameter should be visible and editable by the user
    * Click on each tier of the application profile and:
        * Specify the sensor_install.sh script (with the 
          correct path on the repo) under the *Post-Start Script* section
        * Specify the sensor_uninstall.sh script (with the 
          correct path on the repo) under the *Pre-Stop Script* section
        * Under *Environment Variables*, create a new variable with Name: *TET_SENSOR_TYPE* and
        Value: *%TET_SENSOR_TYPE%*<br>
        Again, this needs to be editable and visible by the user. This variable will make the nodes 
        carrying over the global parameter specified at deployment phase so it will know what sensor
        to install
    * Save your application profile and deploy! 


## Integration video resources

[Cisco CloudCenter Overview](https://cisco.box.com/s/gy3hef6zkvpmpqvpriyfth5trlr2m7u0 "CloudCenter Overview")<br><br>
[CloudCenter - AppDynamics sensor installation configuration](https://cisco.box.com/s/zmz52b8z29fjtnouofpcpwkkbe3rjdjg "CloudCenter - AppDynamics sensor installation configuration")<br><br>
[CloudCenter - Tetration Injector configuration](https://cisco.box.com/s/ik4suj1770snxh72sdqk55ju3q3hiuzk "CloudCenter - Tetration Injector configuration")<br><br>
[Deployment](https://cisco.box.com/s/lngwq06mbtglh9c5f8zk4cpfyqchahv5 "Deployment")<br><br>
[Tetration outcome](https://cisco.box.com/s/3exey04nqua2hkrr995wvqyagm6qubx0 "Tetration outcome")<br><br>
[AppDynamics outcome](https://cisco.box.com/s/zm844tj0gps49f7bksi32dj6fgqcd95h "AppDynamics outcome")<br><br>

#### To do!
* Add AppD scripts
>>>>>>> origin/master
