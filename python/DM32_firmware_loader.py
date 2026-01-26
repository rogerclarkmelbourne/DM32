import serial
import time
import os
import sys


def crc16_xmodem(data: bytes) -> int:
    crc = 0x0000

    for b in data:
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF

    return crc



portName = sys.argv[1]
# 1. Open serial port
port = serial.Serial(portName, 115200, timeout=0.5)
print("Open serial port " + portName)


print("Sending Init sequence")
port.write(b'\x52')
assert port.read(1) == b'\x06'

port.write(b'\x4D\x00\x00\x00\x01')
assert port.read(3) == b'\x4D\x01\x09'

port.write(b'\x06')
assert port.read(9) == b'BFUV32-V2'

port.write(b'\x45\x00\x00\x00\x00')
assert port.read(1) == b'\x06'

port.write(b'\x31')
assert port.read(1) == b'\x43'

port.write(b'\x01')
assert port.read(1) == b'\x43'

loopIndex = 1
BLOCK_SIZE = 0x400

fileSize = os.path.getsize(sys.argv[2])
totalBlocks = fileSize / BLOCK_SIZE

if (fileSize % BLOCK_SIZE != 0):
    totalBlocks = totalBlocks + 1
    
blockCount = 0




with open(sys.argv[2], "rb") as firmware:

    header = firmware.read(9)
    try:
        if header.decode('utf-8') == ('BFUV32-V2'):
            print("Official Baofeng firmware detected.")
            firmware.seek(0)
            firmware.seek(0x100)
        else:
            firmware.seek(0)
    except UnicodeDecodeError:
        firmware.seek(0)
    
    
    
    print("Send Erase command. Waiting to for up to 15 seconds for this to finish")

    port.write(b'\x00\xFF')
    
# Note. 
# This next write to the bootloader contains the filename and the size in bytes, expressed as text, padded to 128 bytes, with the CRC at the end
# The fileSize does not seem to be used by the bootloader, and replacing it with 0, worked fine.
# The file name does not seem to be important and it does not appear to be uploaded into the program memory of the radio,
# but possibly it is being stored in the GD25Q128 16Mb flash
    
    fileDetailsBuffer =(b'OpenDM32' + b'\x00' + str(fileSize).encode('ascii') )

    fileDetailsBufferLenth = len(fileDetailsBuffer)
    
    zeroBytes = bytearray(128 - fileDetailsBufferLenth)
    fileDetailsBuffer += zeroBytes
    port.write(fileDetailsBuffer)
    crc = crc16_xmodem(fileDetailsBuffer)
    crcBytes = crc.to_bytes(2,'big')
    port.write(crcBytes)
   
#set timeout because the response to the erase command takes just under 15 seconds   
    port.timeout = 15.0
    
#VERY LONG WAIT WHILE PROBABLY THE FLASH MEMORY IS ERASED

    assert port.read(2) == b'\x06\x43'

#set the timeout back to its normal default 
    port.timeout = 0.5
 
    print("Erase complete")
    
    print("Sending firmware data")
    
    lastPercentage = 0
    
    while True:
        block = firmware.read(BLOCK_SIZE)
        if not block:
            break
        blockLen = len(block)
        if (blockLen != BLOCK_SIZE):
            #print("Padding with "+str(BLOCK_SIZE - blockLen)+" zero bytes")
            additionalBytes = bytearray(BLOCK_SIZE - blockLen)
            block += additionalBytes
            #print("New block length is "+str(len(block)))
            
        port.write(b'\x02')
        assert port.read(1) == b'\x43'
        
        port.write((loopIndex).to_bytes(1,'big'))
        port.write((0xFF - loopIndex).to_bytes(1,'big'))
        progressPercentage = int((blockCount * 100) / totalBlocks)
        if (progressPercentage != lastPercentage):
            print( str(progressPercentage)+"%")
            lastPercentage = progressPercentage
        

        port.write(block) # write the 1k data block
        
        crc = crc16_xmodem(block) #calc crc
        crcBytes = crc.to_bytes(2,'big')
        port.write(crcBytes) # write the crc

        assert port.read(1) == b'\x06'
        
        loopIndex = loopIndex + 1
        if (loopIndex > 0xFF):
            loopIndex = 0
            
        blockCount += 1



print("Data send complete")





# The official Baofeng loader now sends 7 blocks of 130 bytes 0x00  with the  2 bytes of index number at the start 
# But it does not seem to be necessary to send these

# BUT SENDING THESE BYTES SEEMS TO NOT GET THE 0X06 RESPONSE, AND IT DOESNT SEEM TO BE NECESSARY TO SEND THEM

# port.timeout = 1
# loopNum = 0
# loopIndex = 0xFF
# while loopNum < 7:
    
    # print("Sending zeros")
    # port.write(b'\x01')
    # assert port.read(1) == b'\x43'
    
    # port.write((loopIndex).to_bytes(1,'big'))
    # port.write((0xFF - loopIndex).to_bytes(1,'big'))
    # port.write(bytearray(130))
    
    # assert port.read(1) == b'\x06'
    
    # loopIndex = loopIndex + 1
    
    # if (loopIndex > 0xFF):
       # loopIndex = 0
    
    # loopNum = loopNum + 1


print("Send Reboot command")
# COMMAND 0x04 appears to be the reboot command as after this there is only some sporadic bytes which are corrupt
port.write(b'\x04')




