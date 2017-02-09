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
    _deviceDict = dict((x.devicename, x) for x in _deviceList)
    _deviceTuple = [(x, x.devicename + ": " + x.first_name + ' ' + x.last_name) for x in _deviceList]


def getDeviceList():
    return _deviceList

def getDeviceTuple():
    return _deviceTuple

def getDeviceDictionary():
    return _deviceDict





