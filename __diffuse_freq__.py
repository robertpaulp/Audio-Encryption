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

    N = 10

    spectrum = scipy.fft.fft(audio_data)

    original_len = len(spectrum)
    # Split spectrum into N sub-bands
    remaining = len(spectrum) % N
    if remaining != 0:
        padding = N - remaining
        spectrum = numpy.pad(spectrum, (0, padding), 'constant')

    sub_band = numpy.split(spectrum, N)
    sub_band_idx = numpy.random.permutation(N)

    sub_band_shuffled = [sub_band[i] for i in sub_band_idx]

    spectrum_shuffled = numpy.concatenate(sub_band_shuffled)

    encrypted_spectrum = scipy.fft.ifft(spectrum_shuffled)

    enc_audio_data = numpy.real(encrypted_spectrum)

    # Remove padding
    enc_audio_data = enc_audio_data[:original_len]    

    enc_audio_data = enc_audio_data.astype(numpy.int16)

    wavfile.write(output_file, sample_rate, enc_audio_data)
    
    return sub_band_idx

def decrypt(input_file, output_file, key):

    # Get data
    sample_rate, audio_data = wavfile.read(input_file)

    N = 10

    spectrum = scipy.fft.fft(audio_data)

    # # Split spectrum into N sub-bands
    # remaining = len(spectrum) % N
    # if remaining != 0:
    #     padding = N - remaining
    #     spectrum = numpy.pad(spectrum, (0, padding), 'constant')

    sub_band = numpy.split(spectrum, N)
    
    #inverse_key = numpy.argsort(key)
    arranged_sub_band = [0] * N
    for i in range(N):
        arranged_sub_band[key[i]] = sub_band[i]

    spectrum_shuffled = numpy.concatenate(arranged_sub_band)

    encrypted_spectrum = scipy.fft.ifft(spectrum_shuffled)

    enc_audio_data = numpy.real(encrypted_spectrum)

    enc_audio_data = enc_audio_data.astype(numpy.int16)

    wavfile.write(output_file, sample_rate, enc_audio_data)
