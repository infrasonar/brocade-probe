from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery


QUERIES = (
    MIB_INDEX['SW-MIB']['swSystem'],
    MIB_INDEX['SW-MIB']['swFabric'],
    MIB_INDEX['SW-MIB']['swCpuOrMemoryUsage'],
    MIB_INDEX['SW-MIB']['swFCPortEntry'],
    MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortStatusEntry'],
    MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortPhysEntry'],
)


async def check_brocade(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)

    sw_system = state.pop('swSystem', [])
    if len(sw_system):
        item = sw_system[0]  # swSystem is one item
        state['swSystem'] = [{
            'name': 'brocade',
            'swCurrentDate': item.get('swCurrentDate'),
            'swBootDate': item.get('swBootDate'),
            'swFWLastUpdated': item.get('swFWLastUpdated'),
            'swFlashLastUpdated': item.get('swFlashLastUpdated'),
            'swBootPromLastUpdated': item.get('swBootPromLastUpdated'),
            'swFirmwareVersion': item.get('swFirmwareVersion'),
            'swOperStatus': item.get('swOperStatus'),
            'swAdmStatus': item.get('swAdmStatus'),
            'swTelnetShellAdmStatus': item.get('swTelnetShellAdmStatus'),
            'swSsn': item.get('swSsn'),
            'swFlashDLOperStatus': item.get('swFlashDLOperStatus'),
            'swFlashDLAdmStatus': item.get('swFlashDLAdmStatus'),
            'swBeaconOperStatus': item.get('swBeaconOperStatus'),
            'swBeaconAdmStatus': item.get('swBeaconAdmStatus'),
            'swDiagResult': item.get('swDiagResult'),
        }]

    sw_fabric = state.pop('swFabric', [])
    if len(sw_fabric):
        state['swFabric'] = sw_fabric
        # swFabric is one item

    sw_cpu_mem = state.pop('swCpuOrMemoryUsage', [])
    if len(sw_cpu_mem):
        state['swCpuOrMemoryUsage'] = sw_cpu_mem
        # swCpuOrMemoryUsage is one item

    port_status = {
        item['name']: item for item in state.pop('fcFxPortStatusEntry', [])
    }
    port_phys = {
        item['name']: item for item in state.pop('fcFxPortPhysEntry', [])
    }
    for item in state.get('swFCPortEntry', []):
        name = item['name']
        port_status_item = port_status.get(name)
        if port_status_item:
            item.update(port_status_item)
        port_phys_item = port_phys.get(name)
        if port_phys_item:
            item.update(port_phys_item)
    return state
