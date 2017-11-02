import nfb.pynfb.io.brainvision as brainvision


from nfb.pynfb.io.brainvision import read_raw_brainvision
vhdr_path = r'/home/evgenii/Downloads/ExpData/Bulavenkova_A_2017-10-24_15-33-18_Rest.vhdr'

brainvision_data = read_raw_brainvision(vhdr_fname=vhdr_path)