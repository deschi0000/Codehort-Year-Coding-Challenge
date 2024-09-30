import os
import re

# class JSONParseError(Exception):
#     """Base class for exceptions in JSON parsing."""
#     pass

# class MissingBracketError(JSONParseError):
#     """Raised when there are unmatched brackets."""
#     def __init__(self):
#         super().__init__("Invalid JSON: Not enough closing brackets / Mismatch")

# class InvalidSyntaxError(JSONParseError):
#     """Raised for syntax errors in the JSON."""
#     def __init__(self, message):
#         super().__init__(f"Invalid JSON: {message}")




# TODO:
# fail 1  - "A JSON payload should be an object or array, not a string."
# fail 2  - ["Unclosed array"
# fail 3  - {unquoted_key: "keys must be quoted"}                 ****** >>>
# fail 4  - ["extra comma",]
# fail 5  - ["double extra comma",,]
# fail 6  - [   , "<-- missing value"]
# fail 7  - ["Comma after the close"],
# fail 8  - ["Extra close"]]
# fail 9  - {"Extra comma": true,}
# fail 10 - {"Extra value after close": true} "misplaced quoted value"
# fail 11 - {"Illegal expression": 1 + 2}
# fail 12 - {"Illegal invocation": alert()}                       ****** >>>
# fail 13 - {"Numbers cannot have leading zeroes": 013}
# fail 14 - {"Numbers cannot be hex": 0x14}                       ****** >>>
# fail 15 - ["Illegal backslash escape: \x15"]                    ****** >>> 
# fail 16 - [\naked]                                              ****** >>>
# fail 17 - ["Illegal backslash escape: \017"]
# fail 18 - [[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]
# fail 19 - {"Missing colon" null}                                ****** >>>
# fail 20 - {"Double colon":: null}
# fail 21 - {"Comma instead of colon", null}                      ****** >>>
# fail 22 - ["Colon instead of comma": false]                     ****** >>>
# fail 23 - ["Bad value", truth]                                  ****** >>>
# fail 24 - ['single quote']                                      ****** >>>
# fail 25 - ["	tab	character	in	string	"]                    ****** >>>
# fail 26 - ["tab\   character\   in\  string\  "]                ****** >>>
# fail 27 - Line/ break                                           ****** >>>
# fail 28 - Line break                                            ****** >>>
# fail 29 - [0e]                                                  ****** >>>
# fail 30 - [0e+]
# fail 31 - [0e+-1]
# fail 32 - {"Comma instead if closing brace": true,
# fail 33 - ["mismatch"}

