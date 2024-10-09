import argparse
import json
import os
import heapq
from abc import ABC, abstractmethod
import zipfile
import io


# The classes for making the huffman tree are transcribed from Java from the following source:
# https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/Huffman.html
class HuffBaseNode(ABC):
    @abstractmethod
    def is_leaf(self):
        pass

    @abstractmethod
    def weight(self):
        pass


# Huffman Leaf Node Class
class HuffLeafNode(HuffBaseNode):

    def __init__(self, element, weight):
        """Constructor"""
        self._element = element
        self._weight = weight

    def value(self):
        """Return the element value"""
        return self._element

    def weight(self):
        """Return the weight of the node"""
        return self._weight

    def is_leaf(self):
        """Return True, since this is a leaf node"""
        return True
    
    def __str__(self):
        return f"Element: {self._element} | Weight: {self._weight}"


# Huffman Internal Node Class
class HuffInternalNode(HuffBaseNode):

    def __init__(self, left, right, weight):
        """Constructor"""
        self._left = left
        self._right = right
        self._weight = weight

    def left(self):
        """Return the left child"""
        return self._left

    def right(self):
        """Return the right child"""
        return self._right

    def weight(self):
        """Return the weight of the node"""
        return self._weight

    def is_leaf(self):
        """Return False, since this is an internal node"""
        return False

    
# Huffman coding tree
class HuffTree:
    def __init__(self, *args):
        """Constructor
        Either takes a single leaf node (char, weight) or two nodes (left, right, weight)
        """
        if len(args) == 2:
            # Leaf node constructor: HuffTree(char, weight)
            element, weight = args
            self._root = HuffLeafNode(element, weight)
        elif len(args) == 3:
            # Internal node constructor: HuffTree(left_node, right_node, weight)
            left, right, weight = args
            self._root = HuffInternalNode(left, right, weight)

    def root(self):
        """Return the root of the Huffman Tree"""
        return self._root

    def weight(self):
        """Return the weight of the tree (which is the weight of the root node)"""
        return self._root.weight()

    def compare_to(self, other):
        """Mimic the compareTo method from Java"""
        if self.weight() < other.weight():
            return -1
        elif self.weight() == other.weight():
            return 0
        else:
            return 1

    def __lt__(self, other):
        """Comparison method for heapq to compare HuffTree objects"""
        return self.weight() < other.weight()

    @staticmethod
    def build_tree(Hheap):
        """Build the Huffman Tree from a min-heap"""
        while len(Hheap) > 1:  # While more than one item left in the heap
            tmp1 = heapq.heappop(Hheap)  # Remove min (smallest tree)
            tmp2 = heapq.heappop(Hheap)  # Remove next min

            # Combine two smallest trees into a new tree
            # If only 2 args, then it is a leaf node and uses that constructor
            # If 3, then an internal node.
            combined_weight = tmp1.weight() + tmp2.weight()
            tmp3 = HuffTree(tmp1.root(), tmp2.root(), combined_weight)
            
            heapq.heappush(Hheap, tmp3)  # Insert new tree back into heap

        return heapq.heappop(Hheap)  # The last remaining tree is the Huffman tree


def traverse_hufftree_binary(node, code=0, length=0, code_dict=None):
    """Traverse the Huffman tree and store binary Huffman codes in a dictionary."""
    if code_dict is None:
        code_dict = {}  # Create a dictionary to hold the binary codes
    
    if node.is_leaf():
        # Use the actual length as formatting
        binary_code = f"{code:0{length}b}"  

        # Store tuple (binary code, bit length)
        code_dict[node.value()] = (binary_code, length)  
    else:
        # Traverse left (append 0 to the binary code)
        traverse_hufftree_binary(node.left(), code << 1, length + 1, code_dict)
        
        # Traverse right (append 1 to the binary code)
        traverse_hufftree_binary(node.right(), (code << 1) | 1, length + 1, code_dict)
    
    return code_dict


