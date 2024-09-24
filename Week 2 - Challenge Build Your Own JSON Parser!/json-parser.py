import os

def main():
    
    folder_names = ['unit-test', 'test-files']

    cwd = os.getcwd()
    file_path = os.path.join(cwd, *folder_names)

    print("PATH:    " + file_path)

    pass_file = os.path.join(file_path, 'pass2.json')
    fail_file = os.path.join(file_path, 'fail21.json')   
    
    with open(fail_file, 'r') as file:
    # with open(pass_file, 'r') as file:
        # for f in file.read():
        #     print(f)
        # print(file.read())
        file = file.read().strip()
        print(file)
        # print(file[0])
        # if file[0] == "{" or file[0] == "[":
        #     print("match")

        # TODO: CHeck for tabs
        # if "\   " or "   " in file:
        #     return "Ivalid Json: Contains Tabs"
        
        # TODO: Check for newlines
        # if "\n" or ""
        if ":" not in file:
            return "Invalid Json: Missing colon"

        # TODO: Check to see if it opens with { or [
        if file[0] not in ("{", "["):
            return "Invalid Json: No starting { or ["

        # TODO: Check to see if it closes with } or ]
        if file[-1] not in ("}","]"):
            return "Invalid Json: No ending } or ]"

        # if file[0] == "{":
        #     if file[-1] != "}":
        #         return "Invalid Json"

        # if file[0] == "[":
        #     if file[-1] != "]":
        #         return "Invalid Json"
        file_length = len(file)


        array_counter = 0
        bracket_counter = 0

        for i in range(file_length):

            if file[i] == "{":
                bracket_counter += 1
            if file[i] == "}":
                bracket_counter -= 1

            if file[i] == "[":
                array_counter += 1
            if file[i] == "]":
                array_counter -= 1 

            # if file[i] == "\\" and file[i +1] != "\\":
            #     return "Line break"

        # print("Array Counter: " + str(array_counter))
        # print("Bracket Counter: " + str(bracket_counter))

        if array_counter != 0:
            return "Invalid Json: Not enough closing arrays"
        elif bracket_counter != 0:
            return "Invalid Json: Not enough closing brackets"
    # RULES
    # Json must start be enclosed with [], or {}
    # 



if __name__ == '__main__':
    print(main())


# pass_json = {
#     "JSON Test Pattern pass3": {
#         "The outermost value": "must be an object or array.",
#         "In this test": "It is an object."
#     }
# }


# fail_json = {"Illegal expression": 1 + 2}

