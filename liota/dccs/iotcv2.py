# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
#  Copyright © 2015-2016 VMware, Inc. All Rights Reserved.                    #
#                                                                             #
#  Licensed under the BSD 2-Clause License (the “License”); you may not use   #
#  this file except in compliance with the License.                           #
#                                                                             #
#  The BSD 2-Clause License                                                   #
#                                                                             #
#  Redistribution and use in source and binary forms, with or without         #
#  modification, are permitted provided that the following conditions are met:#
#                                                                             #
#  - Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                  #
#                                                                             #
#  - Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"#
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  #
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE #
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  #
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR        #
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF       #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS   #
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN    #
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)    #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF     #
#  THE POSSIBILITY OF SUCH DAMAGE.                                            #
# ----------------------------------------------------------------------------#

import json
import logging
import time
import threading
import ConfigParser
import os
import Queue
from time import gmtime, strftime
from threading import Lock

from liota.dccs.dcc import DataCenterComponent, RegistrationFailure
from liota.lib.protocols.helix_protocol import HelixProtocol
from liota.entities.metrics.metric import Metric
from liota.lib.utilities.utility import LiotaConfigPath, getUTCmillis, mkdir, read_liota_config
from liota.lib.utilities.si_unit import parse_unit
from liota.entities.metrics.registered_metric import RegisteredMetric
from liota.entities.registered_entity import RegisteredEntity

log = logging.getLogger(__name__)


class Iotcv2(DataCenterComponent):
    """ The implementation of VMware IoTC V2 Data Center Component

    """

    def __init__(self, con):
        log.info("Logging into IOTC V2 DCC")
        self.comms = con
        self.counter = 0

    def register(self, entity_obj):
        log.info("Registering resource with IoTCV2 {0}".format(entity_obj.name))
        self.comms.send(json.dumps(self._commo_req(
                self.next_id(),
                entity_obj.entity_id,
                entity_obj.name,
                entity_obj.entity_type
        )))
        return RegisteredEntity(entity_obj, self, entity_obj.entity_id)

    def create_relationship(self, reg_entity_parent, reg_entity_child):
        pass

    def _format_data(self, reg_metric):
        pass

    def set_properties(self, reg_entity, properties):
        pass

    def unregister(self, entity_obj):
        pass

    def _commo_req(self, operation_id, uuid, mo_name, mo_type):
        return {
            "type": "createOrModifyMO_req",
            "source": "null",
            "portalTopic": "createOrModifyMO_req",
            "destination": "MODB",
            "operationID": operation_id,
            "MOFields": {
                "parent": "null",
                "children": [],
                "uuid": uuid,
                "MOType": mo_type,
                "name": mo_name,
                "properties": {
                    "foo": "bar"
                }
            }
        }

    def next_id(self):
        self.counter = (self.counter + 1) & 0xffffff
        # Enforce even IDs
        return int(self.counter * 2)
