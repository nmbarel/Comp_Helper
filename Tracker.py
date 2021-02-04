from scapy.layers.inet import IP, UDP, TCP, ICMP
from Torrent import Torrent
import asyncio
import aiohttp
import urllib.parse
from util_funcs import get_peer_id, get_transaction_id, TrackerResponseException, TrackerRequestException
import bencoder
import scapy.all as scapy
import struct
import socket
import random
import time


class Tracker(object):
    def __init__(self, torrent):
        self.torrent = torrent
        self.url = self.torrent.get_torrent_tracker()
        self.peers = []

    def change_trackers(self, currenttracker):
        self.url = self.torrent.get_torrent_announce_list()[currenttracker + 1][0]

    def get_request_params(self):
        return \
            {
                'info_hash': urllib.parse.quote(self.torrent.get_torrent_info_hash()),
                'peer_id': urllib.parse.quote(get_peer_id()),
                'compact': 1,
                'no_peer_id': 0,
                'event': 'started',
                'port': 25247,
                'uploaded': 0,
                'downloaded': 0,
                'left': self.torrent.get_torrent_size()
            }

class Tracker_http(Tracker):
    async def request_peers_http(self, url):
        i = 1
        async with aiohttp.ClientSession(trust_env = True) as session:
            if url[-1] != "e":
                url += "/announce"
            print(url)
            try:
                response = await session.get(url, params=self.get_request_params(), ssl=False)
            except Exception:
                print('Failed to get response')
                tracker_list = self.torrent.get_torrent_announce_list()
                for url in tracker_list:
                    await self.request_peers_http(url[0].decode('utf-8'))
            print(response.url)
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


class Tracker_udp(Tracker):
    def __init__(self, torrent):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn_id = 0x41727101980
        self.transactions = {}
        super().__init__(torrent)

    def host_port_update(self):
        self.host = urllib.parse.urlparse(self.url).hostname
        self.port = urllib.parse.urlparse(self.url).port

    def udp_make_header(self, action_id):
        transaction_id = get_transaction_id()
        return transaction_id, struct.pack('!QLL', self.conn_id, action_id, transaction_id)

    def send(self, action, payload=None):
        print("got to send")
        self.host_port_update()
        if not payload:
            payload = ''.encode()
        trans_id, header = self.udp_make_header(action)
        self.transactions[trans_id] = trans = {
            'action': action,
            'time': time.time(),
            'payload': payload,
            'completed': False,
        }
        self.sock.sendto(header + payload, (self.host, self.port))
        return trans

    def send_connect_udp(self):
        sended = self.send(0)
        print(sended)
        return sended

    def announce_payload(self, downloaded = 0, left = 0, uploaded = 0, event = 0):
        payload = [self.torrent.get_torrent_info_hash, get_peer_id(), downloaded, left, uploaded, event, 0, get_transaction_id(), -1, 6988]
        return struct.pack('!20s20sqqqiIIiH', *payload)

    def send_announce_udp(self):
        sended = self.send(1, self.announce_payload())
        print(sended)
        return sended

    def interpret(self):
        self.sock.settimeout(15)
        print("got to interpret")
        try:
            response = self.sock.recv(10240)
            print("answer recieved")
        except socket.timeout:
            print("no answer, try again")
            raise TrackerResponseException("no answer", 0)

        headers = response[:8]
        payload = response[8:]

        action, trans_id = struct.unpack('!LL', headers)

        try:
            trans = self.transactions[trans_id]
        except KeyError:
            raise TrackerResponseException("InvalidTransaction: id not found", trans_id)

        trans['response'] = self.process(action, payload, trans)
        trans['completed'] = True
        del self.transactions[trans_id]
        print(trans)
        return trans

    async def connect_udp(self, try_num):
        if try_num == len(self.torrent.get_torrent_announce_list()):
            print("no tracker worked.")
            return None
        self.change_trackers(try_num)
        try:
            sended = self.send(0)
            print(sended)
        except Exception:
            print("connect udp exception")
            await self.connect_udp(try_num + 1)
        finally:
            answer = {}
            try:
                answer = self.interpret()
            except Exception:
                await self.connect_udp(try_num + 1)
            return answer

    async def announce_udp(self, try_num):
        pass

    def process(self, action, payload, trans):

        if action == 0:
            return self.process_connect(payload, trans)
        elif action == 1:
            return self.process_announce(payload, trans)
        elif action == 2:
            return self.process_scrape(payload, trans)
        elif action == 3:
            return self.process_error(payload, trans)

        else:
            raise TrackerResponseException("Invalid Action", action)

    def process_connect(self, payload, trans):
        self.conn_id = struct.unpack('!Q', payload)[0]
        return self.conn_id


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # debugging
    # loop.set_debug(True)
    # loop.slow_callback_duration = 0.001

    test_torrent = Torrent("C:\\temp\\wired-cd.torrent")
    test_tracker = Tracker_udp(test_torrent)
    print(urllib.parse.quote(test_torrent.get_torrent_info_hash()))
    print(test_torrent.get_torrent_tracker())
    print(test_torrent.get_torrent_name().decode())
    loop.run_until_complete(test_tracker.connect_udp(0))
    print(test_tracker.conn_id)
    loop.close()
