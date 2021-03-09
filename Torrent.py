import hashlib
from pprint import pformat
import asyncio
import bencoder


class Torrent(object):
    def __init__(self, path):
        self.path = path
        self.torrent_info = self.read_torrent_file()
        self.trackers = self.get_torrent_announce_list()
        print(self.trackers)

    def read_torrent_file(self):
        with open(self.path, 'rb') as f:
            return bencoder.decode(f.read())

    def get_torrent_data(self):
        return pformat(self.torrent_info)

    def get_torrent_name(self):
        return self.torrent_info[b'info'][b'name']

    def get_torrent_ind_size(self):
        info = self.torrent_info[b'info']
        if b'length' in info:
            return {info[b'name']: info[b'length']}
        else:
            return [{f[b'name']: f[b'length']} for f in info[b'files']]

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

    def get_torrent_piece_length(self):
        return self.torrent_info[b'info'][b'piece length']

    def get_torrent_num_of_pieces(self):
        x = self.get_torrent_size() / self.get_torrent_piece_length()
        if int(x) < x:
            return int(x+1)
        else:
            return int(x)

    def get_torrent_last_piece_length(self):
        return int(self.get_torrent_size() - ((self.get_torrent_num_of_pieces() - 1) * self.get_torrent_piece_length()))


if __name__ == '__main__':
    tor = Torrent("C:\\temp\\htmlt.torrent")
    print(tor.get_torrent_info_hash_decoded())
    print(tor.get_torrent_pieces())
    print(tor.get_piece_hash(0))
    print(tor.get_torrent_piece_length())
    print(tor.get_torrent_num_of_pieces())
    print(tor.get_torrent_last_piece_length())
