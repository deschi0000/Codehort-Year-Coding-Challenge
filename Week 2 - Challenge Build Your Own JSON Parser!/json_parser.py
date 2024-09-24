import os

def main():
    # TODO:
    # fail 3 - keys must be quoted
    # fail 12 - illegal invocation
    # fail 18 - too deep
    # fail 20 - double colon
    # fail 22 - colon instead of comma
    # fail 23 - bad value
    # fail 24 - single quote
    # fail 25 - tab characters
    # fail 26 - tab/ chars
    # fail 27 - Line/ break
    # fail 28 - Line break
    # fail 29 - [0e]
    # fail 30 - [0e+]
    # fail 31 - [0e+-1]
    
    folder_names = ['unit-test', 'test-files']

    cwd = os.getcwd()
    file_path = os.path.join(cwd, *folder_names)

    print("PATH:    " + file_path)

    pass_file = os.path.join(file_path, 'pass2.json')
    fail_file = os.path.join(file_path, 'fail33.json')   
    
    with open(fail_file, 'r') as file:
    # with open(pass_file, 'r') as file:
        # for f in file.read():
        #     print(f)
        # print(file.read())
        file = file.read().strip()
        print("==============================================")
        print(file)
        print("==============================================")

        # print(file[0])
        # if file[0] == "{" or file[0] == "[":
        #     print("match")

        # TODO: CHeck for tabs
        # if "\   " or "   " in file:
        #     return "Ivalid Json: Contains Tabs"
        
        # TODO: Check for newlines

        # TODO: Check to see if it opens with { or [
        if file[0] not in ("{", "["):
            return "Invalid Json: No starting { or ["

        # TODO: Check to see if it closes with } or ]
        if file[-1] not in ("}","]"):
            return "Invalid Json: No ending } or ]"
        
        file_length = len(file)
        array_counter = 0
        bracket_counter = 0

        for i in range(file_length):

            if file[i] == "{":
                bracket_counter += 1
                if ":" not in file:
                    return "Invalid Json: Missing colon"
            if file[i] == "}":
                bracket_counter -= 1

            if file[i] == "[":
                array_counter += 1
            if file[i] == "]":
                array_counter -= 1 

            # if file[i] == "\\" and file[i +1] != "\\":
            #     return "Line break"
            # TODO: Illegal escape chars
            if file[i] == "\\":
                if file[i+1] not in ("\\"):
                    return "Invalid Json: Invalid escape chars"

            # TODO: Nums cannot be Hex
            # From reading the file, every number is a string!
            # if type(file[i]) == int:
            #     print("Its an int")

            # TODO: Extra comma
            if file[i] == ",":
                # if file[i+1] or file[i-1] not in ("\"", " "):
                #     return "Invalid Json: Extra Comma"
                arr = file.split(",")
                check_extra_comma_arr = [i.strip() for i in arr]
                print(check_extra_comma_arr)
                for i in check_extra_comma_arr:
                    if i in ("[","]","{","}"):
                        return "Invalid Json: Extra Comma"
            
            # TODO: Check for leading zeros 
            if file[i] == "0":
                if file[i+1] in ("1","2","3","4","5","6","7","8","9"):
                    return "Invalid Json: Leading Zeros"
          
        # print("Array Counter: " + str(array_counter))
        # print("Bracket Counter: " + str(bracket_counter))

        if array_counter != 0:
            return "Invalid Json: Not enough closing arrays / Mismatch"
        elif bracket_counter != 0:
            return "Invalid Json: Not enough closing brackets / Mismatch"
        
        # TODO: Check for Illegal expressions
        check_illegal_expression_arr = [i.strip() for i in file.split(":")]
        for i in check_illegal_expression_arr:
            if "\"" not in i:
                if "+" in i or "-" in i or "*" in i or "/" in i:
                    return "Invalid Json: Illegal Expression"
                
if __name__ == '__main__':
    print(main())

