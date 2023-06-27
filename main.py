import __diffuse_freq__


def main():

    filename = "CantinaBand60.wav"
    output_file = "CantinaBand60_encrypted.wav"

    sample_rate, audio_data = __diffuse_freq__.load_data(filename)

    __diffuse_freq__.encrypt(sample_rate, audio_data, output_file)

    __diffuse_freq__.decrypt(output_file, "CantinaBand60_decrypted.wav")

if __name__ == "__main__":
    main()