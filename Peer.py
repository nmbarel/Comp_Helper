from Torrent import Torrent
import bitarray
import asyncio
import socket


class Peer(object):
    def __init__(self, host, port, torrent):
        self.host = host
        self.port = port
        self.torrent = torrent
        self.have_pieces = bitarray.bitarray()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for piece in range(int(self.torrent.get_torrent_num_of_pieces())):
            self.have_pieces.append(False)
        print(self.have_pieces)
        print(len(self.have_pieces))

    async def download(self):
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port), timeout=1)
        except Exception as e:
            raise e


if __name__ == '__main__':
    tor = Torrent("C:\\temp\\wired-cd.torrent")
    print(tor.get_torrent_num_of_pieces())
    print(tor.get_torrent_piece_length())
    print(tor.get_torrent_last_piece_length())
    print(tor.get_torrent_size())
    peer = Peer('187.189.62.77', '51413', tor)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(peer.download())
    loop.close()
