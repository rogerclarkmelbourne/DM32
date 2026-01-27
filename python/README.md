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


## C7000_write_progmem.py

### WARNING. 
### USE THIS SCRIPT AT YOUR OWN RISK.
### IT CAN OVERWRITE CRITICAL DATA
### ALWAYS USE THE C7000_read_progmem.py SCRIPT TO BACKUP THE PROGRAM MEMORY BEFORE USING THIS SCRIPT TO WRITE TO THE PROGRAM MEMORY

This script writes to the program memory GD25Q08 using the same method as the UV008 Flash tool (written by andynvkz)
The script uses microcode reverse engineered from data transcactions between the UV008 Flash tool and the DM32

usage is

py C7000_write_progmem.py  COM_PORT FILE_TO_WRITE.bin <ADDRESS_OFFSET>

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

This script uploads firmware data into the radio using the Baofeng bootloader

The script attempts to detect whether the firmware file is a packaged official Baofeng firmware, or a raw firmware file, e.g. OpenTRx or OpenGD77 etc

Usage

py DM32_firmware_loader.py  COM_PORT   FIRMWARE_DATA.bin

To use this script, the radio needs to be in firmware update mode, i.e hold PTT and button SK1 (the button below the PTT), when turning on the radio

If the radio does not reboot into the firmware after loading has finished. The radio should be turned off, and the battery removed and reconnected.
Holding PTT + SK1 on the side of the radio, when turning the radio on, should again show the green LED which means the radio is fine, 
but the firmware file was not compatible with the DM32

## DM32_read_Q128.py

This script reads the GD25Q128 16Mb flash 'data' memory while the official Baofeng firmware is running.

py DM32_read_Q128.py  COM_PORT BACKUP_FILE_NAME.bin  <START_ADDRESS_IN_HEX  END_ADDRESS_IN_HEX>

If start address and end address are not specified, all of the 16Mb memory will be downloaded from the radio
