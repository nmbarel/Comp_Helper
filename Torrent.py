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
        print(self.torrent_info[b'info'])
        print(bencoder.encode(self.torrent_info[b'info']))
        print(hashlib.sha1(bencoder.encode(self.torrent_info[b'info'])).digest())
        return hashlib.sha1(bencoder.encode(self.torrent_info[b'info'])).digest()

    def get_torrent_tracker(self):
        return self.torrent_info[b'announce'].decode('utf-8')

    def get_torrent_pieces(self):
        return self.torrent_info[b'info'][b'pieces']

    def get_piece_hash(self, piece_idx):
        return self.torrent_info[b'info'][b'pieces'][piece_idx * 20: (piece_idx * 20) + 20]


class Tracker(object):
    def __init__(self, torrent):
        self.torrent = torrent
        self.url = self.torrent.get_torrent_tracker()
        self.peers = []

    def get_request_params(self):
        return \
            {
                'info_hash': (self.torrent.get_torrent_info_hash()),
                'peer_id': (get_peer_id()),
                'compact': 1,
                'no_peer_id': 0,
                'event': 'started',
                'port': 25247,
                'uploaded': 0,
                'downloaded': 0,
                'left': self.torrent.get_torrent_size()
            }

    async def request_peers(self):
        async with aiohttp.ClientSession(trust_env = True) as session:
            response = await session.get(self.url, params=self.get_request_params())
            response_data = await response.read()
            print("client request: {}".format(response))
            print("tracker response data: {}".format(response_data))
            peers = None
            try:
                peers = bencoder.decode(response_data)
            except Exception:
                print('Failed to get response')
            print(peers)
            return peers


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # debugging
    # loop.set_debug(True)
    # loop.slow_callback_duration = 0.001

    test_torrent = Torrent("C:\\temp\\wired-cd.torrent")
    test_tracker = Tracker(test_torrent)
    print(test_torrent.get_torrent_tracker())
    print(test_torrent.get_torrent_name().decode())
    loop.run_until_complete(test_tracker.request_peers())
    loop.close()
