
```mermaid
  flowchart TD
 subgraph s1["Proxmox"]
        A["Master VM"] --> B["App VM"] 
        A --> C["Metrics VM"]
  end
```
