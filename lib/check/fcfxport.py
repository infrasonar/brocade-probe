from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery


QUERIES = (
    (MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortEntry'], True),
    (MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortStatusEntry'], True),
    (MIB_INDEX['FIBRE-CHANNEL-FE-MIB']['fcFxPortPhysEntry'], True),
)


class CheckFcFxPort(Check):
    key = 'fcfxport'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        port_status = {
            item['name']: item for item in state.pop('fcFxPortStatusEntry', [])
        }
        port_phys = {
            item['name']: item for item in state.pop('fcFxPortPhysEntry', [])
        }

        # fcFxPortStatus, fcFxPortPhysEntry can be merged, they share the same
        # index oid (-> name). This is indicated by the AUGMENTS clause in the
        # mib.
        for item in state.get('fcFxPortEntry', []):
            name = item['name']
            port_status_item = port_status.get(name)
            if port_status_item:
                item.update(port_status_item)
            port_phys_item = port_phys.get(name)
            if port_phys_item:
                item.update(port_phys_item)
        return state