def test_valid_json(file_path):

    # folder_names = ['unit-test', 'test-files']

    # cwd = os.getcwd()
    # file_path = os.path.join(cwd, *folder_names)

    # print("PATH:    " + file_path)

    # pass_file = os.path.join(file_path, 'pass5.json')
    # fail_file = os.path.join(file_path, 'fail25.json')   
    
    # Missing comma bug 18, 24, 25, 33
    # print(file_path)

    with open(file_path, 'r') as file:
    # with open(pass_file, 'r') as file:
        uncleaned_content = file.read().strip()

        digit_sequence = []  # To collect digits outside quotes
        in_brackets = False
        cleaned_list = []
        escaped = False  # To handle escape sequences

        for i in range(len(uncleaned_content)):
            char = uncleaned_content[i]
            # print("THIS: " + char)

            if escaped and not in_brackets:
                return "Invalid Json: Illegal Naked"

            # Handle escaped backslashes
            if escaped:
                cleaned_list.append(char)
                escaped = False
                continue

            # if char == "\\":
                # This means the next character is escaped, so we skip handling it specially
                # escaped = True
                # cleaned_list.append(char)
                # continue

            # Check if it's a backslash
            if char == "\\":
                # Look at the next character
                next_char = uncleaned_content[i + 1]

                # Check if it's a valid escape character
                if next_char not in ("'", "\\", "n", "r", "t", "b", "f", '"',"/","u"):
                    # Check if it's the start of an illegal octal sequence
                    if next_char.isdigit() and uncleaned_content[i + 1:i + 4].isdigit():
                        return "Invalid Json: Illegal octal escape sequence"
                    else:
                        return "Invalid Json: Illegal escape character"
                
                escaped = True
                cleaned_list.append(char)
                continue


            if char == " " and not in_brackets:
                continue

            if char == "\n" and not in_brackets:
                continue

            elif char == "\n" and in_brackets:
                return "Invalid Json: Illegal Line Break"

            if char == "\"" and not escaped:
                in_brackets = not in_brackets  # Toggle the in_brackets state

            # Preserve spaces inside quotes
            if char == " " and in_brackets:
                cleaned_list.append(char)  # Keep the space
                continue

            # Handle digit sequences outside of quotes and checking special character numbers
            if char.isdigit() and not in_brackets and uncleaned_content[i - 1] not in ("+","-","e"):
                digit_sequence.append(char)
            else:
                # If not a digit, we check the current digit sequence for leading zeros
                if digit_sequence and digit_sequence[0] == "0" and len(digit_sequence) > 1:
                    # print(f"Found leading zero in number: {''.join(digit_sequence)}")
                    # Handle the error as needed (raise exception, continue, etc.)
                    return f"Invalid Json: Found leading zero in number: {''.join(digit_sequence)}"
                
                # Clear the digit sequence as we're moving past digits
                digit_sequence = []

            cleaned_list.append(char)

            # # Final check for any trailing digit sequence
            # if digit_sequence and digit_sequence[0] == "0" and len(digit_sequence) > 1:
            #     return f"Invalid Json: Found leading zero in number: {''.join(digit_sequence)}"

        content = "".join(cleaned_list)

        print("==============================================")
        print(content)
        print("==============================================")

        # TODO: Check to see if it opens with { or [
        if content[0] not in ("{", "["):
            return "Invalid Json: No starting { or ["
            # raise InvalidSyntaxError("No starting { or [")

        # TODO: Check to see if it closes with } or ]
        if content[-1] not in ("}","]"):
            return "Invalid Json: No ending } or ]"
        
        file_length = len(content)
        array_counter = 0
        bracket_counter = 0

        # Check for the double colon
        pattern = r'(\")(:{2,})'
        if re.search(pattern, content):         
            return "Invalid Json: Double Colon"
        
        # Check for illegal invocations
        pattern = r'[a-zA-Z]{2,}\(\)'
        if re.search(pattern, content):         
            return "Invalid Json: Illegal Invocation"

        pattern = r'\[\d*[a-zA-Z](\+|\-)*\d*\]'
        if re.search(pattern, content):         
            return "Invalid Json: Illegal Invocation"
        
        pattern_bad_value = r'[\[,]\s*(\w+)\s*[\],]'
        match = re.search(pattern_bad_value, content)
        if match:
            word = match.group(1)  # Capture the matched word
            print("MATCH: " + word)
            if word in ("true", "false", "null"):
                print(f"Valid word '{word}' found in content")
            else:
                return "Invalid Json: Illegal Invocation"      


        temp_string = []

        # Check if in brackets
        brackets = False
        wait_to_skip = False
        index_to_skip_to = 0

        for i in range(file_length):

            char = content[i]
            # print("Char: " + char)
            # print("In Brackets: " + str(in_brackets))

            # if not wait_to_skip or i == index_to_skip_to:
            #     wait_to_skip = False

            if bracket_counter > 0 and bracket_counter < 2: # takes into account not nested
                colon_pattern = r'\"\S*\:'
                if not re.search(colon_pattern, content):         
                    return "Invalid Json: Missing Colon"

                
            if array_counter > 0 and array_counter < 2: # takes into account not nested
                comma_pattern = r'\"\S*\,|\S*\,' 
                comma_pattern_single = r'\[\"\S*?]'
                if not re.search(comma_pattern, content):
                    if not re.search(comma_pattern_single, content):         
                        return "Invalid Json: Missing Comma"
                    else:
                        continue
                

                # # print(char)
                # if char.isalpha() and content[i - 1] != "\"" and not char.isdigit() and brackets is False:
                #     value_to_test = []
                #     for j in range(i, len(content)):
                #         if content[j] in (",","]","}","."):
                #             if content[j] == "]":
                #                 array_counter -= 1
                #                 break
                #             elif content[j] == "}":
                #                 bracket_counter -1
                #                 break
                #             else:
                #                 break
                #         else:
                #             value_to_test.append(content[j])

                #     word_to_test = "".join(value_to_test)
                #     # print("Testing: ---- " + word_to_test)

                #     # print("is it in?: " + word_to_test not in ("true","false","null"))

                #     if word_to_test in ("true","rue","ue","e","false","null"):
                #         # index_to_skip_to = j
                #         # wait_to_skip = True
                #         continue
                #     else:
                        # return "Invalid Json: Bad Value"

            if char == "\"" and not content[i - 1] == "\\":
                brackets = not brackets 

            if brackets is False:
                
                if brackets is True or i == len(content) - 1:
                    string_to_check = "".join(temp_string)
                    hex_pattern = r'0x[0-9a-fA-F]+|[0-9a-fA-F]+^'
                    single_quote_pattern = r'[a-zA-Z]*\''
                    if re.search(hex_pattern, string_to_check): 
                        return "Ivalid Json: Hex Oustide of a string"
                    elif re.search(single_quote_pattern, string_to_check): 
                        return "Ivalid Json: Single Quotes"       
                    else:
                        temp_string = []
                else:
                    temp_string.append(char)
            
            if char == "{":
                bracket_counter += 1
                # if ":" not in content:
                #     return "Invalid Json: Missing colon"

            if char == "}":
                bracket_counter -= 1

            if char == "[":
                array_counter += 1
                if array_counter > 19:                    # Test the depth of an array
                    return "Invalid Json: Too Deep"
            if char == "]":
                array_counter -= 1 
            
            # Check for any invalid line breaks
            if (char.isalpha() or char == "\\") and content[i + 1] == "\n":
                return "Invalid Json: Invalid line break"
            
            if char.isalpha() and content[i + 1] == "\t":
                return "Invalid Json: Invalid tab break"
            
            # Check for extra commas
            if not brackets:
                if char == "," and i + 1 < file_length and (content[i + 1] == "," or content[i + 1] in ("]","}") ):
                        return "Invalid Json: Extra Comma"
                
                if char == "," and i + 1 < file_length and (content[i - 1] == "," or content[i - 1] == "["):
                        return "Invalid Json: Missing Value"
                
                # Check for missing colons, commas (19)
                if char == "\"" and i + 1 < file_length and content[i + 1] not in (":",",","]","}"):
                    return "Invalid Json: Missing colon"
                


        # print("arr: " + str(array_counter))
        # print("brack: " + str(bracket_counter))

        if array_counter != 0:
            return "Invalid Json: Not enough closing arrays / Mismatch"
        elif bracket_counter != 0:
            return "Invalid Json: Not enough closing brackets / Mismatch"
        

        
        # TODO: Check for Illegal expressions
        check_illegal_expression_arr = [i.strip() for i in content.split(":")]
        for i in check_illegal_expression_arr:
            if "\"" not in i:
                if "+" in i or "-" in i or "*" in i or "/" in i:
                    return "Invalid Json: Illegal Expression"
                

    return "Valid Json File"
                
# if __name__ == '__main__':
#     print(main())
#     # main()




