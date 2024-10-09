from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery


QUERIES = (
    MIB_INDEX['SW-MIB']['swSystem'],
    MIB_INDEX['SW-MIB']['swFabric'],
    MIB_INDEX['SW-MIB']['swCpuOrMemoryUsage'],
    MIB_INDEX['SW-MIB']['swFCPortEntry'],
    MIB_INDEX['SW-MIB']['swSensorEntry'],
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
            'swNumSensors': item.get('swNumSensors'),
            'swTrackChangesInfo': item.get('swTrackChangesInfo'),
            'swID': item.get('swID'),
            'swEtherIPAddress': item.get('swEtherIPAddress'),
            'swEtherIPMask': item.get('swEtherIPMask'),
            'swFCIPAddress': item.get('swFCIPAddress'),
            'swIPv6Address': item.get('swIPv6Address'),
            'swIPv6Status': item.get('swIPv6Status'),
            'swModel': item.get('swModel'),
            'swTestString': item.get('swTestString'),
            'swPortList': item.get('swPortList'),
            'swBrcdTrapBitMask': item.get('swBrcdTrapBitMask'),
            'swFCPortPrevType': item.get('swFCPortPrevType'),
            'swDeviceStatus': item.get('swDeviceStatus'),
        }]

    sw_fabric = state.pop('swFabric', [])
    if len(sw_fabric):
        state['swFabric'] = sw_fabric
        # swFabric is one item

    sw_cpu_mem = state.pop('swCpuOrMemoryUsage', [])
    if len(sw_cpu_mem):
        state['swCpuOrMemoryUsage'] = sw_cpu_mem
        # swCpuOrMemoryUsage is one item

    return state
