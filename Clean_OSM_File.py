
# coding: utf-8

# In[8]:

import xml.etree.cElementTree as ET
import re

OSMFILE = "victoria_canada.osm"
CLEANED_OSMFILE = "victoria_canada_cleaned.osm"

street_format = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected =  ["Street", "Avenue", "Boulevard", "Drive","Court", "Place","Square","Lane",
             "Road","Trail","Parkway", "Commons","Highway","Way",'101', '20', 'Access','Alley', 'Bend', 'Bend','Box', 'Chase', 
            'Circle', 'Cove', 'Close', 'Crescent', 'Dell', "Esplanade", 'Estates', 'Gardens', 'Gate', 'Glen', 'Green','Grove',
            'Heights', 'Hill', 'Hills', 'Landing', 'Loop', 'Meadows', 'Plateau', 'Reach', 'Ridge', 'Rise', 'Row', 'Run',
            'Spur', 'Station', 'Terrace', 'Track','View', 'Vista','Walk', 'Wood', 'Woods', 'Wynd', "Southeast", "Southwest", 
            "Northeast","Northwest",'East','West','North','South']

mapping = {"St": "Street",
           "St.": "Street",
           "Rd": "Road",
           "Dr": "Drive",
           "Streeteet": 'Street',
           "Deerpath": "Deerpath Road",
           "(WA)":""
           }

                       
    
def is_street_name(elem):
    #Checks to see if elem is a street name
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    #Checks to see if elem is a postal code
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")
    
def update_street_name(name):
    #Updates the street name  
    m= street_format.search(name)
    if m:
        pattern = m.group()
        if pattern in mapping:
            start_index = m.start()
            name = name[:start_index] + mapping[pattern] 
        return name
    else:
        return name

def update_postal_code(postal_code):
    #Updates the postal code
    if re.findall(r'^\d{5}$', postal_code): 
        new_postal_code = postal_code
        return new_postal_code
    elif re.findall(r'(^\d{5})-\d{4}$', postal_code):
        new_postal_code = re.findall(r'(^\d{5})-\d{4}$', postal_code)[0]
        return new_postal_code
    elif re.findall(r'WA\s*\d{5}', postal_code): 
        new_postal_code =re.findall(r'\d{5}', postal_code)[0]  
        return new_postal_code  
    elif re.findall(r'[A-z][0-9][A-z][\s-]?[0-9][A-z][0-9]', postal_code):
        new_postal_code= postal_code.upper()
        new_postal_code=re.sub(r'[\s-]','',new_postal_code)
        return new_postal_code  
    else:
        return None  
    
def get_element(osm_file, tags=('node', 'way', 'relation')):
    #Yield element if it is the right type of tag
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
        
def create_new_xml(filename,newfilename):   
    with open(filename, "rb") as infile, open(newfilename, "wb") as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<osm>\n  ')
        for elem in get_element(infile):
            if elem.tag == "node" or elem.tag == "way": #only check way and node
                if elem.find("tag") != -1:
                    for tag in elem.iter("tag"): 
                        if is_street_name(tag):
                            street_name = tag.attrib['v']
                            street_name = update_street_name(street_name)
                            tag.attrib['v'] = street_name           
                        elif is_postal_code(tag):
                            postal_code = tag.attrib['v'] 
                            if update_postal_code(postal_code) == None:
                                elem.remove(tag) 
                            else:
                                postal_code = update_postal_code(postal_code)
                                tag.attrib['v']  = postal_code                       
            outfile.write(ET.tostring(elem, encoding='utf-8')) 
        outfile.write('</osm>')
                        
create_new_xml(OSMFILE,CLEANED_OSMFILE)


# In[ ]:



