"""
Import Vale of Glamorgan
"""
from data_collection.management.commands import BaseShpShpImporter

class Command(BaseShpShpImporter):
    """
    Imports the Polling Station data from Vale of Glamorgan
    """
    council_id     = 'W06000014'
    districts_name = 'Polling Districts'
    stations_name  = 'Polling Stations.shp'

    def district_record_to_dict(self, record):

        # this address is missing from the stations file
        # so put it in an object property where we can
        # pick it up in station_record_to_dict()
        if record[0] == 'FD1':
            self.fd1_address = record[4]

        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):

        address = record[2]
        if record[0] == 'FD1':
            address = self.fd1_address

        # extract postcode
        try:
            address_parts = address.split(', ')
            postcode = address_parts[-1]
            if postcode == 'Penarth' or postcode == 'The Knap' or postcode == 'Leckwith':
                postcode = ''
        except TypeError:
            postcode = ''

        # format address
        del(address_parts[-1])
        address = "\n".join(address_parts)

        return {
            'internal_council_id': record[0],
            'postcode'           : postcode,
            'address'            : address
        }
