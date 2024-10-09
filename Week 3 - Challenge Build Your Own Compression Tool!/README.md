

# Week 3 Challenge: Build Your Own Compression Tool!

This week is a little dip into data compression via the creation of my own Huffman coding tool. 

This challenge helped to advance my skills by way of:
- Learning about tree data structures and queues
- Practicing bit manipulation and file I/O
- Gaining insight into how real-world compression algorithms work.


## These Features will be implemented:

### Step 0: Setup 
 - Python
 - The goal is to compress Les Misérables by Victor Hugo available here: https://www.gutenberg.org/files/135/135-0.txt 


### Step 1: Character Frequency Count
The program accepts a filename as input.
   ```bash 
   > python huffman.py -z test.txt 
   ```

A frequency table is built. In as in our test.txt example:
   ```bash 
   [('A', 1), ('y', 1), ('n', 1), ('g', 1), ('t', 1), ('u', 2), ('r', 2), ('b', 2), ('a', 2), ('s', 2), ('l', 3), ('o', 3), ('e', 3), (' ', 6)]
   ```

### Step 2: Build the Huffman Tree
These classes are the heavy lifters in building the Huffman Tree:
   ```bash 
   class HuffBaseNode(ABC)
   class HuffLeafNode(HuffBaseNode)
   class HuffInternalNode(HuffBaseNode)
   class HuffTree
   ```
In this process they :
- Create a leaf node for each character and its frequency
- Add all nodes to a priority queue
- While there's more than one node in the queue:
  - Remove the two nodes with the lowest frequencies
  - Create a new internal node with these two as children
  - Add the new node back to the queue

### Step 3: Generate the Prefix Code Table and Write the Header
The prefix code table is generated.
   ```bash 
    (' ', ('00', 2))
    ('o', ('010', 3))
    ('g', ('0110', 4))
    ('r', ('0111', 4))
    ('u', ('1000', 4))
    ('t', ('10010', 5))
    ('y', ('10011', 5))
    ('n', ('10100', 5))
    ('A', ('10101', 5))
    ('b', ('1011', 4))
    ('s', ('1100', 4))
    ('a', ('1101', 4))
    ('l', ('1110', 4))
    ('e', ('1111', 4))
   ```
Although this could have been included into  a header section for the output file, This tree structure will be included as a JSON file in the compressed ZIP file.

### Step 4: Prepare the header:
   ```bash 
    huffman_dict_json = json.dumps(code_dict).encode()
    padding_info_bytes = bytes([padding_length])
    delimeter = b"\nHEADER_END\n"
   ```

### Step 5: Use io.BYTESIO to handle all data in memory 
   ```bash 
    with io.BytesIO() as memory_stream:
        memory_stream.write(huffman_dict_json)
        memory_stream.write(padding_info_bytes)
        memory_stream.write(delimeter)
   ```

### Step 6: Encode and Write the Compressed Data

The text is encoded using the code table. The compressed .bin file is put into a zipped folder. 

### Step 7: Decoding

To decode the file, use this command by passing in the zip folder as the argument:

   ```bash 
   > python huffman_decode.py -u test.zip 
   ```

The reverse from the previous steps is carried out; the code table is used to decode and write the decompressed data into a text file.


### Final Boss Step: Large File Handling Consideration
Optimization has been considered to more efficiently handle files larger than available RAM:
- Read and write in chunks - 64KB at a time
- Use buffered I/O

**N.B.** - Buffered Streams have been utilized so that the entire file is not read into memory at once. Bitwise operations were used for actual compression, with the compressed data being written in binary mode, not as text. I have included a different version without the header, instead storing it as a Json file. The results for this method were comparable to the header version.


### Results!

So how well does it work? For the small test data, the results were negligible, but for the full Les Misérables text, the compression was starting to make a difference.
- Original size = 3291 KB
- Compressed size = 1879 KB

$$ 
\text{Compression Ratio} = \frac{\text{Compressed Size}}{\text{Original Size}} 
$$  

So for the ratio:
The compression ratio is 1879 / 3291 ≈ 0.57 

Or 57%. 

While this is in no way outstanding and only marginally reaches closer to 57% for a file twice the size of Les Mis, proof-of-concept was the focus of this week: A file is read, compressed using Huffman coding and subsequently decompressed. While there are many optimizations to be made, this was a fun first dip into data compression!


