import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import komm
import FEC

if __name__ ==  '__main__':
    """
    
    Main function
    
    """
    # arguments
    import argparse
    # Create argument parser object
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', type=int, action='store')
    parser.add_argument('-t', type=int, action='store')
    # Create a namespace
    args = parser.parse_args()
    
    
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    image_path = os.path.join(script_dir, 'data/DC4_150x100.pgm')
    # input image
    tx_im = Image.open(image_path)
    # number of pixels
    Npixels = tx_im.size[1] * tx_im.size[0]
    
    # # plot input image
    # plt.figure(1)
    # plt.title('Input Image')
    # plt.imshow(np.array(tx_im),cmap="gray",vmin=0,vmax=255)
    
    # flatten the image into a 1D array
    tx_bin = np.unpackbits(np.array(tx_im))
    
    
    
    # positive integers(>=3)
    m = args.m
    # the number of bit errors to be corrected
    t = args.t
    
    
    # create an instance of the qpsk modulation scheme
    qpsk = komm.PSKModulation(4, phase_offset=np.pi/4)
    
    # maximim SNR[dB] value
    max_snr = 10
    num_bits = 8*Npixels
    
    # list of additive white gaussian noise sources with SNR in range 0 to max_snr
    awgn = [komm.AWGNChannel(snr=10**(x/10.)) for x in range(max_snr)]
        
    # array to store simulated bit error ratio
    ber = np.zeros(max_snr)
    # array to store signal-to-noise[dB] ratio for the channel
    snr = np.zeros(max_snr)



    # simulate the BCH channel codes
    # create BCH code
    code = FEC.BCH.create_bch_codes(m, t)
    
    # BCH code length and dimension
    n = code.length
    k = code.dimension        
   
    
   
    string = "".join(["(", str(n), ",", str(k), ") BCH Code"])
    print(" ".join(["Simulating", string, "..."]))              
      
    
    
    # simulate the channel encoding of k bits at a time
    tx_bin = tx_bin.reshape(-1,k)
    coded_word = [code.encode(tx) for tx in tx_bin]
    coded_word = np.array(coded_word).ravel()
    
    # simulate modulation
    tx_data = qpsk.modulate(coded_word)
    
    # loop to to simulate transmission with the SNR value in range 0 to max_snr
    for dB in range(max_snr):
        # simulate noise in channel            
        rx_data = awgn[dB](tx_data)
        
        # simulate demodulation
        rx_demod = qpsk.demodulate(rx_data).reshape(-1,n)
        
        # simulate channel decoding of n bits at a time
        rx_bin = [code.decode(rx) for rx in rx_demod]
        rx_bin = np.array(rx_bin)
    
        # total number of errors
        num_error = np.sum(rx_bin != tx_bin)
        
        # simulated BER for corresponding SNR[dB]
        ber[dB] = num_error / num_bits
        nonzero_index = np.nonzero(ber) # indices up to non-zero BER
        
        snr[dB] = dB
        
    # plot simulated BER against SNR for all the BCH codes
    plt.figure(2)
    plt.scatter(snr[nonzero_index], ber[nonzero_index])
    plt.plot(snr[nonzero_index], ber[nonzero_index], label = string)

    plt.yscale('log')
    plt.grid(True)
    plt.xlabel('SNR [dB]')
    plt.ylabel('BER')
    plt.legend(loc = 'upper right')
    plt.title('BER against SNR Comparison (with BCH Code)')
        
    plt.show()