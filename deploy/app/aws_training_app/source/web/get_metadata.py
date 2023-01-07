import os

_region_zone_name = None


def get_region_zone() -> str:
    global _region_zone_name

    if _region_zone_name:
        return _region_zone_name

    pipe = os.popen(r'curl http://169.254.169.254/latest/meta-data/placement/availability-zone/')

    answ = pipe.read()
    pclose = pipe.close()

    if pclose is None:
        _region_zone_name = str(answ)
        return _region_zone_name
    else:
        raise Exception('internal request error code: ' + str(pclose))


_public_ip = None


def get_public_ip() -> str:
    global _public_ip

    if _public_ip:
        return _public_ip

    pipe = os.popen(r'curl http://169.254.169.254/latest/meta-data/public-ipv4/')

    answ = pipe.read()
    pclose = pipe.close()

    if pclose is None:
        _public_ip = str(answ)
        return _public_ip
    else:
        raise Exception('internal request error code: ' + str(pclose))
