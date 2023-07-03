import __diffuse_freq__ as diff
import __err_input__ as err
import sys

def main():
    arg_len = len(sys.argv)

    if err.err_usage(arg_len, [3, 5]):
        return

    if sys.argv[1] == "-c":
        if err.err_args(arg_len, 3):
            return
        diff.nyquist_sampling(sys.argv[2])

    elif sys.argv[1] == "-enc":
        if err.err_args(arg_len, 5):
            return
        diff.encrypt(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-d":
        if err.err_args(arg_len, 5):
            return
        diff.decrypt(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-encN":
        if err.err_args(arg_len, 5):
            return
        diff.encrypt_shuffle(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == "-dN":
        if err.err_args(arg_len, 5):
            return
        diff.decrypt_shuffle(sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()
