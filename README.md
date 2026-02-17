# Container Stack Deployment With Ansible 
<!-- <img widht="100" src="https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/container-stack-image.png" allign=left><br> -->
<img src="https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/container-stack-deployment.png" allign=left>

**Container Stack Deployment With Ansible**
<br>**Authors:** _<a href="https://github.com/Filipanderssondev">Filip Andersson</a> and <a href="https://github.com/JonatanHogild">Jonatan Högild</a>_<br>
Publiceringsdatum<br>
<br>

## Abstract
Container stack application Deployment and monitoring on virtual machines running Podman, Managed by Ansible.
<br>

## Table of Contents

1. [Introduction](#introduction)
2. [Goals and Objectives](#goals-and-objectives) <br>
4. [Method](#method)
5. [Target Audience](#target-audience)
6. [Document Status](#document-status)
7. [Disclaimer](#disclaimer)
8. [Scope and Limitations](#scope-and-limitations)
9. [Environment](#environment)
10. [Acknowledgments](#acknowledgments)
11. [Implementation](#implementation) <br>
    	11.1 [Creating the Ansible roles](#creating-the-ansible-roles) <br>
		11.2 [Composing and running the playbooks](#composing-and-running-the-playbooks) <br>
13. [Conclusion](#conclusion)
14. [References](#references) <br>
    14.1 [Other projects in our virtual IT-enviroment](#other-projects-in-our-virtual-it-enviroment)
<br>

## Introduction<br>
**Welcome friend!** <br>
_In this project we are going to deploy a container-based application using infrastructure-as-code (IaC), Ansible. Deployment of containers on two worker VMs, the application VM will serve as our runtime enviroment and the metrics VM serving as our metrics collector / Monitoring for that app, running Prometheus and Grafana. Everything will be managed from our management VM running Ansible. This will be done by configuring Ansible roles, and reusing those roles in playbooks. This is our fourth project <a href="https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/blob/main/Extra/Mermaid/Projects.md">in a series of projects</a> with the end goal of setting up a complete virtualized, automated, and monitored IT-Enviroment as a part of our internship on [The Swedish Meteorological and Hydrological Institute (SMHI)](https://www.smhi.se/en/about-smhi) IT-department at the headquarters in Norrköping. The second goal of these projects are also supposed to serve as a set-up guide here on Github for anyone and everyone that wants to replicate what we have done. we will link every project to each other aswell._ <br>

_[Other projects in our virtual IT-enviroment](#other-projects-in-our-virtual-it-enviroment)_

## Goals and Objectives
The goals and objectives of this project is: 
- To run an application on the application VM, hosting it basic html
- Collect metrics from that app to the metrics VM, displaying it in Grafana.
- Doing it all through Ansible on the management VM
<br>

## Method

The solution was implemented using Ansible on a management VM to automate the deployment of a container-based application on virtual machines running Podman. The container stack consisted of NGINX (frontend) along with monitoring using container based Prometheus node exporters on each vm for exporting metrics, running Prometheus Grafana both as containers on the monitoring vm, configuring prometheus as a data source for Grafana to visualize the result. Reusable Ansible roles and playbooks were used to install dependencies, pull images, and start containers with defined ports and volumes. To collect the container images from the private image registry, an ansible login role was composed and implemented with the mechanics of fetching confidential login credentials defined in the encrypted vault file in our ansible structure.

<!--

- At first i approached with 
As i described in the beginning im going run a container stack / application on the application vm, monitor that application and display the metrics on the metrics vm. I will manage everything through our control vm called Management through Ansible, using roles in playbooks.

  **For the container stack i will run:**
  - NGINX as frontend, displaying basic HTML/CSS
  - Postgres as a database
  - Python as backend
 
  **For monitoring i will run:**
  - Prometheus
  - Grafana
  - Node-exporter on all vms as exporter

Management VM:
 - Ansible roles
 - Ansible Playbooks

Application VM
 - Running Podman as runtime enviroment
 - Running the application

- We have our earlier projects as a foundation, [a Server running Proxmox](https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/tree/) and proxmox running [three replicated virtual machines from a Rocky Linux OS base](https://github.com/Filipanderssondev/Rocky_Linux_OS_Base_for_VMs) and [Ansible configuration on the management vm](https://github.com/JonatanHogild/Ansible_on_management_vm)

<br>

### 3.2 Ansible Roles configuration on Management VM
For each role, i will create a deafults/main.yaml and a tasks/main.yaml as is the standard to have a defaults as fallback and a tasks/main.yaml to descrive how things will be executed, and in playbooks what will be executed. I choose to create reusable roles as it is less repetative then writing tasks in playbooks.

- I will need a role for logging into the private registry
- I will need a role for checking that enviroment tools like podman exists 
- I will need a role who pulls images, run applications.
-->

## Target Audience
- This repo is for anyone who wants a step-by-step guide on .
This repo is also part of a larger project aimed at people interested in learning about IaC, and building such an environment from scratch. 
<br><br>

## Document Status
> [!NOTE]  
> This is an ongoing work right now

## Disclaimer
> [!CAUTION]
> This is intended for learning, testing, and experimentation. The emphasis is not on security or creating an operational environment suitable for production. 

## Scope and Limitations

### Scope
- The scope is inteded to serve as an internship project and learning oppertunity when it comes to working with containers, and to run applications on our virtual machines with redundance

### Limitations
- Naturally we have strict limitations for what we can specify and not. We only specfify public information and our general approach.

## Environment
- [See our foundation from earlier projects](###Our-other-projects)

## Acknowledgments
Great thanks once again to our mentor [Rafael](https://github.com/rafaelurrutiasilva) and [Victor](https://github.com/ludd98) for helping with 

## Implementation

- Note, that some details cant be disclosed due to company policy and that i will speak in general terms. For example the registry i will pull images from i will call _"private-registry.com/repository"_
<br

Every config file is available under the [code directory](https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/tree/main/Code/ansible)

### Configuring reusable roles

What we need is:
- A role for installing/Checking dependencies like Podman
- A role for logging in to the private registry, fetching the credentials in our encryoted vault file
- A role for pulling images, the necisarry images on each machine
- A role for creating and running the containers, with a defaults file (for defining our variables), and a tasks file for the logic.

#### The dependencies installation role
Very straight forward basic. The key to every task in ansible playbooks or roles is the use of ansible modules, like the _ansible.builtin.dnf_ which allows the use of dnf package manager.
~~~yaml
---
- name: Installation of tools
  ansible.builtin.dnf:
    name:
      - podman
    state: present
  become: true

- name: Verify podman version
  ansible.builtin.command: podman --version
~~~
<br>


#### Login role

##### Defaults file

As the registry URL isnt as sensitive information as my                                   
user credentials, its considered best practice to have it  
in my defaults main and not our encrypted vault file

Out of necesity i need to have the tls verify false, i had many issues with certificate suthentivation on the vms so it is easier to do it like this so it dosent fail
~~~yaml
---
#Default image registry
registry_url: "www.private-container-registry.com/myrepository"  # Dummy value for demostration purpose
tlsverify: tls-verify=false
~~~

##### tasks file
This is the logic for logging us in, using the module _containers.podman.podman_login_. Here im referring to the variables in my encrypted vault file. This is considered best practice.

~~~yaml
- name: Login to private-registry
  containers.podman.podman_login:
    registry: "{{ registry_url }}"
    username: "{{ registry_username }}"
    password: "{{ registry_password }}"
    tlsverify: false
~~~

#### image pull role
- Since some image paths varies, for example: <br>
	 _private-registry.com/myrepository/image:tag_ <br>
 	 _private-registry.com/myrepository/manufacturer/image:tag_ <br>
Its considered industry stabdard, and generally safer to create a mechanics for building the image name. 

##### Defaults file
~~~yaml
---
default_registry: "private-registry.com/repository"

#image basics:
default_image: "myimage"
default_tag: "latest"
tlsverify: false
~~~

##### Tasks file
This is the mechanics for the image name builder, For each image in a list, it builds the full image name (registry, optional manufacturer, image name, and version tag). If a version is not specified, it uses a default fallback value defined in the defaults file.
~~~yaml
---
- name: Pull container images
  containers.podman.podman_image:
    name: >-
      {{
        default_registry
        ~ '/'
        ~ (item.get('manufacturer', '') ~ '/' if item.get('manufacturer', '') != '' else '')
        ~ item.image_name
        ~ ':'
        ~ (item.get('tag', default_tag))
      }}
    state: present
~~~

#####

### Deploying the frontend to the application VM

I want to display some basic HTML/CSS/JS on in my frontend container, so i compose basic web files, and since im only going to do this once theres no need to create an entire play for it. So i just send them to my desired directory on the application vm.

#### On the management VM
These are my frontend files: 

#### index.HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Welcome to My App!</h1>
    <button id="clickBtn">Click Me</button>
    <p id="message"></p>

    <script src="script.js"></script>
</body>
</html>
```
#### style.CSS
```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 50px;
}

button {
    padding: 10px 20px;
    font-size: 16px;
}
```

#### script.js
```javascript
document.getElementById('clickBtn').addEventListener('click', function() {
    document.getElementById('message').innerText = "You clicked the button!";
});
```
then i just send them to where i want them. The "-r" means recursivly, so this goes for every folder in the parent folder.
```bash
spc -r /home/Filip/projects/frontend filip@10.208.12.103:/home/Filip/app_projects/frontend
```
<!--
### Composing and running the playbooks
-->

## Conclusion
Slutsats

## References
- [Dockerhub (public image repository](https://hub.docker.com/)
- [Ansible structure](https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/Ansible_structure.md)

### Other projects in our virtual IT-enviroment:
- Project 1 - [Proxmox on Nuc](https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/)
- Project 2 - [Rocky Linux golden image for cloning](https://github.com/Filipanderssondev/Rocky_Linux_OS_Base_for_VMs)
- Project 3 - [Ansible on management VM](https://github.com/JonatanHogild/Ansible_on_management_vm)
- Project 5 - [FreeIPA for Virtual Enviroment](https://github.com/JonatanHogild/FreeIPA_for_virtual_environment/)



