import filecmp
def compress_lzw(data):
    dictionary = {chr(i): i for i in range(256)}
    result = []
    w = ""
    for c in data:

        wc = w + chr(c)
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = len(dictionary)
            w = chr(c)
    if w:
        result.append(dictionary[w])
    return result

def decompress_lzw(data):
    dictionary = {i: chr(i) for i in range(256)}
    result = b""
    prev = chr(data[0])
    result += bytes(prev, 'utf-8')
    for curr in data[1:]:
        if curr in dictionary:
            entry = dictionary[curr]
        elif curr == len(dictionary):
            entry = prev + prev[0]
        else:
            raise ValueError("Invalid compressed data")
        result += bytes(entry, 'utf-8')

        dictionary[len(dictionary)] = str(prev) + entry[0]
        prev = entry
    return result


input_file = 'input.txt'
compressed_file = 'compressed_file.lzw'
output_file = 'output_file.txt'

# read input file
with open(input_file, 'rb') as f:
    data = f.read()

# compress data using LZW algorithm
compressed_data = compress_lzw(data)

# write compressed data to compressed file
with open(compressed_file, 'wb') as f:
    for code in compressed_data:
        f.write(code.to_bytes(2, byteorder='big'))

# read compressed data from compressed file
with open(compressed_file, 'rb') as f:
    compressed_data = []
    while True:
        code = f.read(2)
        if not code:
            break
        code = int.from_bytes(code, byteorder='big')
        compressed_data.append(code)

# decompress data using LZW algorithm
decompressed_data = decompress_lzw(compressed_data)

# write decompressed data to output file
with open(output_file, 'wb') as f:
    f.write(decompressed_data)

print("Is the Decompressed file equals the Original file? ",filecmp.cmp('input.txt', 'output_file.txt'))