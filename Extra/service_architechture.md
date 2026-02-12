```mermaid
flowchart TB
    A["Ansible"] --> |ssh|B["Podman containers"] & C["Prometheus"] & D
    B --> |ssh|C
    C --> |ssh| D["Grafana"]
```
