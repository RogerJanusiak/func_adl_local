# FuncADL Local

Sometimes users would like to use FuncADL on local files without the use of ServiceX. This is the package for you!

`func_adl_local` allows you to run [FuncADL](https://github.com/iris-hep/func_adl) queries directly on local files using either the **xAOD** or **Uproot** backends — no ServiceX required.

## Overview

[FuncADL](https://github.com/iris-hep/func_adl) (Functional Analysis Description Language) is a declarative query language for HEP data analysis. Normally it is used in conjunction with [ServiceX](https://github.com/ssl-hep/ServiceX) to run queries on remote datasets. `func_adl_local` brings that same interface to files on your local machine.

## Features

- Run FuncADL queries on local files without ServiceX
- Supports xAOD files via the xAOD backend
- Supports ROOT and other columnar formats via the Uproot backend

## Installation

```bash
pip install func_adl_local
```

## Docs

The documentation for this package is hosted [here](https://tryservicex.org)

## Related Projects

- [func_adl](https://github.com/iris-hep/func_adl) — the core FuncADL library
- [ServiceX](https://github.com/ssl-hep/ServiceX) — remote data delivery service
- [func_adl_servicex](https://github.com/iris-hep/func_adl_servicex) — FuncADL ServiceX backend

## Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/RogerJanusiak/func_adl_local).

## License

MIT License
