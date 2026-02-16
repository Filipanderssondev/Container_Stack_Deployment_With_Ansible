# Container Stack Deployment With Ansible 
<img widht="100" src="https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/container-stack-image.png" allign=left><br>

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
11. [Implementation](#implementation)
12. [Conclusion](#conclusion)
13. [References](#references)
<br>

## Introduction<br>
**Welcome friend!**
In this project we are going to deploy a container-based application using infrastructure-as-code (IaC), Ansible. Deployment of containers on two worker VMs, the application VM will serve as our runtime enviroment and the metrics VM serving as our metrics collector / Monitoring for that app, running Prometheus and Grafana. Everything will be managed from our management VM running Ansible. This will be done by configuring Ansible roles, and reusing those roles in playbooks. This is our fourth project <a href="https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/blob/main/Extra/Mermaid/Projects.md">in a series of projects</a> with the end goal of setting up a complete virtualized, automated, and monitored IT-Enviroment as a part of our internship on [The Swedish Meteorological and Hydrological Institute (SMHI)](https://www.smhi.se/en/about-smhi) IT-department at the headquarters in Norrköping. The second goal of these projects are also supposed to serve as a set-up guide here on Github for anyone and everyone that wants to replicate what we have done. we will link every project to each other aswell._<br>

**<a href="https://github.com/Filipanderssondev">Filip Andersson</a> and <a href="https://github.com/JonatanHogild">Jonatan Högild</a>**
<br>
<br>

## Goals and Objectives
The goals and objectives of this project is: 
- To run an application on the application VM, hosting it basic html
- Collect metrics from that app to the metrics VM, displaying it in Grafana.
- Doing it all through Ansible on the management VM
<br>

## Method

The solution was implemented using Ansible on a management VM to automate the deployment of a container-based application on virtual machines with Podman. The container stack consisted of NGINX (frontend), Python (backend), and Postgres (database), along with monitoring using Prometheus and Grafana. Reusable Ansible roles and playbooks were used to install dependencies, pull images, and start containers with defined ports and volumes. To collect the container images from the private image registry, an ansible login role was composed and implemented with the mechanics of fetching confidential login credentials defined in the encrypted vault file in our ansible structure.

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

My project structuer will look something like this:
<br>
~~~yaml
ansible/roles
├── containers
│   ├── images
│   │   └── pull
│   │       ├── defaults
│   │       │   └── main.yaml
│   │       └── tasks
│   │           └── main.yaml
│   ├── install
│   │   └── tasks
│   │       └── main.yaml
│   ├── login
│   │   ├── filip
│   │   │   ├── defaults
│   │   │   │   └── main.yaml
│   │   │   └── tasks
│   │   │       └── main.yaml
│   │   └── jonatan
│   └── run
│       ├── defaults
│       │   └── main.yaml
│       └── tasks
│           └── main.yaml
~~~

#### 3.2.1 Log in Role

<br>

#### 3.2.2 Installation role

<br>

#### 3.2.3 image Pull role

ansible/roles/containers/images/pull/defaults/main.yaml
~~~yaml
---
default_registry: "private-registry.com/repository"

#image basics
image_name: ""
tag: "latest"
tlsverify: false

#manufacturer if needed like prom/prometheus:latest
manufacturer: ""

images_to_pull:[]
~~~

ansible/roles/containers/images/pull/tasks/main.yaml

~~~yaml
---
- name: Pull images
  containers.podman.podman_image:
    name: >-
      {{
        default_registry
        + '/'
	+ (item.manufacturer ~ '/' if item.manufacturer is defined else '')
        + item.image_name
        + ':'
	+ (item.tag | default(default_tag))
      }}
    state: present
    tlsverify: "{{ tlsverify }}"
  loop: "{{ images_to_pull }}"
~~~



#### 3.2 Deploying the application
draft:

/ansible/playbooks/container_projects/deploy_app.yaml
~~~yaml
---
- name: Deploy containers
  hosts: application
  become: true
  roles:
    - role: containers/install
    - role: containers/login/filip

  tasks:
    - name: Run nginx frontend
      include_role:
        name: containers/run
      vars:
        container_name: nginx_frontend
        image_name: nginx
        tag: 1.29.4
        container_ports:
          - "8081:80"
        container_volumes:
          - "/home/Filip/app_projects/frontend:/usr/share/nginx/html:Z"
        container_cmd:
          - "sh"
          - "-c"
          - "chown -R 0:0 /usr/share/nginx/html && nginx -g 'daemon off;'"
        container_state: started
        container_restart_policy: always
        container_env_vars: {}

    - name: Run postgres
      include_role:
        name: containers/run
      vars:
        container_name: database
        image_name: postgres
        tag: latest
        container_ports:
          - "5433:5432"
        container_state: started
        container_restart_policy: always
        container_env_vars: {}
~~~

##### Debug
N/A

<br>
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

#### Step 1: Creating the Absible roles

What we need is:
- A role for installing/Checking dependencies like Podman
- A role for logging in to the private registry, fetching the credentials in our encryoted vault file
- A role for pulling images, the necisarry images on each machine
- A role for creating and running the containers, with a defaults file (for defining our variables), and a tasks file for the logic.

**The install role**
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

**The login role**

The defaults:
~~~yaml
---
#Default image registry
registry_url: "www.private-container-registry.com/myrepository"  # Dummy value for demostration purpose
tlsverify: tls-verify=false

# As the registry URL isnt as sensitive information as my                                   
# user credentials, its considered best practice to have it  
# in my defaults main and not our encrypted vault file

# PS: Out of necesity i need to have the tls verify false, 
#i had many issues with certificate suthentivation on the vms so it is easier to do it like this so it dosent fail
~~~

the login tasks, the logic behind it:
~~~yaml
- name: Login to private-registry
  containers.podman.podman_login:
    registry: "{{ registry_url }}"
    username: "{{ registry_username }}"
    password: "{{ registry_password }}"
    tlsverify: false

#Login Mechanics
#Referring to my credentials in our encrypted vault file following best practice methods
~~~

**The image pull role:**
- Since some image paths varies, for example:
  _private-registry.com/myrepository/image:tag_
  _private-registry.com/myrepository/manufacturer/image:tag_
i felt its safer and industry stabdard to create a mechanics for building the image name.

As always, the defaut values defined in the defaults file
~~~yaml
---
default_registry: "private-registry.com/repository"

#image basics:
default_image: "myimage"
default_tag: "latest"
tlsverify: false

#manufacturer if needed like prom/prometheus:latest
manufacturer: "mymanufacturer"

#Default values variables for the pull/tasks/main.yaml mechanics
~~~

and the mechanics in the tasks file.
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

**Step 2: Composing and running the playbooks**

**Step 3: 

## Conclusion
Slutsats

## References
- [Dockerhub (public image repository](https://hub.docker.com/)
- [Ansible structure](https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/Ansible_structure.md)

### Other projects in our IT-infrastructure
1. [Proxmox_on_Nuc](https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc)
2. [Rocky_Linux_OS_Base_for_VMs](https://github.com/Filipanderssondev/Rocky_Linux_OS_Base_for_VMs)
3. [Ansible_on_management_vm](https://github.com/JonatanHogild/Ansible_on_management_vm)
4. [Podman_Compose_app_on_VMs](https://github.com/Filipanderssondev/Podman_Compose_app_on_VMs)


