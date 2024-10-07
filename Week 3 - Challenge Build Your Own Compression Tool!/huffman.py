import argparse
import json
import os
import heapq
from abc import ABC, abstractmethod
import zipfile



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
        # If it's a leaf node, store the character's binary code and its bit length
        # binary_code = bin(code)[2:]
        binary_code = f'{code:0{length}b}'  # Use the actual length as formatting
        print(bin(code))
        # code_dict[node.value()] = (int(binary_code), length)  # Store tuple (binary code, bit length)
        code_dict[node.value()] = (binary_code, length)  # Store tuple (binary code, bit length)
    else:
        # Traverse left (append 0 to the binary code)
        traverse_hufftree_binary(node.left(), code << 1, length + 1, code_dict)
        
        # Traverse right (append 1 to the binary code)
        traverse_hufftree_binary(node.right(), (code << 1) | 1, length + 1, code_dict)
    
    return code_dict


# # For traversing the tree and printing as a string:
# def traverse_hufftree(node, path=""):
#     """Traverse the Huffman tree and print the character along with its code."""
#     if node.is_leaf():
#         # If it's a leaf node, print the character and its Huffman code
#         print(f"Character: {node.value()} | Huffman Code: {path}")
#     else:
#         # If it's an internal node, traverse left and right with updated path
#         traverse_hufftree(node.left(), path + "0")   # Traverse left and append "0"
#         traverse_hufftree(node.right(), path + "1")  # Traverse right and append "1"

def compress_into_binary(text, code_dict, title):
    """Compress text into a binary string using Huffman codes from code_dict and save it as a ZIP file."""
    binary_string = ""
    
    # Iterate over each character in the text and replace it with its binary code
    for char in text:
        if char in code_dict:
            code, length = code_dict[char]  # Get the binary code and its length
            padded_binary = format(int(code, 2), f'0{length}b')
            binary_string += padded_binary  

    # Ensure the binary string is a multiple of 8 bits by padding with zeros if necessary
    padding_length = (8 - len(binary_string) % 8) % 8
    binary_string += '0' * padding_length  

    # Convert the binary string to an integer
    binary_int = int(binary_string, 2)

    # Convert the integer to a byte array using to_bytes()
    byte_length = (len(binary_string) + 7) // 8  
    byte_array = binary_int.to_bytes(byte_length, byteorder='big')

    # Create a ZIP file to save the compressed data
    # output_file_path = os.path.join(os.getcwd(), "compressed_output.zip")
    output_file_path = os.path.join(os.getcwd(), f"{title}.zip")
    
    with zipfile.ZipFile(output_file_path, 'w') as zip_file:
        # Save the compressed data as a binary file inside the ZIP
        zip_file.writestr("compressed_data.bin", byte_array)
        
        # Optionally, you can save the padding length for decompression purposes
        zip_file.writestr("padding_length.txt", str(padding_length).encode())
    
        # Save the Huffman dictionary as a JSON file
        zip_file.writestr("huffman_dict.json", json.dumps(code_dict).encode())

    print(f"Compressed binary saved to {output_file_path}")
    print(binary_string)

    return binary_string

# Argument parse function
# Text files to be parsed will be passed as arguments
def get_argument():
    parser = argparse.ArgumentParser(prog="huffman_decode")
    parser.add_argument("-z", help="Enter the name of the Zip file")
    args=parser.parse_args()

    return args.z


def main():

    # Get the file that will be zipped
    file_to_zip = get_argument()
    print(file_to_zip)

    # Get the path and the actual folder that we will be compressing.
    title = file_to_zip.replace(".txt", "")

    # Open the file and read the frequency of characters into a dictionary
    alpha_dict = {}
    
    with open(file_to_zip, "r", encoding="utf8") as file:
        
        read_file = file.read()

        for i in read_file:
            if i not in alpha_dict:
                alpha_dict[i] = 1
            else:
                alpha_dict[i] += 1

        # Sort the dictionary by the values then arrange by descending 
        sorted_dict_lst = sorted(alpha_dict.items(), key= lambda item : item[1])

        print(sorted_dict_lst)
        # print("Char Frequency of File:")
        # # for i in sorted_dict_lst:
        # #     print(i)
        
        # First turn each into a huffman node of element and weight
        huffman_heap = [HuffTree(char,freq) for char, freq in sorted_dict_lst]
        # print(len(huffman_heap))
        # for i in huffman_heap:
        #     print(i)
        heapq.heapify(huffman_heap)

        huffman_tree = HuffTree.build_tree(huffman_heap)
        # build_tree(huffman_heap)
        # build_tree(sorted_dict_lst)

        # print(f"Root weight of the final Huffman tree: {huffman_tree.weight()}")

    
        # Assuming `hufftree` is your HuffTree object
        root = huffman_tree.root()
        
        # We can double check and print out what the codes are going to be
        # traverse_hufftree(root)

        # Storing the binary into a dictionary/reference
        binary_dict = traverse_hufftree_binary(root)

        print("===================================")
        # print(binary_dict)
        for i in binary_dict.items():
            print(i)
            # print(type(i[1][0]))
        print("===================================")

        # for i in read_file:
        #     print(f"{i} : {binary_dict[i]}")
            # binary_dict += binary_dict[i][0]
       
        # Lets compress it!
        compress_into_binary(read_file, binary_dict, title)


        # print(binary_arr)
        # binary_string = compress_into_binary(read_file, binary_dict)


if __name__ == "__main__":
    main()