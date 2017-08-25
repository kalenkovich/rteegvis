from nfb.pynfb_io.xml_ import save_signal, load_signal

from nfb.signals import DerivedSignal

#save_signal(DerivedSignal(), 'sig.xml')
load_signal('sig.xml', ['ch'+str(j) for j in range(50)])