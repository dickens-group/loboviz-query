#!/usr/bin/env python3

import json

class Node(object):
    '''
    nodes have an id, a number, a name, valid measurement groups, coordinate/location, and possible hardware/platfor
    but this could be more related to valid measurement groups
    "IRL-LP" : {"serial_number" : 35, "name" : "Indian River Lagoon - Link Port", "valid_measurements" : ["weather","water"], "coordinates" : { "lat" : -80.343113,"long" : 27.534830,"alt" : 0}},
    '''
    def __init__(self, id, node_json_data):
        self.id = id
        self.serial_number = node_json_data['serial_number']
        self.name = node_json_data['name']
        self.name = node_json_data['name']
        self.valid_measurements = node_json_data['valid_measurements']
        self.coordinates =  node_json_data['coordinates']


if __name__ == '__main__':
    pass
