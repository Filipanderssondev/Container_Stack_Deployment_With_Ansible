
```mermaid
  flowchart TD
 subgraph s1["Proxmox"]
        A["Master VM"] --> |ssh|B["App VM"] 
        A --> |ssh|C["Metrics VM"]
  end
```
