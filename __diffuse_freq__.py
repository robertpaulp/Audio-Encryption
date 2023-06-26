import numpy
import scipy
import scipy.fft
import matplotlib.pyplot as plt
import sympy
from scipy.io import wavfile

# define
N = 10


def load_data(filename):
    sample_rate, audio_data = wavfile.read(filename)

    return sample_rate, audio_data


def encrypt(sample_rate, audio_data, output_file):


    spectrum = numpy.fft.fft(audio_data)
    sub_bands = numpy.split(spectrum, N)

    shuffle_bands = numpy.random.shuffle(sub_bands)

    x_FT = numpy.concatenate(shuffle_bands)

    wavfile.write(output_file, sample_rate, x_FT)

