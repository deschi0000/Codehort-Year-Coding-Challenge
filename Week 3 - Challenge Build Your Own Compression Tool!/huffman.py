import os

def main():

    # Get the current working directory and the list of items there
    cwd = os.getcwd()
    list_dir = os.listdir(cwd)

    # Retrieve only txt files.
    txt_files = [f for f in list_dir if f.endswith(".txt")]

    # Get the path and the actual folder that we will be decompressing.
    file_with_path = os.path.join(cwd, txt_files[0])

    # Open the file and read the frequency of characters into a dictionary
    alpha_dict = {}
    
    with open(file_with_path, 'r', encoding="utf8") as file:
        
        read_file = file.read()

        for i in read_file:
            if i not in alpha_dict:
                alpha_dict[i] = 1
            else:
                alpha_dict[i] += 1


        # Sort the dictionary by the values then arrange by descending 
        sorted_dict_lst = sorted(alpha_dict.items(), key= lambda item : item[1])
        sorted_dict_lst.reverse()

        print("===================================")
        print("Char Frequency of File:")
        # print(sorted_dict_lst)
        for i in sorted_dict_lst:
            print(i)
        print("===================================")


    # put the dictionary into a sorted list where the lowest frequency is first and the highest is last

    return










if __name__ == '__main__':
    main()