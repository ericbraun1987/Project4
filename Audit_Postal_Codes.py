
# coding: utf-8

# In[7]:

import xml.etree.cElementTree as ET
import re
import pprint

OSMFILE = "victoria_canada.osm"
postal_code_us = re.compile(r'^\d{5}')
postal_code_canada=re.compile(r'^[A-z][0-9][A-z][\s-]?[0-9][A-z][0-9]')


def audit_postal_code(postal_codes,value):
    #Audits postal codes for US and Canadian formats, returning unexpected values
    m = postal_code_us.search(value)
    m2= postal_code_canada.search(value)
    if not m and not m2: 
        postal_codes.add(value)

def is_postal_code(elem):
    #Checks if elem is a postal code
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    postal_codes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way": 
            for tag in elem.iter("tag"): 
                if is_postal_code(tag):
                    audit_postal_code(postal_codes,tag.attrib['v'])
    osm_file.close()
    return postal_codes
      
postal_codes = audit(OSMFILE)
pprint.pprint(postal_codes)


# In[21]:




# In[ ]:



