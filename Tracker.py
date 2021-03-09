from Torrent import Torrent
import asyncio
import aiohttp
import urllib.parse
from util_funcs import get_peer_id, get_transaction_id, TrackerResponseException, TrackerRequestException
import bencoder
import struct
import socket
import time
import Peer

#main tracker object - takes torrent object when initing and communicates with the tracker for that object
class Tracker(object):
    def __init__(self, torrent, url):
        self.torrent = torrent
        self.url = url
        self.peers = []

    def get_request_params(self):
        return \
            {
                'info_hash': self.torrent.get_torrent_info_hash(),
                'peer_id': get_peer_id(),
                'compact': 1,
                'port': 25247,
                'downloaded': 0,
                'left': self.torrent.get_torrent_size()
            }


class Tracker_http(Tracker):
    def __init__(self, torrent, url):
        print("initializing http tracker")
        super().__init__(torrent, url)
        self.url = self.url.decode()

    async def request_peers_http(self):
        async with aiohttp.ClientSession(trust_env = True) as session:
            #if self.url[-1] != "e":
                #self.url += "/announce"
            print(self.url)
            #self.url = yarl.URL(self.url).update_query(self.get_request_params())
            try:
                response = await session.get(self.url, params = urllib.parse.urlencode(self.get_request_params()), ssl=False)
            except Exception as e:
                raise TrackerResponseException(e)
            #print(response.url)
            response_data = await response.read()
            print("client request: {}".format(response))
            print("tracker response data: {}".format(response_data))
            peers = None
            try:
                peers = bencoder.decode(response_data)
            except Exception as e:
                raise TrackerResponseException("Error, tracker responing with: {0}".format(e))
            print(peers)
            return peers


class Tracker_wss(Tracker):
    def __init__(self, torrent, url):
        super().__init__(torrent, url)


