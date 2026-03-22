# func_adl_local

Run [FuncADL](https://github.com/iris-hep/func_adl) queries on local files without ServiceX.

[FuncADL](https://github.com/iris-hep/func_adl) (Functional Analysis Description Language) is a declarative query language for HEP data analysis. Normally it is used with [ServiceX](https://github.com/ssl-hep/ServiceX) to query remote datasets. `func_adl_local` brings that same interface to files on your local machine — no ServiceX deployment required.

## Installation

```bash
pip install func_adl_local
```

## Usage

### xAOD files

Use `xAODConfig` to configure the ATLAS release and runtime platform, then call `get_data` with your dataset path and FuncADL query:

```python
from func_adl_local import xAODConfig, get_data

config = xAODConfig(
    release=22,        # ATLAS release: 21, 22, or 25
    platform="docker", # "docker", "singularity", or "wsl2"
)

# Build a query using the release-appropriate FuncADL dataset type
query = config.FuncADLQueryPHYS().SelectMany(lambda e: e.Jets("AntiKt4EMTopoJets")).Select(
    lambda j: {"pt": j.pt(), "eta": j.eta()}
)

result = get_data("path/to/file.root", query, config)
```

To get the result as an [awkward-array](https://awkward-array.org/), set `awk=True`:

```python
config = xAODConfig(release=22, awk=True)
result = get_data("path/to/file.root", query, config)
# result is now an awkward array
```

**Available query types:**

| Method | Releases |
|---|---|
| `config.FuncADLQueryPHYS()` | 21, 22, 25 |
| `config.FuncADLQueryPHYSLITE()` | 22, 25 |

**Platforms:**

| Value | Description |
|---|---|
| `"docker"` | Run the transformer in Docker (default) |
| `"singularity"` | Run in Singularity/Apptainer |
| `"wsl2"` | Run in WSL2 |

**Docker image versions:**

`xAODConfig` automatically selects the latest image for the chosen release. You can inspect available versions or pin to a specific one:

```python
config = xAODConfig(release=22)
print(config.available_versions)   # all available tags
print(config.latest_r22_version)   # e.g. "22.2.110"

config_pinned = xAODConfig(release=22, version="22.2.107")
```

### Uproot / columnar files

For ROOT files and other columnar formats, use the re-exported `UprootDataset` from [func_adl_uproot](https://github.com/iris-hep/func_adl_uproot):

```python
from func_adl_local import UprootDataset

ds = UprootDataset("path/to/file.root", "treename")
result = ds.Select(lambda e: {"pt": e["pt"]}).AsAwkwardArray().value()
```

## API Reference

### `xAODConfig`

```python
@dataclass
class xAODConfig:
    release: int = 21           # ATLAS release year: 21, 22, or 25
    version: str = "latest"     # Docker image tag, or "latest" to auto-select
    platform: str = "docker"    # "docker", "singularity", or "wsl2"
    ignore_cache: bool = False  # Bypass the local ServiceX cache
    awk: bool = False           # Return results as awkward arrays
```

### `get_data(ds_name, query, config)`

Runs a FuncADL query against a local xAOD file.

- `ds_name` — path to the local dataset
- `query` — a FuncADL `ObjectStream` built from `config.FuncADLQueryPHYS()` or `config.FuncADLQueryPHYSLITE()`
- `config` — an `xAODConfig` instance

Returns a dict of arrays (or an awkward array if `config.awk=True`).

## Related Projects

- [func_adl](https://github.com/iris-hep/func_adl) — core FuncADL library
- [func_adl_uproot](https://github.com/iris-hep/func_adl_uproot) — Uproot backend for FuncADL
- [servicex_local](https://github.com/iris-hep/servicex_local) — local ServiceX runtime
- [ServiceX](https://github.com/ssl-hep/ServiceX) — remote data delivery service
- [func_adl_servicex](https://github.com/iris-hep/func_adl_servicex) — FuncADL ServiceX backend

## Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/RogerJanusiak/func_adl_local).

## License

MIT License
