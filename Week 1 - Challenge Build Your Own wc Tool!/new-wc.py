import os 
import sys 
import regex as re


def count_bytes(file_path):         # -c (count bytes)
    return str(os.path.getsize(file_path))

def count_lines(file):              # -l (count lines)
    return len(file.splitlines())

def count_words(file):              # -w (count words)
    pattern = re.compile(r'\S+', re.UNICODE)
    words = re.findall(pattern, file)
    return len(words)

def count_chars(file):              # -m (count characters)
    return len(file)


def main():

    file = ""
    command = None

    # If there is no argument, instruct the user
    if len(sys.argv) < 2:
        print("Usage: new-wc [-c | -l | -w | -m] [filename]")
        return

    if len(sys.argv) > 2:
        # If there is a command
        file = sys.argv[2]
        command = sys.argv[1].strip("-")
    else:
        # If there is no command
        file = sys.argv[1]

        # Check if a file is provided and exists
    if file and os.path.isfile(file):
        full_path = os.path.join(os.getcwd(), file)
        with open(full_path, 'r', encoding='utf-8') as my_file:
            file_content = my_file.read()

    if not command:
    # TODO default (no arg) combine -c,-l,-w
    # > new-wc test.txt
    #    7145   58164  342190 test.txt
        print(f'{count_bytes(full_path)} {count_lines(file_content)} {count_words(file_content)} {file}')

    elif command == "c":
        # -c (count bytes)
        # > new-wc -c test.txt
        #    342190 test.txt
        print(f'{count_bytes(full_path)} {file}')

    elif command == "l":
        # -l (count lines)
        # > new-wc -l test.txt
        #    7145 test.txt
        print(f'{count_lines(file_content)} {file}')

    elif command == "w":
        # -w (count words)
        # > new-wc -w test.txt
        #    58164 test.txt
        print(f'{count_words(file_content)} {file}')

    elif command == "m":
        # -m (count characters)
        # > new-wc -m test.txt
        #    339292 test.txt
        # print(f'{count_chars(full_path)} {file}')
        print(f'{count_chars(file_content)} {file}')


if __name__ == '__main__':
    main()



