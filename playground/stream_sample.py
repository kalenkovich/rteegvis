from mne.datasets import sample

from nfb.pynfb.generators import stream_file_in_a_thread
from nfb.pynfb.io.xml_ import xml_file_to_params

params = xml_file_to_params('nfb/pynfb/sourcespace.xml')
stream_name = params['sStreamName']
reference = params['sReference']

data_path = sample.data_path()
file_path = data_path + '/MEG/sample/sample_audvis_raw.fif'

if __name__ == '__main__':
    thread = stream_file_in_a_thread(file_path, reference, stream_name)