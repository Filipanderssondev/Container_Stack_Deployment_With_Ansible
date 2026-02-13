~~~yaml
├── ansible.cfg
├── inventory
│   ├── group_vars
│   │   └── all
│   │       └── vault.yml
│   ├── hosts.ini
├── playbooks
│   ├── container_projects
│   │   ├── deploy_app.yaml
│   │   ├── deploy_node-exporter.yaml
│   │   ├── playbook_template.yaml
│   │   ├── pull_images.yaml
│   │   ├── pull_monitoring.yaml
│   │   ├── run_container_template.yaml
│   │   ├── run_grafana.yaml
│   │   ├── run_prometheus.yaml
│   └── standard_plays
│       ├── dnf_install_package.yml
│       ├── os_base.yml
│       └── update_dnf.yml
└── roles
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
    │   └── run
    │       ├── defaults
    │       │   └── main.yaml
    │       └── tasks
    │           └── main.yaml
~~~
