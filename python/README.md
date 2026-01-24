# Various Python scripts...

Note. All files require Python 3 and pyserial to be installed

Pyserial can be installed using the command

pip install pyserial


## C7000_read_progmem.py

This script reads the program memory GD25Q08 using the same method as the UV008 Flash tool (written by andynvkz)
The script uses microcode reverse engineered from data transcactions between the UV008 Flash tool and the DM32

usage is

py C7000_read_progmem.py  COM_PORT BACKUP_FILE_NAME.bin

This script needs to be run while the radio is connected to the PC but the radio must be turned off.
Once the script has been run, you have 30 seconds to turn on the radio
After the radio is turned on the script will upload the microcode and begin reading the memory


## C7000_read_Q128.py

This script reads the program memory GD25Q126 (16Mb main flash memory) using the same method as the UV008 Flash tool (written by andynvkz)
The script uses microcode reverse engineered from data transcactions between the UV008 Flash tool and the DM32

usage is

py C7000_read_Q128.py  COM_PORT BACKUP_FILE_NAME.bin <START_ADDRESS_IN_HEX> <END_ADDRESS_IN_HEX>

If no start or end address is specified, the entire 16Mb chip will be read


This script needs to be run while the radio is connected to the PC but the radio must be turned off.
Once the script has been run, you have 30 seconds to turn on the radio
After the radio is turned on the script will upload the microcode and begin reading the memory


## DM32_firmware_loader.py

This script uploads raw unpackaged firmware data into the radio

IT SHOULD NOT BE USED WITH THE OFFICIAL BAOFENG FIRMWARE 

py DM32_firmware_loader.py  COM_PORT RAW_FIRMWARE_DATA.bin

To use this script, the radio needs to be in firmware update mode, i.e hold PTT and button SK1 (the button below the PTT), when turning on the radio

If you attempt to use this script to upload an official Baofeng firmware, the radio will not work after the firmware is loaded.
This is because the Baofeng firmware is packaged with a 256 byte header, and this header is removed by the Baofeng CPS before the firmware is uploaded

If you want to use this loader with the official Baofeng firmware, you should use a binary editor to first remove the 256 byte header.

