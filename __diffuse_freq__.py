import numpy
import scipy
import scipy.fft
import matplotlib.pyplot as plt
import sympy
from scipy.io import wavfile

# define
N = 4


def load_data(filename):
    sample_rate, audio_data = wavfile.read(filename)

    return sample_rate, audio_data


def encrypt(sample_rate, audio_data, output_file):
    
    spectrum = scipy.fft.fft(audio_data)
    spectrum = numpy.array(spectrum, dtype=numpy.complex64)
    spectrum = numpy.real(spectrum)

    plt.plot(spectrum)
    plt.plot(audio_data)
    plt.show()

    # write to file
    wavfile.write(output_file, sample_rate, spectrum)


def decrypt(input_file, output_file):
    # read from file
    sample_rate, audio_data = load_data(input_file)

    # decrypt
    spectrum = numpy.array(audio_data, dtype=numpy.complex64)
    spectrum = scipy.fft.ifft(spectrum)
    spectrum = numpy.real(spectrum)
    spectrum = numpy.array(spectrum, dtype=numpy.int16)

    # write to file
    wavfile.write(output_file, sample_rate, spectrum)