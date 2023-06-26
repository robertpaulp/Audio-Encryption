import __diffuse_freq__


def main():

    filename = "CantinaBand60.wav"

    data = __diffuse_freq__.load_data(filename)

    __diffuse_freq__.encrypt(data[0], data[1], "output.wav")


if __name__ == "__main__":
    main()