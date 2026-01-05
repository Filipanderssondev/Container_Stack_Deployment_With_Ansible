```mermaid
flowchart TB
    A["Ansible"] --> B["Podman containers"] & C["Prometheus"] & D
    B --> C
    C --> D["Grafana"]
```
