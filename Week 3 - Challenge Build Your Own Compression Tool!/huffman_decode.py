import argparse
import json
import zipfile
import os

def unzip_files(zip_folder, unzip_folder_dir):
    if zip_folder:
        print(f"argument passed in: {zip_folder}")

        title = zip_folder.replace(".zip", "")

        with zipfile.ZipFile(zip_folder, "r") as zip_file:

            file_list = zip_file.namelist()
            print(file_list)
            # with zip_file.open("compressed_data.bin") as 

            byte_array = None
            padding_length = None
            huffman_dict = None

            # Iterate through the different folders
            for filename in file_list:
                if filename.endswith(".bin"):
                    with zip_file.open(filename) as compressed_file:
                        byte_array = compressed_file.read()
                        print(f"Read {len(byte_array)} bytes from {filename}.")

                elif filename.endswith(".txt"):
                    with zip_file.open(filename) as padding_file:
                        padding_length = int(padding_file.read())
                        print(f"Padding length: {padding_length}")

                elif filename.endswith(".json"):
                    with zip_file.open(filename) as dict_file:
                        huffman_dict_json = dict_file.read() 
                        huffman_dict = json.loads(huffman_dict_json)  
                        print("Huffman dictionary loaded:") 
                        for char, code in huffman_dict.items():
                            print(f"{char}: {code}")

            if byte_array is not None and huffman_dict is not None:
                print(byte_array)

                # Convert the byte array to a bit string
                bit_string = "".join(f"{byte:08b}" for byte in byte_array)
                # print(bit_string)

                # Remove the padding
                bit_string = bit_string[:-padding_length] if padding_length > 0 else bit_string
                # print(bit_string)

                # Decode using huffman dict
                reverse_huffman_dict = {v[0]: k for k, v in huffman_dict.items()}
                # print(reverse_huffman_dict)

                decoded_text = ""
                temp_bits = ""

                # print(max(huffman_dict.values()[1]))

                for bit in bit_string:
                    temp_bits += bit
                    if temp_bits in reverse_huffman_dict:
                        # print("temp_bits : " + temp_bits)
                        decoded_text += reverse_huffman_dict[temp_bits]
                        temp_bits = ""

                print("decoded text: " + decoded_text)

                full_path = os.path.join(unzip_folder_dir, f"{title}.txt")

                with open(full_path, 'w') as file:
                    file.write(decoded_text)



            else:
                print("Missing files required for deconding.")   


def main():

    # Prep No.1
    # Check to see if there is a folder where the unzipped files will go,
    # And if not, create it
    cwd = os.getcwd()
    unzip_folder_dir = 'Unzip Directory'
    unzipped_main_folder_exists = os.path.isdir(os.path.join(cwd, unzip_folder_dir))

    if not unzipped_main_folder_exists:
        print("Creating folder for unzipped files")
        os.mkdir(unzip_folder_dir)


    # Prep No.2
    # Pass the zip file in as an argument
    parser = argparse.ArgumentParser(prog="huffman_decode")
    parser.add_argument("-u", help="Enter the name of the Zip file")
    args=parser.parse_args()
    zip_folder = args.u

    # Unzip the files
    unzip_files(zip_folder, unzip_folder_dir)







if __name__ == "__main__":
    main()