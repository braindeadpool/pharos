import bluetooth
import os
import sys
import requests

global UserCode
global SampleCode
global DevCode
global process

while 1:
	##Device Connection via Bluetooth
	target_name = "001072-S-US-1153"
	target_address = "00:07:80:BA:CC:48"

	nearby_devices = bluetooth.discover_devices()

	for bdaddr in nearby_devices:
		if target_name == bluetooth.lookup_name(bdaddr):
			target_address = bdaddr
			break
			
	if target_address is not None:
		print("Found target bluetooth device with address"), target_address
	else:
		print("Could not find target bluetooth device nearby")

def scan():
	
	##Function to be called each time a new code is needed to be scanned

	global UserCode
	global SampleCode
	global DevCode
	global process

	UserCode = None
	SampleCode = None
	DevCode = None
	process = None

	##ASCII Communication Block
	bd_addr = "00:07:80:BA:CC:48"
	port = 1
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bd_addr,port))

	data = ""
	while 1:
		try:
			data += sock.recv(1024)
			data_end = data.find('\n')
			if data_end != -1:
				rec = data[data_end+1:]
				print(data)
				if "EP" in data:
					print("HEXCODE RECEIVED")

					##Extract HexCode From Transmission
					HexCode = data[4:28]
					
					url = 'http://38.110.18.171:8000/'

					if HexCode.startswith('8'):
						UserCode = HexCode
						print("User Code: %s" % UserCode)
						query = {'User': HexCode}
						url = 'http://38.110.18.171:8000/scan/user/' + UserCode

					elif HexCode.startswith('4'):
						DevCode = HexCode
						print("Device Code: %s" % DevCode)
						query = {'Device': HexCode}
						url = 'http://38.110.18.171:8000/scan/device/' + DevCode

					elif HexCode.startswith('0'):
						SampleCode = HexCode
						print("Sample Code: %s" % SampleCode)
						query = {'Sample': HexCode}
						url = 'http://38.110.18.171:8000/scan/sample/' + SampleCode

					if process is not None:
						process.terminate()
					process = subprocess.Popen([command, url])

					print(HexCode)

				data = data[data_end+1:]
		except KeyboardInterrupt:
			break
	sock.close()

scan()
