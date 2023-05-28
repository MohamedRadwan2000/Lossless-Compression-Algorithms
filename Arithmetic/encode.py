from decimal import Decimal
from ArithmeticDecoding import ArithmeticDecoding

from ArithmeticEncoding import ArithmeticEncoding
 
PRECSION = 101
BYTES =  42
input_file = 'input.txt'
encoded_file = 'encoded.bin'

def convert_decimal_to_bytes(encoded_msg):
    digits = int(str(encoded_msg)[2:])
    zeros = len(str(encoded_msg))-2-len(str(int(str(encoded_msg)[2:])))
    return digits, zeros

def choose_message_size(original_msg, AE, PRECSION):
    AD = ArithmeticDecoding(AE.probability_table , PRECSION)
    for i in range(86, 30, -1):
        flag = False
        end = min(10000, len(original_msg))
        for j in range(0,end , i):
            #print(j)
            temp_original = original_msg[j:j+i]
            temp_decoded = b''.join(AD.decode(AE.encode(temp_original), i)[0:len(temp_original)])
            if j + i >= end and temp_decoded == temp_original:
                flag = True
            elif temp_decoded != temp_original:
                break
        if flag:
            return i


# Read message from file
with open(input_file, 'rb') as file:
    original_msg = file.read()

AE = ArithmeticEncoding(original_msg , PRECSION)

MESSAGE_SIZE = choose_message_size(original_msg, AE, PRECSION)
print("MESSAGE_SIZE: ", end = '')
print(MESSAGE_SIZE)
last_message_len = len(original_msg) % MESSAGE_SIZE
msg_list=[]
zeros_list=[]
for idx in range(0,len(original_msg) ,MESSAGE_SIZE):
    # Encode the message
    encoded_msg = AE.encode(original_msg[idx:idx+MESSAGE_SIZE])
    digits, zeros = convert_decimal_to_bytes(encoded_msg)
    msg_list.append(digits)
    zeros_list.append(zeros)

with open(encoded_file, 'wb') as file:
    
    file.write(PRECSION.to_bytes(2, 'big'))
    file.write(BYTES.to_bytes(2, 'big'))
    file.write(MESSAGE_SIZE.to_bytes(2, 'big'))
    file.write(last_message_len.to_bytes(2, 'big'))
    file.write(AE.probability_table_size.to_bytes(2, 'big'))
    file.write(AE.probability_table_entity_precsion.to_bytes(2, 'big'))
    file.write(AE.probability_table_entity_size.to_bytes(2, 'big'))

    for key, value in AE.probability_table.items():
        file.write(key)
        digits, zeros = convert_decimal_to_bytes(value)
        file.write(zeros.to_bytes(1, 'big'))
        file.write(digits.to_bytes(AE.probability_table_entity_size, 'big'))

    for idx in range(len(msg_list)) :
        file.write(zeros_list[idx].to_bytes(1, 'big'))
        file.write(msg_list[idx].to_bytes(BYTES, 'big'))

print("file encoded successfully")
