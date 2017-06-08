from gattlib import BeaconService

class Beacon_uuid(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "{UUID}"\
                .format(UUID=self._uuid)
        return ret

class Beacon_power(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "{POWER}"\
                .format(POWER=self._power)
        return ret

class Beacon_rssi(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "{POWER}"\
                .format(POWER=self._power)
        return ret

class Beacon_rssi(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "{RSSI}"\
                .format(RSSI=self._rssi)
        return ret
def measureDistance(txPower, rssi):
    if rssi == 0:
        return -1.0
    ratio = rssi * 1.0 / txPower
    if ratio < 1.0:
        return pow(ratio,10)
    else:
        return (0.89976) * pow(ratio, 7.7095) + 0.111

service = BeaconService("hci0")
devices = service.scan(2)

for address, data in list(devices.items()):
    uuid = Beacon_uuid(data, address)
    power = Beacon_power(data, address)
    rssi = Beacon_rssi(data, address)

    print(uuid)
    print(power)
    print(rssi)
    print("1.82278946499")
 #   print(measureDistance(power, rssi))

print("Done.")
