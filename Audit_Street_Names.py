
# coding: utf-8

# In[4]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "victoria_canada.osm"
street_type_format = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected =  ["Street", "Avenue", "Boulevard", "Drive","Court", "Place","Square","Lane",
         "Road","Trail","Parkway", "Commons","Highway","Way",'101', '20', 'Access','Alley', 'Bend', 'Bend','Box', 'Chase', 
            'Circle', 'Cove', 'Close', 'Crescent', 'Dell', "Esplanade", 'Estates', 'Gardens', 'Gate', 'Glen', 'Green','Grove',
            'Heights', 'Hill', 'Hills', 'Landing', 'Loop', 'Meadows', 'Plateau', 'Reach', 'Ridge', 'Rise', 'Row', 'Run',
            'Spur', 'Station', 'Terrace', 'Track','View', 'Vista','Walk', 'Wood', 'Woods', 'Wynd', "Southeast", "Southwest", 
            "Northeast","Northwest",'East','West','North','South']


def audit_street_type(street_types, street_name):
    #Audits street names to check for unexpected street names
    m = street_type_format.search(street_name)
    if m:
        street_type = m.group() 
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    #Checks to see if elem is a street name
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    #Returns unexpected street types
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"): 
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

unexpected_street_types = audit(OSMFILE)
pprint.pprint(dict(unexpected_street_types)) 


# In[ ]:




# In[ ]:



