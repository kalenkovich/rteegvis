from nfb.pynfb_io.xml_ import *

odict = read_xml_to_dict('nfb/pynfb_io/settings/pilot.xml')
print(odict)
write_dict_to_xml(odict, 'tests/test.xml')