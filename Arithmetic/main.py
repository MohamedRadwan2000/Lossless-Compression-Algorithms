import pyae
from decimal import Decimal
import struct

# Read message from file
with open('input.txt', 'r') as file:
    original_msg = file.read().strip()

AE = pyae.ArithmeticEncoding(original_msg)

MESSAGE_SIZE = 9
encoded_msg_list = []
last_message_len = len(original_msg) % MESSAGE_SIZE

print("===" , last_message_len)
msg = ""
for idx in range(0,len(original_msg) ,MESSAGE_SIZE):
    # Encode the message
    encoded_msg = AE.encode(original_msg[idx:idx+MESSAGE_SIZE])
    encoded_msg_list.append(encoded_msg)
    msg +=str(encoded_msg)[2:]
    binary_data = struct.pack('d', encoded_msg)
    with open('encoded.bin', 'ab') as file:
        file.write(binary_data)

decoded = ""

with open('encoded.bin', 'rb') as file:
    binary_data = file.read()

for idx in range(len(encoded_msg_list)):
    # Read binary data from file
    data = struct.unpack("d",binary_data[idx*8:idx*8+8])

    # Decode the message
    decoded_msg = AE.decode( Decimal(data[0]), MESSAGE_SIZE)
    print(decoded_msg)
    decoded +=decoded_msg

if decoded == original_msg:
    print("menio is the best")
else:
    print("fuck menio")
