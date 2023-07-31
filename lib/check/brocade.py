from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpquery import snmpquery

QUERIES = (
    MIB_INDEX['FOUNDRY-BFD-STD-MIB']['bfdSessEntry'],
    MIB_INDEX['FOUNDRY-SN-AGENT-MIB']['snAgentCpuUtilEntry'],
    MIB_INDEX['FOUNDRY-SN-AGENT-MIB']['snAgentGbl'],
    MIB_INDEX['FOUNDRY-SN-AGENT-MIB']['snAgentTempEntry'],
    MIB_INDEX['FOUNDRY-SN-AGENT-MIB']['snChasFanEntry'],
    MIB_INDEX['FOUNDRY-SN-AGENT-MIB']['snChasPwrSupplyEntry'],
    MIB_INDEX['FOUNDRY-SN-BGP4-GROUP-MIB']['snBgp4NeighborSummaryEntry'],
)


async def check_brocade(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    state = await snmpquery(asset, asset_config, check_config, QUERIES)
    return state
