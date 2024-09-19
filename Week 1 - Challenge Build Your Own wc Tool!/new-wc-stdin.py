import os 
import sys 
import regex as re


def count_bytes(file):         # -c (count bytes)    This gets the right amount, not by len 
    return str(len(file))

def count_bytes_stdin(file):         # -c (count bytes)
    return len(file)

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

    if len(sys.argv) < 2:
        print("Usage: new-wc [-c | -l | -w | -m] [filename]")
        return

    try:
        if len(sys.argv) > 2:
            # If there is a command
            file = sys.argv[2]
            command = sys.argv[1].strip("-")
        else:
            # If there is no command
            file = sys.argv[1]

        # Check to see if using std-in
        if file and os.path.isfile(file):
            full_path = os.path.join(os.getcwd(), file)
            with open(full_path, 'r', encoding='utf-8') as my_file:
                file_content = my_file.read()
        else: 
            command = sys.argv[1].strip("-")
            file_content = sys.stdin.read()  # Read from standard input
    except:
        print("No Bueno")

    if not command:
    # default (no arg) combine -c,-l,-w
        print(f'{count_bytes(file_content)} {count_lines(file_content)} {count_words(file_content)} {file}')

    elif command == "c":
        print(f'{count_bytes(file_content)} {file}')

    elif command == "l":
        print(f'{count_lines(file_content)} {file}')

    elif command == "w":
        print(f'{count_words(file_content)} {file}')

    elif command == "m":
        print(f'{count_chars(file_content)} {file}')


if __name__ == '__main__':
    main()



