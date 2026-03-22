# func_adl_local — run FuncADL queries on local files without ServiceX

__version__ = "0.1.0"

# Allow function from UprootTo be used without importing the module
from func_adl_uproot import UprootDataset

from .functions import xAODConfig, get_data