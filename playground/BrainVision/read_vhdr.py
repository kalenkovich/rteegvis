import os
import sys

from mne.io import read_raw_brainvision

vhdr_path = r'/home/evgenii/Downloads/ExpData/Bulavenkova_A_2017-10-24_15-33-18_Rest.vhdr'

bobe_header = 'BrainVision Data Exchange Header File Version 1.0'
normal_header = b'Brain Vision Data Exchange Header File Version 1.0\r\n'
from mne.io.brainvision.brainvision import _check_hdr_version

def _bobe_header_make_copies(vhdr_path):
    byte_to_str = lambda bstr: bstr.decode('ascii', 'ignore').strip()
    str_to_byte = lambda str: str.
    with open(vhdr_path, 'rb') as vhdr:
        bheader = vhdr.readline()
        header = bheader
        try:
            _check_hdr_version(header)
        except ValueError as e:
            if header == bobe_header:
                root, ext = os.path.splitext(vhdr_path)
                vhdr_copy_path = root + '_copy_for_nfb' + ext
                with open(vhdr_copy_path, 'wb') as vhdr_copy:
                    vhdr_copy.write(normal_header)
                    for line in vhdr:
                        if line.decode('ascii', 'ignore').split
                        vhdr_copy.write(line)
            else:
                new_message = ('\nmne-python error message:\n' + str(e) +
                               '\n\nWe actually also support "{}" (no space between Brain and Vision), but that is it.'
                                   .format(bobe_header))
                raise type(e)(new_message).with_traceback(sys.exc_info()[2])

    vhdr = read_raw_brainvision(vhdr_fname=vhdr_copy_path)

_check_mrk_version(header)