def compress_into_binary(text, code_dict, title):
    """Compress text into a binary string using Huffman codes 
    from code_dict and save it as a ZIP file."""
    binary_string = ""
    
    # Iterate over each character in the text and replace it with its binary code
    for char in text:
        if char in code_dict:
            code, length = code_dict[char]  # Get the binary code and its length
            padded_binary = format(int(code, 2), f'0{length}b')
            binary_string += padded_binary  

    # Ensure the binary string is a multiple of 8 bits by padding with zeros if necessary
    padding_length = (8 - len(binary_string) % 8) % 8
    binary_string += "0" * padding_length  

    print(f"Padding length: {padding_length}")


    # Convert the binary string to an integer
    binary_int = int(binary_string, 2)

    # Convert the integer to a byte array using to_bytes()
    byte_length = (len(binary_string) + 7) // 8  
    byte_array = binary_int.to_bytes(byte_length, byteorder="big")

    # Use buffered writing to save the compressed data
    output_file_path = os.path.join(os.getcwd(), f"{title}.zip")

    # Step 4: Prepare the header:
    # Convert the Huffman dictionary into JSON format and encode it to bytes
    huffman_dict_json = json.dumps(code_dict).encode()

    # Store the padding length as a single bye (since it's between 0 -7)
    padding_info_bytes = bytes([padding_length])

    # Define the delimeter to sperate the header from the compressed data
    delimeter = b"\nHEADER_END\n"

    # Step 5: Use io.BYTESIO to handle all data in memory 
    with io.BytesIO() as memory_stream:
    # Write the header: Huffman dictionary, padding info and delimeter

        memory_stream.write(huffman_dict_json)
        memory_stream.write(padding_info_bytes)
        memory_stream.write(delimeter)

        # Write the compressed binary data
        memory_stream.write(byte_array)

        # Get the final compressed data from the memory stream
        compressed_data = memory_stream.getvalue()

    # Step 6: Write the compressed data into a ZIP file
    output_file_path = os.path.join(os.getcwd(), f"{title}.zip")

    with zipfile.ZipFile(output_file_path, "w") as zip_file:
        zip_file.writestr("compressed_data.bin", compressed_data)

    print(f"Compressed binary with header saved to {output_file_path}")

    return compressed_data

def get_argument():
    parser = argparse.ArgumentParser(prog="huffman_decode")
    parser.add_argument("-z", help="Enter the name of the Zip file")
    args = parser.parse_args()

    return args.z


def main():
    # Get the file that will be zipped
    file_to_zip = get_argument()
    print(file_to_zip)

    # Get the path and the actual folder that we will be compressing.
    title = file_to_zip.replace(".txt", "")

    # Open the file and read the frequency of 
    # characters into a dictionary using buffered I/O
    alpha_dict = {}

    # Accumulate the entire file content
    full_text = ""

    # Open the file in binary mode
    with open(file_to_zip, "rb") as file:
        
        # Use BufferedReader to read 64 KB chunks
        buffered_reader = io.BufferedReader(file)
        chunk_size = 64 * 1024

        while True:
            chunk = buffered_reader.read(chunk_size)  
            if not chunk:
                break
            
            # Decode the binary chunk to a UTF-8 string
            text_chunk = chunk.decode("utf-8")
            full_text += text_chunk  # Accumulate file content in full_text
           
            for i in text_chunk:
                if i not in alpha_dict:
                    alpha_dict[i] = 1
                else:
                    alpha_dict[i] += 1

        # Sort the dictionary by the values then arrange by descending 
        sorted_dict_lst = sorted(alpha_dict.items(), key=lambda item: item[1])

        print(sorted_dict_lst)
        
        # First turn each into a Huffman node of element and weight
        huffman_heap = [HuffTree(char, freq) for char, freq in sorted_dict_lst]
        heapq.heapify(huffman_heap)

        huffman_tree = HuffTree.build_tree(huffman_heap)

        root = huffman_tree.root()
        
        # Storing the binary into a dictionary/reference
        binary_dict = traverse_hufftree_binary(root)

        print("===================================")
        for i in binary_dict.items():
            print(i)
        print("===================================")

        # Compress the entire accumulated file content
        compress_into_binary(full_text, binary_dict, title)


if __name__ == "__main__":
    main()