# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:16:04 2021

@author: singh
"""

import numpy as np
from numpy import random
from matplotlib import pyplot as plt
from scipy import fft
from scipy import signal
import diff_codec as dff


def bin_array(data, n, dummy_bits):
    """

    Converts a positive integer num into an m-bit vector and 
    adds dummy bits at the beginning of to cover any locking delay
    
    Parameters
    ----------
    data : digital data
    n : number of bits
    
    Returns
    -------
    binary sequence
    """
    temp =  np.array(list(np.binary_repr(data).zfill(n))).astype(np.bool)
    return np.append(dummy_bits, temp)


def bpsk_mod(x, f_c, ph_c, bit_len, nb, nd):
    """

    Performs binary phase shift keying modulation
    
    Parameters
    ----------
    x : binary sequence
    f_c : carrier frequency with offset
    ph_c : carrier phase
    bit_len: bit period
    nb : number of bits
    nd : number of dummy bits to cover any locking delay
    
    Returns
    -------
    res : modulated signal
    """
    # Modulation:
    m = np.zeros(nb+nd)
    res = np.empty(0)
    for i in range(nb+nd):
        # array containing symbols -1 & +1 for bits 0 & 1 respectively
        m[i] = 2*x[i] - 1
        for j in range(bit_len):
            # multiplication of symbols with carrier wave
            res = np.append(res, m[i] * np.cos(ph_c + 2*np.pi*f_c*(i*bit_len+j)))
            
    # plot modulated signal
    plt.figure(1)
    plt.title('BPSK Modulated signal')
    plt.plot(res)
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    
    # plot frequency response of the modulated signal
    plt.figure(2)
    plt.title('Modulated signal frequency response')
    plt.plot(np.linspace(0,1,len(res)), np.abs(fft.fft(res)))
    plt.axvline(x=0.5, color='k', linestyle='--')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency/sample rate')
    return res


def VCO(v, fi, clock, alpha):
    """

    Voltage Controlled Oscillator
    
    Parameters
    ----------
    v : input voltage
    fi : initial clock frequency
    clock : current state of voltage controlled digital clock
    alpha : gain/attenuation parameter
    
    Returns
    
    -------
    clock : updated state of voltage controlled digital clock
    """  
    c = np.cos(2*np.pi*fi * (1 + alpha*v))
    s = np.sin(2*np.pi*fi * (1 + alpha*v))
    clock = np.matmul(np.array([[c, -s], [s, c]]), clock)
    return clock


def bpsk_demod(x, clock, fi, bit_len, nb, nd, coeff, numtaps):
    """

    Performs demodulation and decodes the demodulated signal
    
    Parameters
    ----------
    x : modulated signal
    clock : current state of voltage controlled digital clock
    fi : initial clock frequency
    bit_len: bit period
    nb : number of bits    
    nd : number of dummy bits to cover any locking delay
    coeff : FIR filter coefficients
    numtaps : number of taps
    
    Returns
    
    -------
    res : decoded binary sequence
    """       
    # Demodulation:
    c_mixed = np.zeros(numtaps)
    s_mixed = np.zeros(numtaps)
    
    c_lpf_output = np.empty(0) 
    s_lpf_output = np.empty(0) 
    
    volt = 0.0
    vout = np.array(volt)
    rout = np.empty(0)
    cout = clock[0]
    sout = clock[1]
    dout = np.empty(0)
        
    for i in range(((nb+nd)*bit_len) + numtaps//2):
        # array for each branch to store LPF input samples
        c_mixed = np.append(c_mixed[1:], clock[0] * x[i % ((nb+nd)*bit_len)])
        s_mixed = np.append(s_mixed[1:], -clock[1] * x[i % ((nb+nd)*bit_len)])
            
        # low pass filtering (convolution)
        # array for each branch to store LPF output samples
        c_lpf_output = np.sum(coeff * c_mixed)
        s_lpf_output = np.sum(coeff * s_mixed)
        
        # update VCO voltage
        volt = c_lpf_output * s_lpf_output
        
        # update current state of the clock
        clock = VCO(volt, fi, clock, alpha)
        
        # array storing demodulated signal
        dout = np.append(dout, c_lpf_output)
        # array storing in-phase component of oscillator
        cout = np.append(cout, clock[0])
        # array storing quadrature component of oscillator
        sout = np.append(sout, clock[1])
        # array storing reference clock
        rout = np.append(rout, np.cos(np.pi*2*fi*i))
        # array storing VCO voltage
        vout = np.append(vout, volt) 
    
    # plot VCO voltage
    plt.figure(3)
    plt.title('VCO voltage')
    plt.plot(vout)
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    
    # plot referance and recovered clock
    plt.figure(4)
    plt.plot(rout, '-r', label='Reference Clock')
    plt.plot(cout, '-b', label='Recovered Clock')
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    plt.legend(loc = 'upper right')
    
    plt.figure(5)
    plt.plot(sout, '-r', label='Quadrature Component')
    plt.plot(cout, '-b', label='In-phase Component')
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    plt.legend(loc = 'upper right')
    
    # plot demodulated signal
    plt.figure(6)
    plt.title('Demodulated signal')
    plt.plot(dout)
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    
    # decode demodulated signal
    res = np.zeros(nb)   
    for i in range(nd, (nb+nd)):
        # define mid-point of the bit period (compensate for the FIR filter delay)
        mid = i*bit_len + bit_len//2 + numtaps//2
        # decode using a threshold value of 0
        res[i-nd] = np.heaviside(dout[mid], 0)
    return res.astype(bool)
        

if __name__ == '__main__':
    """
    
    Main function
    
    """
    # input 24-bit digital data
    id_num = 2544946
    # number of bits to be transmitted
    Nbits = 24
    # dummy bits to cover any locking delay
    Ndummy = 16
    dummy_bits = np.append(np.zeros(Ndummy-1), 1).astype(bool)
    
    
    # convert digital data into binary sequence
    tx_bin = bin_array(id_num, Nbits, dummy_bits)
    
    
    # Differential Encoding:
    tx_diff = dff.diff_encode(tx_bin, Nbits, Ndummy)
    Nbits = Nbits+1

    
    # initialise parameters
    # initial clock frequency
    fi = 0.125
    # bit period (should be atleast twice the carrier period)
    bit_len = 16
    # numpy array denoting current state of the clock
    clock = np.array([1.0, 0.0])
    # VCO gain/attenuation parameter 
    alpha = 0.25
    #  random carrier phase and frequency (up to 1% deviation)
    f_c = fi * (1. + 0.02*(random.rand() - 0.5))
    ph_c = 2*np.pi * random.rand()
    
    
    # perform BPSK modulation
    tx_mod = bpsk_mod(tx_diff, f_c, ph_c, bit_len, Nbits, Ndummy)
    
    
    # low-pass filter design
    # number of taps
    numtaps = 64
    # FIR filter coefficients (cutoff frequency = 0.1)
    coeff = np.flip(signal.firwin(numtaps, 0.1))
    
    
    # perform demodulation and decode the demodulated signal into binary sequence
    rx_diff = bpsk_demod(tx_mod, clock, fi, bit_len, Nbits, Ndummy, coeff, numtaps)


    # Differential Dencoding:
    rx_bin = dff.diff_decode(rx_diff, Nbits)


    #  compare output binary data with your input data
    print("Number of incorrect bits:" + str(np.sum(rx_bin != tx_bin[Ndummy:])))
    
    plt.show()