class Tracker_udp(Tracker):
    def __init__(self, torrent, url):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn_id = 0x41727101980
        self.transactions = {}
        super().__init__(torrent, url)
        self.host = urllib.parse.urlparse(self.url).hostname
        self.port = urllib.parse.urlparse(self.url).port

    def udp_make_header(self, action_id):
        transaction_id = get_transaction_id()
        return transaction_id, struct.pack('!QLL', self.conn_id, action_id, transaction_id)

    def send(self, action, payload=None):
        self.sock.settimeout(15)
        print("got to send")
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

    def announce_payload(self, downloaded = 0, left = 0, uploaded = 0, event = 0, key = get_transaction_id()):
        payload = [self.torrent.get_torrent_info_hash(), get_peer_id().encode(), downloaded,
                   self.torrent.get_torrent_size(), uploaded, event, key, 1, -1, 6988]
        p_tosend = None
        try:
            p_tosend = struct.pack('!20s20sqqqiIIiH', *payload)
        except Exception as e:
            print("there was an error: {0}".format(e))
        return p_tosend

    def interpret(self, timeout=10):
        self.sock.settimeout(timeout)
        print("got to interpret")
        try:
            response = self.sock.recv(10240)
            print("answer received")
        except socket.timeout:
            print("no answer, try again")
            raise TrackerResponseException("no answer")

        headers = response[:8]
        payload = response[8:]

        action, trans_id = struct.unpack('!ll', headers)

        try:
            trans = self.transactions[trans_id]
        except KeyError:
            raise TrackerResponseException("InvalidTransaction: id ({0}) not found".format(trans_id))

        try:
            trans['response'] = self.process(action, payload, trans)
        except Exception as e:
            trans['response'] = None
            print("error occurred: {0}".format(e))
        trans['completed'] = True
        del self.transactions[trans_id]
        return trans

    async def connect_udp(self, try_num = 0):
        if try_num == 2:
            print("Tracker could not be reached or did not respond")
            raise TrackerResponseException("Tracker could not be reached or did not respond")
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

    async def announce_udp(self, try_num = 1):
        self.sock.settimeout(15)
        answer = {}
        inner_while = False
        while try_num < 4:
            while try_num < 4:
                try:
                    print("trying to send")
                    sended = self.send(1, self.announce_payload())
                    print("sending the following packet: {0}".format(sended))
                    print(self.url)
                    inner_while = True
                    break
                except Exception:
                    print("problem in announcing")
                    try_num += 1
            if not inner_while:
                break
            try:
                answer = self.interpret(15)
                break
            except Exception:
                print("problem in receiving announce answer")
                try_num += 1
        print("announce answer is: {0}".format(answer))
        return answer['response']['peers']

    async def scrape_udp(self):
        answer = {}
        self.sock.settimeout(15)
        try:
            sended = self.send(2, struct.pack("!20s", self.torrent.get_torrent_info_hash()))
            print("sending the following packet: {0}".format(sended))
        except Exception:
            print("problem in scraping")
        try:
            answer = self.interpret(15)
        except Exception:
            print("problem in receiving scrape answer")
        print("scrape answer is: {0}".format(answer))
        return answer

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
            raise TrackerResponseException("Invalid Action: {0}".format(action))

    def process_connect(self, payload, trans):
        self.conn_id = struct.unpack('!Q', payload)[0]
        return self.conn_id

    def process_announce(self, payload, trans):
        info = payload[:struct.calcsize("!lll")]
        interval, leechers, seeders = struct.unpack("!lll", info)
        print(interval, leechers, seeders)
        peer_data = payload[struct.calcsize("!lll"):]
        peer_size = struct.calcsize("!lH")
        num_of_peers = int(len(peer_data) / peer_size)
        print("the number of peers is: {0} and the peer data is: {1}".format(num_of_peers, peer_data))
        peers = []
        for peer_offset in range(num_of_peers):
            off = peer_size * peer_offset
            peer = peer_data[off:off + peer_size]
            addr, port = struct.unpack("!LH", peer)
            peers.append({'addr': socket.inet_ntoa(struct.pack('!L', addr)), 'port': port})
        print(payload)
        return dict(interval=interval, leechers=leechers, seeders=seeders, peers=peers)

    def process_scrape(self, payload, trans):
        info_size = struct.calcsize("!LLL")
        info_count = len(payload) / info_size
        response = []
        for info_offset in range(int(info_count)):
            off = info_size * info_offset
            info = payload[off:off + info_size]
            seeders, completed, leechers = struct.unpack("!LLL", info)
            response.append({'seeders': seeders, 'completed': completed, 'leechers': leechers})
        return response

    def process_error(self, payload, trans):
        message = struct.unpack("!8s", payload)
        raise TrackerResponseException("Error Response: {0}".format(message))

    async def test_peer_connect(self):
        announce_peers = await self.announce_udp()
        peers = []
        for peer in announce_peers:
            peer = Peer.Peer(peer['addr'], peer['port'], self.torrent)
            print(peer.host)
            try:
                await peer.download()
                print('appending peer: {0}'.format(peer.host))
                peers.append(peer)
            except Exception as e:
                print("failed to connect to peer: {0} because of error: {1}".format(peer.host, e))
        print(peers)
        return peers


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # debugging
    # loop.set_debug(True)
    # loop.slow_callback_duration = 0.001

    test_torrent = Torrent("C:\\temp\\wired-cd.torrent")
    print(test_torrent.get_torrent_tracker())
    print(test_torrent.get_torrent_name().decode())
    for tracker in test_torrent.get_torrent_announce_list():
        test_tracker = Tracker_udp(test_torrent, tracker[0])
        try:
            #loop.run_until_complete(test_tracker.request_peers_http())
            loop.run_until_complete(test_tracker.connect_udp())
            loop.run_until_complete(test_tracker.test_peer_connect())
            #loop.run_until_complete(test_tracker.announce_udp())
            #loop.run_until_complete(test_tracker.scrape_udp())
            break
        except Exception as e:
            print("tracker {0} did not work, exception was: {1}".format(tracker[0], e))
    loop.close()
