import sys


def longest_comment_block(filename):
    longest = 0
    length = 0

    for record in open(filename):
        line = record.strip()
        if line.startswith("#"):
            length += 1
        else:
            if length > longest:
                longest = length
                length = 0
    return longest


def main():
    for filename in sys.argv[1:]:
        print(filename, longest_comment_block(filename))


if __name__ == "__main__":
    main()
