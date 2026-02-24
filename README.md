# Container Stack Deployment With Ansible 
<!--
<img width="200" src="https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/container-stack-deployment.png" allign="left"> **Container Stack Deployment With Ansible** <br>
**Authors:** _<a href="https://github.com/Filipanderssondev">Filip Andersson</a> and <a href="https://github.com/JonatanHogild">Jonatan Högild</a>_ <br>
24-02-2026 <br clear="left"/>
-->

<div>
  <img src="https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/blob/main/Extra/container-stack-deployment.png" width="300" align="left" />

  <p style="margin-top: 1000px;">
    <strong>Container Stack Deployment With Ansible</strong>
	<br>
    <strong>Authors:</strong>
    <i><a href="https://github.com/Filipanderssondev">Filip Andersson</a></i>
    and
    <i><a href="https://github.com/JonatanHogild">Jonatan Högild</a></i>
    <br>
    24-02-2026
    <br clear="left"/>
  </p>
</div>

## Abstract
Container stack application Deployment and monitoring on virtual machines running Podman, Managed by Ansible.
<br>

## Table of Contents

1. [Introduction](#introduction)
2. [Goals and Objectives](#goals-and-objectives) <br>
3. [Method](#method)
4. [Target Audience](#target-audience)
5. [Document Status](#document-status)
6. [Disclaimer](#disclaimer)
7. [Scope and Limitations](#scope-and-limitations)
8. [Environment](#environment)
9. [Acknowledgments](#acknowledgments)
10. [Implementation](#implementation) <br>
    	10.1 [Creating the Ansible roles](#creating-the-ansible-roles) <br>
    	10.2 [Composing and running the playbooks](#composing-and-running-the-playbooks) <br>
11. [Conclusion](#conclusion)
12. [References](#references) <br>
    12.1 [Other projects in our virtual IT-enviroment](#other-projects-in-our-virtual-it-enviroment)
<br>

## Introduction<br>
**Welcome friend!** <br>
_In this project we are going to deploy a container-based interactive web application using infrastructure-as-code (IaC), Ansible. We will deploy the fullstack containers on our application VM that will serve as our runtime enviroment and the monitoring containers on our metrics VM serving as our metrics collector. Everything will be managed from our management VM running Ansible. This will be done by configuring Ansible roles, and reusing those roles in playbooks. This is our fourth project <a href="https://github.com/rafaelurrutiasilva/Proxmox_on_Nuc/blob/main/Extra/Mermaid/Projects.md">in a series of projects</a> with the end goal of setting up a complete virtualized, automated, and monitored IT-Enviroment as a part of our internship on [The Swedish Meteorological and Hydrological Institute (SMHI)](https://www.smhi.se/en/about-smhi) IT-department at the headquarters in Norrköping. The second goal of these projects are also supposed to serve as a set-up guide here on Github for anyone and everyone that wants to replicate what we have done. we will link every project to each other aswell._ <br>

_[Other projects in our virtual IT-enviroment](#other-projects-in-our-virtual-it-enviroment)_

## Goals and Objectives
The goals and objectives of this project is: 
- To run a container-based web application / full stack, with log in, displaying multiple interactive pages.
- Collect metrics from that app to the metrics VM, displaying it in Grafana.
- Doing it all through Ansible on the management VM
<br>
This is part of a larger ongoing Infrastructure as Code (IaC) project that will use Proxmox as a base, with Rocky Linux as the OS running on each virtual machine. The goal of this project is to build a complete IT-environment and gain a deeper understanding of the underlying components and their part in a larger production chain.

## Method

The solution was implemented using Ansible on a management virtual machine to automate the deployment of a container-based web application and monitoring on virtual on two machines running Podman. The container stack consisted of NGINX (frontend) that served visual presentation, Postgres (Database) for storing users and logging in, and Rocky linux based python api (Backend) as our backend api handling http requests and responses. To be able to serve multiple pages in the same window, a custom Cross-Origin-Resource-Sharing (CORS) function was created inside the backend api, since the inviroment is designed like most modern enterprises with restrictive access to the internet the containers couldn't be reliant on external python libraries and packages websites, instead a custom Rocky Linux based image was constructed using dnf as package handler, with access to internal package repositorys. The stack also consist of monitoring using container based Prometheus node exporters on each vm for exporting metrics configuring prometheus to collect metrics from the node exporters and prometheus as a data source for Grafana to visualize the result. Reusable Ansible roles and playbooks were used to install dependencies, pull images from a private image reg start containers with defined ports and volumes. To collect the container images from the private image registry, an ansible login role was composed and implemented with the mechanics of fetching confidential login credentials defined in the encrypted vault file in our ansible structure.

## Target Audience
- This repo is for anyone who wants a step-by-step guide on how to deploy a modern container stack based application and monitoring stack with Ansible.
This repo is also part of a larger project aimed at people interested in learning about IT-infrastructure, and building such an environment from scratch. 
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
1
## Acknowledgments
Great thanks once again to our mentor [Rafael](https://github.com/rafaelurrutiasilva) for ongoing support and guidance. And thanks to [Victor](https://github.com/ludd98) for insight and guidance. 

## Implementation

- Note, that some details cant be disclosed due to company policy and that i will speak in general terms. For example the registry i will pull images from i will call _"private-registry.com/repository"_
<br

Every config file is available under the [code directory](https://github.com/Filipanderssondev/Container_Stack_Deployment_With_Ansible/tree/main/Code/ansible)

### Configuring reusable roles

What we want is resuable roles for repetetive tasks. We want a role for checking/installing latest versions of depencencies like Podman, we want a role that logs in to our private registry fetching our credentials from our encrypted vault file, We want a role for pulling images, and we want a role for running images acting as the whole container logic, our "engine" if you will. Each role will have a defaults folder with a main.yaml file and a tasks folder with a main.yaml file. All variables will be pre defined in our defaults/main as a standard fallback as is the best practice to never hardcode anything. Each tasks/main will contain the modules and define the logic for the tasks. Then, we want a role that shows running containers and a role for killing and removing containers, because it is quite a process to do manually for each container when we want to test our containers and such.

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

##### defaults/main.yaml

As the registry URL isnt as sensitive information as our                                   
user credentials, its generally considered best practice to define it in our defaults and not our encrypted vault file

Out of necesity we to have the tls verify set to false, we ran into a lot of complications with certificate authentication on the vms so it is easier to do it like this so it dosent fail.
~~~yaml
---
#Default image registry
registry_url: "www.private-container-registry.com/myrepository"  # Dummy value for demostration purpose
tlsverify: tls-verify=false
~~~

##### tasks/main.yaml
This is the logic for logging us in, using the module _containers.podman.podman_login_. Here im referring to the variables defined in our encrypted vault file.

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
Its safer to create a mechanics for building the complete image name. Defining our default values in defaults and then overriding in pur playbooks, never hardcoding anything. 

##### defaults/main.yaml
~~~yaml
---
default_registry: "private-registry.com/repository"

#image basics:
default_image: "myimage"
default_tag: "latest"
tlsverify: false
~~~

##### tasks/main.yaml
This is the mechanics for the image name builder, since we often want to pull multiple images we want to treat each image as an item in a list we overrode in our define in our playbook. This task runs once per item, tach image is treated as an item in a list, it builds the full image name (registry, optional manufacturer, image name, and version tag).
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

#### Container run role

##### defaults/main.yaml
~~~yaml
---
#Default value for variables, whats the image to run + name of new container

# Default container registry
default_registry: "private-registry.com"
default_project: "project"
manufacturer: " "
image_name: my-image
tag: "latest"
container_name: my-container

#Desired container state / absent
container_state: started

#Additional settings for later
container_ports: []
container_env_vars: {}
container_volumes: []
container_restart_policy: always
container_cmd: []
container_network: " "
tls_verification: false
~~~

##### tasks/main.yaml
~~~yaml
---
- name: Run container
  containers.podman.podman_container:
    name: "{{ container_name }}"
    image: "{{ default_registry }}/{{ default_project }}{% if manufacturer is defined and manufacturer | trim != '' %}/{{ manufacturer }}{% endif %}/{{ image_name }}:{{ tag }}"
    state: "{{ container_state  }}"
    ports: "{{ container_ports | default(omit)  }}"
    env: "{{ container_env_vars  }}"
    volumes: "{{ container_volumes | default(omit) }}"
    restart_policy: "{{ container_restart_policy | default('always') }}"
    user: 0
    command: "{{ container_cmd | default([]) }}"
    tls_verify: "{{ tls_verification | default }}"
    network: "{{ container_network | default(omit) }}"
~~~


#### Show containers

This role is very simple so we dont need default values per say so we only go with tasks for this one.

##### tasks/main.yaml
~~~yaml
---
- name: Get all container names
  command: sudo podman ps -a --format "{{'{{'}}.Names{{'}}'}}"
  register: container_names
  changed_when: false

- name: Show container names
  debug:
    msg: "Container found: {{ item }}"
  loop: "{{ container_names.stdout_lines }}"
  when: container_names.stdout != ""

~~~

#### Container kill role

Since the kill role is partially off the show role but with some tweaks its redundant to use defaults here aswell.

##### tasks/main.yaml
~~~yaml
---
- name: Get all container names
  command: podman ps -a --format "{{'{{'}}.Names{{'}}'}}"
  register: container_names
  changed_when: false

- name: Show container names
  debug:
    msg: "Container found: {{ item }}"
  loop: "{{ container_names.stdout_lines }}"
  when: container_names.stdout != ""

- name: Stop all containers
  command: podman stop {{ item }}
  loop: "{{ container_names.stdout_lines }}"
  ignore_errors: true
  when: container_names.stdout != ""

- name: Remove all containers
  command: podman rm -f {{ item }}
  loop: "{{ container_names.stdout_lines }}"
  ignore_errors: true
  when: container_names.stdout != ""
~~~

<br>

### The stack

What we want is to be able to log into our container based website, and we want our frontend to display something that speaks for what this is about with multiple pages, in this case we want it to speak about that this is our intern project at SMHI and a some information on our enviroment with diagrams. 

#### Structure
On the application vm
```bash
└── app-praktik-projekt
    ├── backend
    │   ├── app.py
    │   ├── dnf-repos
    │   │   └── yum.repos.d
    │   │       ├── epel.repo
    │   │       ├── rocky-extras.repo
    │   │       └── rocky.repo
    │   └── Dockerfile
    ├── db
    │   └── init.sql
    └── frontend
        ├── about.html
        ├── diagram.html
        ├── diagram.png
        ├── index.html
        ├── script.js
        └── style.css
```

##### index.HTML
```html
<!DOCTYPE html>
<html>
<head>
  <title>SMHI Praktikprojekt</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="card">
    <h1>SMHI Praktikprojekt</h1>
    <p class="subtitle">Enter the system</p>

    <input id="username" placeholder="Username">
    <button onclick="login()">ENTER</button>
  </div>

  <script src="script.js"></script>
</body>
</html>
```

##### about.html
```html
<!DOCTYPE html>
<html>
<head>
  <title>About</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="card">
    <h1 id="welcome"></h1>
    <p>This system is deployed using containers, Ansible and Podman.</p>
    <button onclick="goDiagram()">VIEW ARCHITECTURE</button>
  </div>

  <script src="script.js"></script>
</body>
</html>

```

##### diagram.html
This page will serve our flowchart diagram.
```html
<!DOCTYPE html>
<html>
<head>
  <title>Architecture</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="card">
    <h1>ARCHITECTURE</h1>
    <img src="diagram.png" class="diagram">
    <button onclick="goBack()">BACK</button>
  </div>

  <script src="script.js"></script>
</body>
</html>

```

#### style.CSS
```css
body {
  margin: 0;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

  font-family: 'Segoe UI', sans-serif;
  color: white;

  background: radial-gradient(circle at top left, #1f1f1f, #000000);
  animation: fadeIn 1.2s ease-in;
}

.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 50px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 0 40px rgba(255,255,255,0.1);
  width: 400px;
}

h1 {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: 2px;
  margin-bottom: 10px;
}

.subtitle {
  opacity: 0.6;
  margin-bottom: 30px;
}

input {
  width: 100%;
  padding: 14px;
  margin-bottom: 20px;
  border: none;
  border-radius: 8px;
  background: #111;
  color: white;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  background: white;
  color: black;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #00ffcc;
  box-shadow: 0 0 20px #00ffcc;
  transform: translateY(-2px);
}

.diagram {
  max-width: 100%;
  margin: 20px 0;
  border-radius: 10px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

#### script.js
This is the javascript that makes our web application interactive and will call our backend api
```javascript
const api = "http://" + window.location.hostname + ":5000";

function login() {
  const username = document.getElementById("username").value;

  fetch(api + "/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username })
  })
  .then(() => {
    localStorage.setItem("user", username);
    window.location.href = "about.html";
  });
}

window.onload = function () {
  const welcome = document.getElementById("welcome");
  if (welcome) {
    const user = localStorage.getItem("user");
    welcome.textContent = "WELCOME, " + user.toUpperCase();
  }
};

function goDiagram() {
  window.location.href = "diagram.html";
}

function goBack() {
  window.location.href = "about.html";
}
```
### Backend and DB

#### Backend

Since we designed our system like an enterprise enviroment with limited access towards the internet, we could not be depended on external python libraries for our images to work. This is why we based our python backend container off of Rocky Linux because we already have access to internal package repositorys using dnf. We had access to _python3-flask_ but not the _python3-cors_ dependency, making the display of multiple web pages in the same window possible so we had to construct our own Cross-Origin-Resource_Sharing (CORS) in app.py under _def login()_ 

##### app.py
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        response = app.make_response("")
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    data = request.json
    username = data.get("username")
    response = jsonify({"message": f"Welcome {username}!"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

##### Dockerfile
And our Dockerfile for building the backend image, with Rocky Linux as a base image. We used the dnf repo configs from the vm and copied it to the container. 
```Dockerfile
FROM private-registry.com/repository/rockylinux:10-ubi-init

COPY dnf-repos/yum.repos.d /etc/yum.repos.d

RUN dnf install -y \
    python3 \
    python3-flask \
    python3-psycopg2 \
    python3-dotenv \
    && dnf clean all

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
```

#### Database



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



