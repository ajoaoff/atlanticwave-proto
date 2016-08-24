# Copyright 2016 - Sean Donovan
# AtlanticWave/SDX Project


# Unit tests for the SDXController class

import unittest
import threading
import networkx as nx
import mock

from shared.UserPolicy import *
from sdxctlr.BreakdownEngine import *
from sdxctlr.TopologyManager import TopologyManager
from sdxctlr.ParticipantManager import ParticipantManager
from sdxctlr.LocalControllerManager import LocalControllerManager
from sdxctlr.SDXController import *

TOPO_CONFIG_FILE = 'test_manifests/topo.manifest'
PART_CONFIG_FILE = 'test_manifests/participants.manifest'

class UserPolicyStandin(UserPolicy):
    # Use the username as a return value for checking validity.
    def __init__(self, username, json_rule):
        super(UserPolicyStandin, self).__init__(username, json_rule)
        self.valid = username
        self.breakdown = json_rule
        
    def check_validity(self, topology, authorization_func):
        # Verify that topology is a nx.Graph, and authorization_func is ???
        if not isinstance(topology, nx.Graph):
            raise Exception("Topology is not nx.Graph")
        if self.valid == True:
            return True
        raise Exception("NOT VALID")
    
    def breakdown_rule(self, topology, authorization_func):
        # Verify that topology is a nx.Graph, and authorization_func is ???
        if not isinstance(topology, nx.Graph):
            raise Exception("Topology is not nx.Graph")
        if self.breakdown == True:
            return [UserPolicyBreakdown("1.2.3.4", ["rule1", "rule2"])]
        raise Exception("NO BREAKDOWN")
    
    def _parse_json(self, json_rule):
        return


class SingletonTest(unittest.TestCase):
    @mock.patch('sdxctlr.SDXController.RestAPI', autospec=True)
    def test_singleton(self, restapi):
        part = ParticipantManager(PART_CONFIG_FILE)
        topo = TopologyManager(TOPO_CONFIG_FILE)
        lc = LocalControllerManager(TOPO_CONFIG_FILE)
        firstManager = SDXController()
        secondManager = SDXController()

        self.failUnless(firstManager is secondManager)

class AddRuleTest(unittest.TestCase):
    @mock.patch('sdxctlr.SDXController.RestAPI', autospec=True)
    def test_good_test_add_rule(self, restapi):

        part = ParticipantManager(PART_CONFIG_FILE)
        topo = TopologyManager(TOPO_CONFIG_FILE)
        lc = LocalControllerManager(TOPO_CONFIG_FILE)
        sdxctlr = SDXController()
        
        man = RuleManager()
        valid_rule = UserPolicyStandin(True, True)

        self.failUnlessRaises(SDXControllerConnectionError,
                              man.add_rule, valid_rule)




                
if __name__ == '__main__':
    unittest.main()
