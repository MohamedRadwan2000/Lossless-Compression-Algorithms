import filecmp
import os

import bitarray
import time


def compress_lzw(data):
    dictionary = {chr(i): i for i in range(256)}
    result = []
    prev = ""
    for current in data:
        concat = prev + current
        if concat in dictionary:
            prev = concat
        else:
            result.append(dictionary[prev])
            dictionary[concat] = len(dictionary)
            prev = current
    if prev:
        result.append(dictionary[prev])
    return result


def decompress_lzw(data):
    dictionary = {i: chr(i) for i in range(256)}
    result = []
    prev = chr(data[0])
    result += prev
    for curr in data[1:]:
        if curr in dictionary:
            entry = dictionary[curr]
        elif curr == len(dictionary):
            entry = prev + prev[0]
            print("Entry==> ", entry)
        else:
            raise ValueError("Invalid compressed data")
        result += entry

        dictionary[len(dictionary)] = str(prev) + entry[0]
        prev = entry
    return "".join(result)


input_file = 'input.txt'
compressed_file = 'compressed_file.lzw'
output_file = 'output_file.txt'

# read input file
with open(input_file, 'r') as f:
    data = f.read()
# compress data using LZW algorithm
compressed_data = compress_lzw(data)
# Start timer
start_time = time.time()
# write compressed data to compressed file
with open(compressed_file, 'wb') as f:
    for code in compressed_data:
        f.write(code.to_bytes(4, byteorder='big'))

# read compressed data from compressed file
with open(compressed_file, 'rb') as f:
    compressed_data = []
    while True:
        code = f.read(4)
        if not code:
            break
        code = int.from_bytes(code, byteorder='big')
        compressed_data.append(code)

# decompress data using LZW algorithm
decompressed_data = decompress_lzw(compressed_data)

# write decompressed data to output file
with open(output_file, 'w') as f:
    f.write(decompressed_data)

end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
print("Is the Decompressed file equals the Original file? ", filecmp.cmp(input_file, output_file))

original_file_size = os.path.getsize(input_file)
compressed_file_size = os.path.getsize(compressed_file)
ratio = (compressed_file_size/original_file_size)

print(f"Compression Ratio = :{ratio:.2%}")
