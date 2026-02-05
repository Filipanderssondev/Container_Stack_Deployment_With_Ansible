# Container_Stack_Deployment_With_Ansible 
<img width="100" alt="MyLogo" src="https://github.com/rafaelurrutiasilva/images/blob/main/logos/MyLogo_2.png" align=left><br>
<br>
**Container_Stack_Deployment_With_Ansible**<br>
<br>**Authors:** _<a href="https://github.com/Filipanderssondev">Filip Andersson</a> and <a href="https://github.com/JonatanHogild">Jonatan Högild</a>_<br>
Publiceringsdatum<br>

<br>

## Abstract
Container stack / application Deployment on virtual machines running Podman, through a control vm running ansible. Fourth project <a href="https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/blob/main/Extra/Mermaid/Projects.md">in a series of projects</a> during our internship at **The Swedish Meteorological and Hydrological Institute** [(SMHI)](https://www.smhi.se/en/about-smhi), Deploying an application with podman compose on an application vm we created. <br>
<br>

## Table of Contents

1. [Introduction](#introduction)
2. [Goals and Objectives](#goals-and-objectives)
3. [Method](#method)
4. [Target Audience](#target-audience)
5. [Document Status](#document-status)
6. [Disclaimer](#disclaimer)
7. [Scope and Limitations](#scope-and-limitations)
8. [Environment](#environment)
9. [Acknowledgments](#acknowledgments)
10. [References](#references)
11. [Conclusion](#conclusion)

## 1. Introduction<br>
**Welcome friend!**
_...to this project where i am going to do some container deployment through infrastructure-as-code (IaC) with Ansible. Im going to deploy an application / stack of containers on two worker VMs, the application VM will serve as our runtime enviroment and the metrics VM serving as our metrics collector / Monitoring for that app, running Prometheus and Grafana. I will run everything on the VM called management, that will serve as our control VM running Ansible. I will do this by configuring Ansible Roles, and using those ansible roles in playbooks. This is our fourth project <a href="https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/blob/main/Extra/Mermaid/Projects.md">in a series of projects</a> with the end goal of setting up a complete virtualized, automated, and monitored IT-Enviroment as a part of our internship on [The Swedish Meteorological and Hydrological Institute (SMHI)](https://www.smhi.se/en/about-smhi) IT-department at the headquarters in Norrköping. The second goal of these projects are also supposed to serve as a set-up guide here on Github for anyone and everyone that wants to replicate what we have done. we will link every project to each other aswell._<br>

**<a href="https://github.com/Filipanderssondev">Filip Andersson</a> and <a href="https://github.com/JonatanHogild">Jonatan Högild</a>**

## 2. Goals and Objectives
The goals and objectives of this project is: 
- 1. To run an application on the application VM, hosting it on port 8080
  2. Collect metrics from that app to the metrics VM, displaying it in Grafana.
  3. Doing it all through Ansible on the management VM
<br>
<br>

## 3. Method

### 3.1 Preparation 
- We have our earlier projects as a foundation, [a Server running Proxmox](https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/tree/) and proxmox running [three replicated virtual machines from a Rocky Linux OS base](https://github.com/Filipanderssondev/Rocky_Linux_OS_Base_for_VMs) and [Ansible configuration on the management vm](https://github.com/JonatanHogild/Ansible_on_management_vm)

### 3.2 Pre-experimention

- Before applying the same methods to the VM, we start by experimenting locally with diffrent parts of the project, in this perticular case i started experimenting on my own using nginx as an image and nginx-prometheus-exporter 

1. I start with reading company policy for the use of public images, i pull the images from dockerhub, scan them and make them okay for internal use
   
2. afterward, i compose a compose.yaml file to:

~~~yaml
version: "3.8"
services:
  image: "example.com/nginx:1.27-alpine"
    container_name: nginx_container
    ports:
      - "8080:8080"
    volumes:
      - /folder/folder/nginx.conf:/folder/nginx/conf.d/default.conf:Z

  nginx-prometheus-exporter:
    image: "example.com/nginx-prometheus-exporter:latest"
    container_name: nginx-prometheus-exporter_container
    ports:
        - "9113:9113"
    command: ["--nginx.scrape-uri", "http://nginx:8080/status"]
~~~
  
### 3.3 Installation & Configuration on VM
N/A

#### 3.3.1 Installing Podman on the Application VM with Ansible
N/A

#### 3.3.2 Deploying the application with compose.yaml
N/A
draft:
We discovered that since ansible is configured to run as root, the images i pulled with my ansible playbooks and the containers i run with ansible playbooks only show up when typing sudo podman images / sudo podman ps.

## 4. Target Audience
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

## References
- [Dockerhub (public image repository](https://hub.docker.com/)

### Our other projects
1. [Proxmox_on_Nuc](https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc)
2. [Rocky_Linux_OS_Base_for_VMs](https://github.com/Filipanderssondev/Rocky_Linux_OS_Base_for_VMs)
3. [Ansible_on_management_vm](https://github.com/JonatanHogild/Ansible_on_management_vm)
4. [Podman_Compose_app_on_VMs](https://github.com/Filipanderssondev/Podman_Compose_app_on_VMs)

## Conclusion
Slutsats
