import logging

from ..addressable import AddressableDict
from ..elements.generic_status import GenericStatus
from ..elements.generic_capability import GenericCapability

LOG = logging.getLogger("weconnect")


class CapabilityStatus(GenericStatus):
    def __init__(
        self,
        vehicle,
        parent,
        statusId,
        fromDict=None,
        fixAPI=True,
    ):
        self.capabilities = AddressableDict(localAddress='capabilities', parent=self)
        super().__init__(vehicle=vehicle, parent=parent, statusId=statusId, fromDict=fromDict, fixAPI=fixAPI)

    def update(self, fromDict, ignoreAttributes=None):
        ignoreAttributes = ignoreAttributes or []
        LOG.debug('Update capability status from dict')

        if 'capabilities' in fromDict and fromDict['capabilities'] is not None:
            for capDict in fromDict['capabilities']:
                if 'id' in capDict:
                    if capDict['id'] in self.capabilities:
                        self.capabilities[capDict['id']].update(fromDict=capDict)
                    else:
                        self.capabilities[capDict['id']] = GenericCapability(
                            capabilityId=capDict['id'], fromDict=capDict, parent=self.capabilities)
            for capabilityId in [capabilityId for capabilityId in self.capabilities.keys()
                                 if capabilityId not in [capability['id']
                                 for capability in fromDict['capabilities'] if 'id' in capability]]:
                del self.capabilities[capabilityId]
        else:
            self.capabilities.clear()
            self.capabilities.enabled = False

        super().update(fromDict=fromDict, ignoreAttributes=(ignoreAttributes + ['capabilities']))

    def __str__(self):
        string = super().__str__()
        string += f'\n\tCapabilities: {len(self.capabilities)} items'
        for capability in self.capabilities.values():
            string += f'\n\t\t{capability}'
        return string
