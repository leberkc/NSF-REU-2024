

import sys
import time
from struct import unpack, error
from random import random
from ctypes import c_int
from collections import defaultdict

from math import ceil
import lt_sampler

 
DEBUG = False


# Check node in graph
class CheckNode(object):

    def __init__(self, src_nodes, check):
        self.check = check
        self.src_nodes = src_nodes

class BlockGraph(object):
    """Graph on which we run Belief Propagation to resolve 
    source node data
    """
    
    def __init__(self, num_blocks):
        self.checks = defaultdict(list)
        self.num_blocks = num_blocks
        self.eliminated = {}

    def add_block(self, nodes, data):
        """Adds a new check node and edges between that node and all
        source nodes it connects, resolving all message passes that
        become possible as a result.
        """

        # We can eliminate this source node
        if len(nodes) == 1:
            to_eliminate = list(self.eliminate(next(iter(nodes)), data))

            # Recursively eliminate all nodes that can now be resolved
            while len(to_eliminate):
                other, check = to_eliminate.pop()
                to_eliminate.extend(self.eliminate(other, check))
        else:

            # Pass messages from already-resolved source nodes
            for node in list(nodes):
                if node in self.eliminated:
                    nodes.remove(node)
                    data ^= self.eliminated[node]

            # Resolve if we are left with a single non-resolved source node
            if len(nodes) == 1:
                return self.add_block(nodes, data)
            else:

                # Add edges for all remaining nodes to this check
                check = CheckNode(nodes, data)
                for node in nodes:
                    self.checks[node].append(check)

        # Are we done yet?
        return len(self.eliminated) >= self.num_blocks

    def eliminate(self, node, data):
        """Resolves a source node, passing the message to all associated checks
        """

        # Cache resolved value
        self.eliminated[node] = data
        others = self.checks[node]
        del self.checks[node]

        # Pass messages to all associated checks
        for check in others:
            check.check ^= data
            check.src_nodes.remove(node)

            # Yield all nodes that can now be resolved
            if len(check.src_nodes) == 1:
                yield (next(iter(check.src_nodes)), check.check)



def read_blocks(client_socket, drop_rate):
    """Generate parsed blocks from input socket
    """
    while True:
        header_bytes = client_socket.recv(12)
        header = unpack('!III', header_bytes)

        blockdata = client_socket.recv(header[1])
        block  = int.from_bytes(blockdata, 'big')

        if DEBUG: print("AT read_blocks, RECEIVED header={}, data block=\"{}\"".format(header,block))
        yield (header, block)

def handle_block(src_blocks, block, block_graph):
    """What to do with new block: add check and pass
    messages in graph
    """
    return block_graph.add_block(src_blocks, block)


def decode(client_socket, drop_rate):
    """Reads from client_socket, applying the LT decoding algorithm
    to incoming encoded blocks until sufficiently many blocks
    have been received to reconstruct the entire file.

    Simulates lossy channel via p(block dropped) = drop_rate
    """

    # init stuff
    time_start = time.time()
    total_size = 0
    DECODED_STR = ''

    # data structures
    block_graph = None
    prng = None

    # counters
    blocks_received, blocks_dropped = 0, 0
    bytes_received = 0

    if DEBUG: print("AT decode, drop_rate={}".format(drop_rate))
    # Begin forever loop
    for (filesize, blocksize, blockseed), block in read_blocks(client_socket, drop_rate):

        if DEBUG: print("AT decode, filesize={}, blocksize={}, blockseed={},block={}".format(filesize, blocksize, blockseed,block.to_bytes(blocksize, sys.byteorder)))
        # drop some packets
        if random() < drop_rate:
            blocks_dropped  += 1
            continue #skips packet

        blocks_received += 1
        bytes_received += blocksize

        # first time around, init things
        if not prng:
            total_size = filesize
            if DEBUG: print("AT decode, total_size={}".format(total_size))

            K = ceil(filesize/blocksize)
            prng = lt_sampler.PRNG(params=(K, lt_sampler.PRNG_DELTA, lt_sampler.PRNG_C))
            block_graph = BlockGraph(K)

        # Run PRNG with given seed to figure out which blocks were XORed to make received data
        _, _, src_blocks = prng.get_src_blocks(seed=blockseed)

        # If belief propagation is done, stop
        if handle_block(src_blocks, block, block_graph):
            if DEBUG: print("AT decode, belief propagation is done")
            client_socket.send('1'.encode())
            break
    
    # Stop the timer
    time_end = time.time()

    # Iterate through blocks, stopping before padding junk
    for ix, block_str in enumerate(map(lambda p: int.to_bytes(p[1], blocksize, sys.byteorder).decode('utf8'), 
            sorted(block_graph.eliminated.items(), key = lambda p:p[0]))):
        if ix < K-1 or filesize % blocksize == 0:
            DECODED_STR = DECODED_STR + block_str
        else:
            DECODED_STR = DECODED_STR + block_str[:filesize%blocksize]

    # Compute some stats
    time_elapsed = (time_end - time_start) * 1000
    
    #NOTE: summary stats break when blocks are of different sizes
    rate = total_size / bytes_received
    # Report summary stats on transmission 
    
    print("\nDecoded message ====---->: {}\n".format(DECODED_STR))
    if time_elapsed > 1000:
        print("Transmission Time: %.4fs" % (time_elapsed / 1000), file=sys.stderr)
    else:
        print("Transmission Time: %.4fms" % time_elapsed, file=sys.stderr)
    print("Total size:        %d" % total_size, file=sys.stderr)
    print("Packet Stats:", file=sys.stderr)
    print("\tPackets Received:  %d" % (blocks_received + blocks_dropped), file=sys.stderr)
    print("\tPackets Processed: %d" % blocks_received, file=sys.stderr)
    print("\tPackets Dropped:   %d" % blocks_dropped, file=sys.stderr)
    print("Data Stats", file=sys.stderr)
    print("\tBytes/packet: %d" % (bytes_received / blocks_received) , file=sys.stderr)
    print("\tBytes Total:  %d" % bytes_received, file=sys.stderr)
    print("Code Rate: %1.4f" % rate, file=sys.stderr)
    
    return blocks_received + blocks_dropped, blocks_received

def start(client_socket):
    try:
        return decode(client_socket, drop_rate)
    except Exception as e:
        print("Decoder got some error: {}.".format(e))

    if DEBUG: print("EXIT")

drop_rate = 0.5

