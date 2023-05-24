import pyae
from decimal import Decimal
import struct
from decimal import getcontext
import decimal
#import numpy as np

AE = pyae.ArithmeticEncoding()

# Read message from file
with open('input.txt', 'r') as file:
    original_msg = file.read().strip()

#print("Original Message: {msg}".format(msg=original_msg))

# Encode the message
encoder, encoded_msg = AE.encode(original_msg)
import sys
object_size1 = sys.getsizeof(original_msg)
object_size = sys.getsizeof(encoded_msg)
print(object_size1)
print(object_size)
my_object = "Hello, World!"
object_size = sys.getsizeof(my_object)
print(object_size)

print("Encoded Message: {msg}".format(msg=encoded_msg))
"""
# Convert decimal number to binary
binary_data = struct.pack('!d', encoded_msg)

# Write binary data to file

#binary_data = encoded_msg.to_bytes(4501, byteorder='big')
with open('encoded.bin', 'wb') as file:
    file.write(binary_data)

"""

"""
higher_prec_msg = np.float16(encoded_msg)

# Write to file
with open('encoded.bin', 'wb') as file:
    file.write(higher_prec_msg.tobytes())

# Read binary data from file
with open('encoded.bin', 'rb') as file:
    binary_data = file.read()

#dec_num = decimal.Decimal(int.from_bytes(binary_data, byteorder='big')) / (10 ** decimal.getcontext().prec)

# Unpack binary data to decimal number
encoded_msg = np.frombuffer(binary_data, dtype=np.float16)[0]
#print(struct.unpack('!d', binary_data))
print("Encoded Message: {msg}".format(msg=encoded_msg))
"""
# Decode the message
decoder, decoded_msg = AE.decode(encoded_msg=Decimal(encoded_msg), msg_length=len(original_msg))
#print("Decoded Message: {msg}".format(msg=decoded_msg))

print("Message Decoded Successfully? {result}".format(result=original_msg == decoded_msg))
