from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..utils import get_data

QUERIES = (
    MIB_INDEX['SW-MIB']['swCpuOrMemoryUsage'],
    MIB_INDEX['SW-MIB']['swFCPortEntry'],
    MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortStatusEntry'],
    MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortPhysEntry'],
)


async def check_brocade(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    state = await get_data(asset, asset_config, check_config, QUERIES)
    return state
