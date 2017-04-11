#updates device list only when the form is being rendered
#maintains both a dict and a list for easy access
from bootcamp.devices.models import Device

_deviceList = []
_deviceDict = {}
_deviceTuple = []

def update():
    global _deviceList
    global _deviceDict
    global _deviceTuple
    _deviceList = Device.objects.filter(status=Device.PUBLISHED)
    _deviceDict = dict((x.name, x) for x in _deviceList)
    _deviceTuple = [(x, x.name + ": " + x.location) for x in _deviceList]


def getDeviceList():
    update()
    return _deviceList

def getDeviceTuple():
    update()
    return _deviceTuple

def getDeviceDictionary():
    update()
    return _deviceDict





