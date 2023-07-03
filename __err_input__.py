import sys

def err_args(len_args, required_len):
    if len_args != required_len:
        print("Not enough arguments")
        return True
    return False

def err_usage(len_args, required_len):

    match = all(len_args != required_len[i] for i in range(len(required_len)))

    if match:
        print("Usage: python main.py -c <input_file>")
        print("Usage: python main.py -enc|-d <input_file> <output_file> <key_file>")
        print("Usage: python main.py -encN|-dN <input_file> <output_file> <key_file>")
        return True
    return False
    