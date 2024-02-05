# YamlGridReader

# Usage
```python3
from YamlGridReader import YamlGridReader

d = {
    "k1": "v1",
    "k2": ["v2", "v3"],
    "k3": [1e-4, 1e-5]
}

grid = YamlGridReader.FromDict(
    d,
    ignore_list=["k2"]
)

# OR load from file
# grid = YamlGridReader.FromPath("/path/to/grid.yaml", ignore_list=["k2"])

for g in grid:
    print(g)
```
```bash
>>> {
    "k1": "v1",
    "k2": ["v2", "v3"],
    "k3": 1e-4
}
{
    "k1": "v1",
    "k2": ["v2", "v3"],
    "k3": 1e-5
}
```