from nfb.pynfb.generators import stream_file_in_a_thread
from nfb.pynfb.io.xml_ import xml_file_to_params

params = xml_file_to_params('nfb/pynfb/sourcespace.xml')
file_path = params['sRawDataFilePath']
stream_name = params['sStreamName']
reference = params['sReference']

if __name__ == '__main__':
    thread = stream_file_in_a_thread(file_path, reference, stream_name)