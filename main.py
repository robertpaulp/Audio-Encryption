import __diffuse_freq__
import numpy

def main():

    filename = "CantinaBand60.wav"
    output_file = "CantinaBand60_encrypted.wav"

    data = __diffuse_freq__.load_data(filename)

    key, original_len = __diffuse_freq__.encrypt(data, output_file)
    
    __diffuse_freq__.decrypt(output_file, "CantinaBand60_decrypted.wav", key, original_len)

if __name__ == "__main__":
    main()