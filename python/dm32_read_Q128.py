import serial
import time
import os
import sys

portName = sys.argv[1]
# 1. Open serial port
port = serial.Serial(portName, 115200, timeout=0.5)
print("Open serial port " + portName)

time.sleep(0.1)

# 2. Handshake
port.write(b'PSEARCH')


assert port.read(8) == b'\x06DP570UV'

time.sleep(0.1)
port.write(b'PASSSTA')

port.read(3)  # Status (varies)


port.write(b'SYSINFO')
print("Waiting for response from radio")
while port.in_waiting <1:
    time.sleep(0.1)

assert port.read(1) == b'\x06'
time.sleep(0.1)


# 3. Get memory layout
port.write(b'\x56\x00\x00\x00\x0A')  # V-frame 0x0A
response = port.read(11)
start_addr_dynamic_data = int.from_bytes(response[3:7], 'little')  # 0x001000
end_addr_dynamic_data = int.from_bytes(response[7:11], 'little')   # 0x0C8FFF

print("Entering access mode")
port.write(b'\xFF\xFF\xFF\xFF\x0CPROGRAM')
assert port.read(1) == b'\x06'
port.write(b'\x02')
assert port.read(8) == b'\xFF' * 8
port.write(b'\x06')
assert port.read(1) == b'\x06'

#start_addr = 0xa7000

start_addr = 0
end_addr   = 0x1000000

if (len(sys.argv) >= 4):
    start_addr = int(sys.argv[3],16)

if (len(sys.argv) >= 5):
    end_addr = int(sys.argv[4],16)

readLength = 0x001000

print("Start Add:" + hex(start_addr) + " End Add:" + hex(end_addr))
lastPercent = -1;
with open(sys.argv[2], 'wb') as f:
    for addr in range(start_addr, end_addr, readLength):
        # Read metadata byte
        cmd = b'\x52' + addr.to_bytes(3, 'little') + readLength.to_bytes(2,'little')
        port.write(cmd)
        
        response = port.read(len(cmd) + readLength)
        f.write(response[6:])
        percent = int(((addr + readLength) * 100)/(end_addr - start_addr))
        if (percent != lastPercent):
            print( str(percent) +"%")
            lastPercent = percent

port.close()