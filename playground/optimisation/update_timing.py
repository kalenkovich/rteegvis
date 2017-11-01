import timeit
import numpy as np




# RingBuffer
from nfb.pynfb.brain.ring_buffer import RingBuffer

row_cnt = 7000
maxlen = 1200
buffer = RingBuffer(row_cnt=row_cnt, maxlen=maxlen)
samples_in_chunk = 40
chunk = np.random.random((samples_in_chunk, row_cnt))

def extend():
    buffer.extend(chunk.T)
timeit.timeit(extend, number=10)


def roll():
    np.roll(buffer._data, shift=-samples_in_chunk, axis=1)
timeit.timeit(roll, number=100)/100

# LocalDesync
from nfb.pynfb.brain.brain import LocalDesync