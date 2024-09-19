import os 
import sys 
import regex as re

file = ""
command = None

if len(sys.argv) > 2:
    file = sys.argv[2]
    command = sys.argv[1].strip("-")
else:
    file = sys.argv[1]

full_path = os.path.join(os.getcwd(), file)


def count_bytes():
    return str(os.path.getsize(full_path))

def count_words():
    words = 0
    with open(full_path, 'r', encoding='utf-8') as my_file:
        # words = re.findall(r'\b\w+\b', my_file.read())
        # TODO: Regex still not getting all the correct cases
        # pattern = re.compile(r'\b_[a-zA-Z]+_\b|\b\d+[a-z]+\b|\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=]*)?\b|\b[a-zA-Z]+’[a-z]\b|[a-zA-Z]\.[a-zA-Z]\.|\d\.[A-Z]\.\d\b|\$\d+\,\d+|\b\d+\b|\b[a-zA-Z\'\-]+\b|\b\d+[-\d]*\b|\b\w\b', re.UNICODE)
        pattern = r'\S+'
        words = re.findall(pattern, my_file.read())
        
        # print(words)

        # # or
        # with open(full_path, 'r', encoding='utf-8') as my_file:
        #     text = my_file.read()
        #     pattern = re.compile(r'\p{L}+', re.UNICODE) 
        #     matches = pattern.findall(text)

        # print(f'{len(matches)} {file}')
    return len(words)

def count_lines():
    lines = 0
    with open(full_path, 'r', encoding='utf-8') as my_file:
        for line in my_file:
            lines += 1  
    return lines

def count_chars():
    with open(full_path, 'r', encoding='utf-8') as my_file:
        chars = 0
        for line in my_file:
            print(len(line))
            print(line)
            chars += len(line)
        return chars


def main():
    if not command:
    # TODO default (no arg) combine -c,-l,-w
    # > new-wc test.txt
    #    7145   58164  342190 test.txt
        print(f'{count_bytes()} {count_lines()} {count_words()} {file}')

    elif command == "c":
        # TODO -c (count bytes)
        # > new-wc -c test.txt
        #    342190 test.txt
        print(f'{count_bytes()} {file}')

    elif command == "l":
        # TODO -l (count lines)
        # > new-wc -l test.txt
        #    7145 test.txt
        print(f'{count_lines()} {file}')

    elif command == "w":
        # TODO -w (count words)
        # > new-wc -w test.txt
        #    58164 test.txt
        print(f'{count_words()} {file}')

    elif command == "m":
        # TODO -m (count characters)
        # > new-wc -m test.txt
        #    339292 test.txt
        print(f'{count_chars()} {file}')


# if no file:



if __name__ == '__main__':
    main()



