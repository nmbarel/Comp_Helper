import random
import string


def get_peer_id():
    rand_num = ''
    for i in range(18):
        rand_num = rand_num + (random.choice(string.ascii_lowercase + string.digits))
    return 'SA' + rand_num

