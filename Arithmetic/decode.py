from decimal import Decimal

from ArithmeticDecoding import ArithmeticDecoding

encoded_file = 'encoded.bin'
output_file = 'output.txt'

def convert_bytes_to_decimal(binary_data, offset, BYTES, PRECSION):
    leading_zeros = int.from_bytes(binary_data[offset:offset+1], 'big')
    offset+=1
    int_data = str(int.from_bytes(binary_data[offset:offset+BYTES], 'big'))
    offset+=BYTES

    while len(int_data) < PRECSION:
        int_data+='0'

    data = "0."
    for i in range(leading_zeros):
        data+='0'
    data+=int_data
    return Decimal(data) , offset

def test (original_file, decoded_file):
    with open(original_file, 'r') as file:
        original_message = file.read()

    with open(decoded_file, 'r') as file:
        decoded = file.read()
    if decoded == original_message:
        print("menio is the best")
    else:
        print("fuck menio")
 
decoded = ""

with open(encoded_file, 'rb') as file:
    binary_data = file.read()

offset=0
PRECSION = int.from_bytes(binary_data[offset:offset+2], 'big')
offset += 2
BYTES =  int.from_bytes(binary_data[offset:offset+2], 'big')
offset += 2
MESSAGE_SIZE = int.from_bytes(binary_data[offset:offset+2], 'big')
offset += 2
last_message_len = int.from_bytes(binary_data[offset:offset+2], 'big')
offset += 2

probability_table_size = int.from_bytes(binary_data[offset:offset+1], 'big')
offset += 1
probability_table_entity_precsion = int.from_bytes(binary_data[offset:offset+2], 'big')
offset += 2
probability_table_entity_size = int.from_bytes(binary_data[offset:offset+2], 'big')
offset += 2

probability_table = {}
for idx in range (probability_table_size):
    key = binary_data[offset:offset+1].decode('utf-8')
    offset += 1
    value, offset = convert_bytes_to_decimal(binary_data, offset, probability_table_entity_size, probability_table_entity_precsion)
    probability_table[key] = value


AD = ArithmeticDecoding(probability_table , PRECSION, MESSAGE_SIZE)

while offset < len(binary_data):
    data, offset = convert_bytes_to_decimal(binary_data, offset, BYTES, PRECSION)
    decoded_msg = AD.decode(data)
    decoded +=decoded_msg

tail = -(MESSAGE_SIZE - last_message_len)
if (last_message_len != 0):
    decoded = decoded[: -(MESSAGE_SIZE - last_message_len)]

with open(output_file, 'w') as file:
        file.write(decoded)
print("file decoded successfully")

test('input.txt', 'output.txt')
