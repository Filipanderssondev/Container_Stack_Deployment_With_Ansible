~~~yaml
ansible
├── ansible.cfg
├── files
│   ├── grafana
│   │   ├── dashboards
│   │   │   ├── applications
│   │   │       └── container-health.json
│   │   └── provisioning
│   │       ├── dashboards
│   │       │   └── dashboards.yml
│   │       └── datasources
│   │           └── datasource.yml
│   └── prometheus
│       └── prometheus.yml
├── inventory
│   ├── group_vars
│   │   └── all
│   │       └── vault.yml
│   └── hosts.ini
├── playbooks
│   ├── application
│   │   ├── deploy_app.yaml
│   │   ├── deploy_frontend.yaml
│   │   ├── kill_applications.yaml
│   │   ├── kill_backend.yaml
│   │   ├── kill_frontend.yaml
│   ├── monitoring
│   │   ├── deploy_grafana.yaml
│   │   ├── deploy_monitoring.yaml
│   │   ├── deploy_node-exporter.yaml
│   │   ├── deploy_podman-exporter.yaml
│   │   ├── deploy_prometheus.yaml
│   │   ├── kill_grafana.yaml
│   │   ├── kill_monitoring.yaml
│   │   ├── kill_node-exporter.yaml
│   │   ├── kill_podman-exporter.yaml
│   │   └── pull_monitoring.yaml
│   └── standard_plays
│       ├── dnf_install_package.yml
│       ├── os_base.yml
│       ├── pull_images.yaml
│       └── update_dnf.yml
└── roles
    └── containers
        ├── images
        │   └── pull
        │       ├── defaults
        │       │   └── main.yaml
        │       └── tasks
        │           └── main.yaml
        ├── install
        │   └── tasks
        │       └── main.yaml
        ├── login
        │   └── filip
        │       ├── defaults
        │       │   └── main.yaml
        │       └── tasks
        │           └── main.yaml
        └── run
            ├── defaults
            │   └── main.yaml
            └── tasks
                └── main.yaml
~~~
