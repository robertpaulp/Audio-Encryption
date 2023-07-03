import numpy
import scipy.fft
import matplotlib.pyplot as plt
from scipy.io import wavfile



def load_data(filename):
    sample_rate, audio_data = wavfile.read(filename)
    duration = len(audio_data)/sample_rate

    data = [duration, sample_rate, audio_data]

    return data

def encrypt_shuffle(input_file, output_file, key_file):
    # Get data
    data = load_data(input_file)
    duration = data[0]
    sample_rate = data[1]
    audio_data = data[2]

    N = int(duration * sample_rate)

    # Split audio data into N sub-bands
    remaining = len(audio_data) % N
    if remaining != 0:
        print("Padding on encrypted spectrum")
        padding = N - remaining
        audio_data = numpy.pad(audio_data, (0, padding), 'constant')

    sub_band = numpy.array_split(audio_data, N)

    # Shuffle sub-bands
    sub_band_idx = numpy.arange(N)
    numpy.random.shuffle(sub_band_idx)

    sub_band_shuffled = [0] * N
    for i in range(N):
        sub_band_shuffled[sub_band_idx[i]] = sub_band[i]

    # Concatenate sub-bands
    enc_audio_data = numpy.concatenate(sub_band_shuffled)

    # Remove padding
    enc_audio_data = enc_audio_data[:len(audio_data)]

    enc_audio_data = enc_audio_data.astype(numpy.int16)

    # Write encrypted file
    wavfile.write(output_file, sample_rate, enc_audio_data)

    # Write key file
    key = sub_band_idx
    key.tofile(key_file)


def decrypt_shuffle(input_file, output_file, key_file):
    # Get data
    data = load_data(input_file)
    duration = data[0]
    sample_rate = data[1]
    audio_data = data[2]

    N = int(duration * sample_rate)

    # Load key
    key = numpy.fromfile(key_file, dtype=int)

    # Split audio data into N sub-bands
    remaining = len(audio_data) % N
    if remaining != 0:
        print("Padding on decrypted spectrum")
        padding = N - remaining
        audio_data = audio_data[:-padding]

    sub_band = numpy.array_split(audio_data, N)

    # Arrange sub-bands
    arranged_sub_band = [0] * N
    for i in range(N):
        arranged_sub_band[i] = sub_band[key[i]]

    # Concatenate sub-bands
    dec_audio_data = numpy.concatenate(arranged_sub_band)

    # Remove padding
    dec_audio_data = dec_audio_data[:len(audio_data)]

    dec_audio_data = dec_audio_data.astype(numpy.int16)

    wavfile.write(output_file, sample_rate, dec_audio_data)

def encrypt(input_file, output_file, key_file):

    # Get data
    data = load_data(input_file)
    duration = data[0]
    sample_rate = data[1]
    audio_data = data[2]
    audio_data = audio_data.astype(numpy.float64)

    # Number of sub-bands
    N = 4

    spectrum = numpy.fft.fft(audio_data)
    
    # Split spectrum into N sub-bands
    original_len = len(spectrum)
    remaining = len(spectrum) % N
    if remaining != 0:
        print("Padding on encrypted spectrum")
        padding = N - remaining
        spectrum = numpy.pad(spectrum, (0, padding), 'constant')

    sub_band = numpy.array_split(spectrum, N)

    # Shuffle sub-bands
    sub_band_idx = numpy.arange(N)
    numpy.random.shuffle(sub_band_idx)

    sub_band_shuffled = [0] * N
    for i in range(N):
        sub_band_shuffled[sub_band_idx[i]] = sub_band[i]

    spectrum_shuffled = numpy.concatenate(sub_band_shuffled)
    encrypted_spectrum = numpy.fft.ifft(spectrum_shuffled)
    enc_audio_data = numpy.real(encrypted_spectrum)

    # Remove padding
    enc_audio_data = enc_audio_data[:original_len]    

    enc_audio_data = enc_audio_data.astype(numpy.int16)

    wavfile.write(output_file, sample_rate, enc_audio_data)

    # Plot audio data
    # plt.plot(audio_data)
    # plt.plot(enc_audio_data)
    # plt.show()
    
    # Write key file
    key = sub_band_idx
    key.tofile(key_file)


def decrypt(input_file, output_file, key_file):
    # Get data
    data = load_data(input_file)
    duration = data[0]
    sample_rate = data[1]
    audio_data = data[2]
    audio_data = audio_data.astype(numpy.float64)

    # Number of sub-bands
    N = 4

    # Load key
    key = numpy.fromfile(key_file, dtype=int)

    spectrum = numpy.fft.fft(audio_data)

    # # Split spectrum into N sub-bands
    remaining = len(spectrum) % N
    if remaining != 0:
        print("Padding on decrypted spectrum")
        padding = N - remaining
        spectrum = spectrum[:-padding]

    sub_band = numpy.array_split(spectrum, N)
        
    arranged_sub_band = [0] * N
    for i in range(N):
        arranged_sub_band[i] = sub_band[key[i]]

    spectrum_arranged = numpy.concatenate(arranged_sub_band)
    decrypted_spectrum = numpy.fft.ifft(spectrum_arranged)
    dec_audio_data = numpy.real(decrypted_spectrum)

    # Remove padding
    dec_audio_data = dec_audio_data[:len(audio_data)]

    dec_audio_data = dec_audio_data.astype(numpy.int16)

    # Plot audio data
    # plt.plot(dec_audio_data)
    # plt.show()

    wavfile.write(output_file, sample_rate, dec_audio_data)

def nyquist_sampling(input_file):
    # Get data
    data = load_data(input_file)
    sample_rate = data[1]
    signal = data[2]

    nyquist_rate = sample_rate / 2

    signal = signal.astype(numpy.float64)
    signal = numpy.fft.fftfreq(len(signal), 1/sample_rate)
    max_freq = numpy.max(numpy.abs(signal))

    if max_freq > nyquist_rate:
        print("Signal is not sampled at nyquist rate")
        return False
    else:
        print("Signal is sampled at nyquist rate")
        return True