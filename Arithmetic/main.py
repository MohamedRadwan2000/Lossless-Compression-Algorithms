import pyae
from decimal import Decimal

PRECSION = 101
BYTES =  42
MESSAGE_SIZE = 58
"""
encoded_msg="0.0004567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
print(encoded_msg)
binary_data=int(str(encoded_msg)[2:]).to_bytes(BYTES, 'big')

int_data = str(int.from_bytes(binary_data, 'big'))
print(int_data)
data = "0."
for i in range(PRECSION-len(int_data)):
    data+='0'
data+=int_data
print(data)
exit()
"""
# Read message from file
with open('input.txt', 'r') as file:
    original_msg = file.read().strip()

AE = pyae.ArithmeticEncoding(original_msg , PRECSION)

encoded_msg_list = []
last_message_len = len(original_msg) % MESSAGE_SIZE

print("===" , last_message_len)
msg_list=[]
zeros_list=[]
for idx in range(0,len(original_msg) ,MESSAGE_SIZE):
    # Encode the message
    encoded_msg = AE.encode(original_msg[idx:idx+MESSAGE_SIZE])
    msg_list.append(int(str(encoded_msg)[2:]))
    #print(encoded_msg)
    zeros_list.append(len(str(encoded_msg))-2-len(str(int(str(encoded_msg)[2:]))))
    

with open('encoded.bin', 'wb') as file:
    for idx in range(len(msg_list)) :
        file.write(zeros_list[idx].to_bytes(1, 'big'))
        file.write(msg_list[idx].to_bytes(BYTES, 'big'))

decoder, decoded_msg = AE.decode(encoded_msg, MESSAGE_SIZE)

##########################
decoded = ""

with open('encoded.bin', 'rb') as file:
    binary_data = file.read()

offset=0
for idx in range(len(msg_list)):
    leading_zeros = int.from_bytes(binary_data[offset:offset+1], 'big')
    offset+=1
    # Read binary data from file
    int_data = str(int.from_bytes(binary_data[offset:offset+BYTES], 'big'))
    offset+=BYTES

    while len(int_data) < PRECSION:
        int_data+='0'

    data = "0."
    for i in range(leading_zeros):
        data+='0'
    data+=int_data
    #print(data)
    # Decode the message
    decoded_msg = AE.decode( Decimal(data[0]), MESSAGE_SIZE)
    print(decoded_msg)
    decoded +=decoded_msg

if decoded == original_msg:
    print("menio is the best")
else:
    print("fuck menio")


with open('output.txt', 'w') as file:
        file.write(decoded)