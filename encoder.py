
"""Implementation of a Luby Transform encoder.

This is a type of fountain code, which deals with lossy channels by 
sending an infinite stream of statistically correllated packets generated
from a set of blocks into which the source data is divided. In this way, 
epensive retransmissions are unecessary, as the receiver will be able 
to reconstruct the file with high probability after receiving only 
slightly more blocks than one would have to transmit sending the raw
blocks over a lossless channel.

See 

D.J.C, MacKay, 'Information theory, inference, and learning algorithms'.
Cambridge University Press, 2003

for reference.
"""

import os.path
import sys
import time
import pdb
from struct import pack

import lt_sampler

DEBUG = False

def get_blocks(msg, blocksize):
    """Block file byte contents into blocksize chunks, padding last one if necessary
    """
    msg_bytes = bytearray()
    msg_bytes.extend(msg.encode())

    if DEBUG: print("AT get_blocks: blocksize={}".format(blocksize))
    if DEBUG: print("AT get_blocks: msg={}".format(msg))

    blocks = [int.from_bytes(msg_bytes[i:i+blocksize].ljust(blocksize, b'0'), sys.byteorder) 
            for i in range(0, len(msg), blocksize)]
    if DEBUG: print("AT get_blocks: blocks={}".format(blocks))

    return len(msg), blocks


def encoder(msg, blocksize, seed, c, delta):
    """Generates an infinite sequence of blocks to transmit
    to the receiver
    """

    if DEBUG: print("AT encoder: msg={}".format(msg))
    # get file blocks
    filesize, blocks = get_blocks(msg, blocksize)

    # init stream vars
    K = len(blocks)
    prng = lt_sampler.PRNG(params=(K, delta, c))
    prng.set_seed(seed)

    # block generation loop
    while True:
        blockseed, d, ix_samples = prng.get_src_blocks()
        if DEBUG: print("AT encoder: blockseed={}, d={},ix_samples={}".format(blockseed,d,ix_samples))
        block_data = 0
        for ix in ix_samples:
            block_data ^= blocks[ix]
            if DEBUG: print("AT encoder: ix={}, (encoded)block_data={}".format(ix,block_data))

        # Generate blocks of XORed data in network byte order
        yield (filesize, blocksize, blockseed, int.to_bytes(block_data, blocksize, 'big'))

def run(client_socket, msg, blocksize, seed, c, delta):
    """Run the encoder until the channel is broken, signalling that the 
    receiver has successfully reconstructed the file
    """

    if DEBUG: print("AT run: msg={}, seed={}, c={}, delta={}".format(msg,seed, c, delta))

    ENCODER_BLK =  encoder(msg, blocksize, seed, c, delta)
    if DEBUG: print("AT run: ENCODER_BLK={}".format(ENCODER_BLK))
    for block in ENCODER_BLK:
        client_socket.sendall(pack('!III%ss'%blocksize, *block))
        
    if DEBUG: print("AT run - DONE")


def start(client_socket, msg):
    try:
        if DEBUG: print("AT to run")
        run(client_socket, msg, blocksize, seed, c, delta)
    except Exception as e:
        print("Decoder may has cut off transmission. Fountain closed.")
        print("error message: {}".format(e))
        sys.exit(0)
    if DEBUG: print("EXIT")

blocksize = 10000
seed = 2067261
c = lt_sampler.PRNG_C
delta = lt_sampler.PRNG_DELTA


