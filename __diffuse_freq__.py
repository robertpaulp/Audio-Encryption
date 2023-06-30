import numpy
import scipy
import scipy.fft
import matplotlib.pyplot as plt
import sympy
from scipy.io import wavfile



def load_data(filename):
    sample_rate, audio_data = wavfile.read(filename)
    duration = len(audio_data)/sample_rate

    data = [duration, sample_rate, audio_data]

    return data

def encrypt(data, output_file):

    # Get data
    duration = data[0]
    sample_rate = data[1]
    audio_data = data[2]

    N = 100

    plt.plot(audio_data)

    spectrum = scipy.fft.fft(audio_data)

    original_len = len(spectrum)
    # Split spectrum into N sub-bands
    # remaining = len(spectrum) % N
    # if remaining != 0:
    #     padding = N - remaining
    #     spectrum = numpy.pad(spectrum, (0, padding), 'constant')

    sub_band = numpy.split(spectrum, N)
    sub_band_idx = numpy.arange(N)
    numpy.random.shuffle(sub_band_idx)

    sub_band_shuffled = [0] * N
    for i in range(N):
        sub_band_shuffled[sub_band_idx[i]] = sub_band[i]

    spectrum_shuffled = numpy.concatenate(sub_band_shuffled)
    encrypted_spectrum = scipy.fft.ifft(spectrum_shuffled)
    enc_audio_data = numpy.real(encrypted_spectrum)

    # Remove padding
    # enc_audio_data = enc_audio_data[:original_len]    

    enc_audio_data = enc_audio_data.astype(numpy.int16)

    wavfile.write(output_file, sample_rate, enc_audio_data)
    
    return sub_band_idx, original_len

def decrypt(input_file, output_file, key, original_len):
    # Get data
    sample_rate, audio_data = wavfile.read(input_file)

    N = 100

    spectrum = scipy.fft.fft(audio_data)

    # # Split spectrum into N sub-bands
    # remaining = len(spectrum) % N
    # if remaining != 0:
    #     padding = N - remaining
    #     spectrum = numpy.pad(spectrum, (0, padding), 'constant')

    sub_band = numpy.split(spectrum, N)
    
    
    arranged_sub_band = [0] * N
    for i in range(N):
        arranged_sub_band[i] = sub_band[key[i]]

    spectrum_shuffled = numpy.concatenate(arranged_sub_band)
    encrypted_spectrum = scipy.fft.ifft(spectrum_shuffled)
    enc_audio_data = numpy.real(encrypted_spectrum)

    # Remove padding
    # enc_audio_data = enc_audio_data[:original_len]

    enc_audio_data = enc_audio_data.astype(numpy.int16)

    plt.plot(enc_audio_data)
    plt.show()

    wavfile.write(output_file, sample_rate, enc_audio_data)
