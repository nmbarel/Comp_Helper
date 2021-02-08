import copy
import hashlib
import urllib.parse
from pprint import pformat
import asyncio
import aiohttp
from util_funcs import get_peer_id
import bencoder


class Torrent(object):
    def __init__(self, path):
        self.path = path
        self.torrent_info = self.read_torrent_file()

    def read_torrent_file(self):
        with open(self.path, 'rb') as f:
            return bencoder.decode(f.read())

    def get_torrent_data(self):
        return pformat(self.torrent_info)

    def get_torrent_name(self):
        return self.torrent_info[b'info'][b'name']

    def get_torrent_size(self):
        info = self.torrent_info[b'info']
        if b'length' in info:
            return int(info[b'length'])
        else:
            return sum([int(f[b'length']) for f in info[b'files']])

    def get_torrent_info_hash(self):
        return hashlib.sha1(bencoder.encode(self.torrent_info[b'info'])).digest()

    def get_torrent_info_hash_decoded(self):
        return bencoder.encode(self.torrent_info[b'info'])

    def get_torrent_tracker(self):
        return self.torrent_info[b'announce'].decode('utf-8')

    def get_torrent_announce_list(self):
        return self.torrent_info[b'announce-list']

    def get_torrent_pieces(self):
        return self.torrent_info[b'info'][b'pieces']

    def get_piece_hash(self, piece_idx):
        return self.torrent_info[b'info'][b'pieces'][piece_idx * 20: (piece_idx * 20) + 20]


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # debugging
    # loop.set_debug(True)
    # loop.slow_callback_duration = 0.001
