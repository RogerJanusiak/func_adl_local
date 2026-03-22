import importlib
import json
import urllib.request
from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from func_adl import ObjectStream
from servicex import deliver
from servicex.databinder_models import Sample, ServiceXSpec
from servicex_analysis_utils import to_awk

from enum import Enum


class Platform(Enum):
    """Options for which platform to use for the runtime environment."""

    docker = "docker"
    singularity = "singularity"
    wsl2 = "wsl2"

if TYPE_CHECKING:
    from func_adl_servicex_xaodr21.sx_dataset import FuncADLQueryPHYS as _PHYS21
    from func_adl_servicex_xaodr22.sx_dataset import FuncADLQueryPHYS as _PHYS22
    from func_adl_servicex_xaodr22.sx_dataset import FuncADLQueryPHYSLITE as _PHYSLITE22
    from func_adl_servicex_xaodr25.sx_dataset import FuncADLQueryPHYS as _PHYS25
    from func_adl_servicex_xaodr25.sx_dataset import FuncADLQueryPHYSLITE as _PHYSLITE25

_DOCKER_IMAGE = "sslhep/servicex_func_adl_xaod_transformer"


_VALID_RELEASES = (21, 22, 25)


@dataclass
class xAODConfig:
    """Configuration for xAOD datasets."""

    release: int = 21
    version: str = "latest"
    platform: Union[Platform, str] = "docker"
    ignore_cache: bool = False

    def __post_init__(self):
        if self.release not in _VALID_RELEASES:
            raise ValueError(f"release must be one of {_VALID_RELEASES}, got {self.release}")
        if self.version == "latest":
            self.version = self._latest_for_release(self.release)
        if isinstance(self.platform, str):
            self.platform = Platform[self.platform]

    def _latest_for_release(self, release: int) -> str:
        versions = [t for t in self.available_versions if t.startswith(f"{release}.")]
        if not versions:
            raise ValueError(f"No versions found for release {release}")
        return max(versions, key=lambda t: tuple(int(x) for x in t.split(".")))

    @property
    def available_versions(self) -> list[str]:
        """Return available versions (21.x, 22.x, 25.x) of the xAOD transformer Docker image."""
        tags = []
        url = f"https://hub.docker.com/v2/repositories/{_DOCKER_IMAGE}/tags?page_size=100"
        while url:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
            tags.extend(result["name"] for result in data["results"])
            url = data.get("next")
        return [t for t in tags if t.startswith(("21.", "22.", "25."))]

    @property
    def latest_r21_version(self) -> str:
        """Return the latest 21.x version of the xAOD transformer Docker image."""
        return self._latest_for_release(21)

    @property
    def latest_r22_version(self) -> str:
        """Return the latest 22.x version of the xAOD transformer Docker image."""
        return self._latest_for_release(22)

    @property
    def latest_r25_version(self) -> str:
        """Return the latest 25.x version of the xAOD transformer Docker image."""
        return self._latest_for_release(25)

    def _release_module(self):
        return importlib.import_module(f"func_adl_servicex_xaodr{self.release}")

    def FuncADLQueryPHYS(self) -> "Union[_PHYS21, _PHYS22, _PHYS25]":
        return self._release_module().FuncADLQueryPHYS()

    def FuncADLQueryPHYSLITE(self) -> "Union[_PHYSLITE22, _PHYSLITE25]":
        return self._release_module().FuncADLQueryPHYSLITE()


def build_sx_spec(query, ds_name: str, config: xAODConfig):
    """Build a ServiceX spec from the given query and dataset."""
    from servicex_local.utils import find_dataset, install_sx_local
    from servicex_local.utils import Platform as _SxPlatform

    dataset, use_local = find_dataset(ds_name, prefer_local=True)

    if not use_local:
        raise ValueError(f"Unable to run dataset {ds_name} locally.")

    image = f"docker://{_DOCKER_IMAGE}:{config.version}"
    sx_platform = _SxPlatform(config.platform.value)
    codegen_name, adaptor = install_sx_local(image, sx_platform)
    backend_name = "local"

    spec = ServiceXSpec(
        Sample=[
            Sample(
                Name="MySample",
                Dataset=dataset,
                Query=query,
                Codegen=codegen_name,
            ),
        ],
    )

    return spec, backend_name, adaptor


def get_data(
    ds_name: str,
    query: ObjectStream,
    config: xAODConfig,
):
    """Run a query against a dataset, either locally or remotely."""
    from servicex_local.deliver import deliver as local_deliver

    spec, backend_name, adaptor = build_sx_spec(query, ds_name, config)

    sx_result = local_deliver(
        spec, adaptor=adaptor, ignore_local_cache=config.ignore_cache
    )

    return to_awk(sx_result)["MySample"]
