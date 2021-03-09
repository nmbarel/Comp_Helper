import struct
import sys
import udptrack
import Torrent
import socket
test = Torrent.Torrent("C:\\temp\\gentoomen-library.torrent")
announce_url = test.get_torrent_announce_list()
has = test.get_torrent_info_hash()
print(announce_url[1][0])
tracker = udptrack.UDPTracker(announce_url[1][0], timeout=2, info_hash=test.get_torrent_info_hash())
#print(socket.getaddrinfo('tracker.ccc.de', 80))
print(tracker.connect())
print("fdsfasdfdsg"
      ""
      ""
      ""
      "")
print(type("f").encode('utf-8'))
print(tracker.interpret())
#tracker.announce()
#print(tracker.interpret())

