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

    parser.add_argument('-d', action='store')
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
    
    

    # rate 1/2 code with [0o7, 0o5] as the feedforward polynomial
    code,tblen = FEC.ConvCode.create_conv_codes()


            
    # flatten the image into a 1D array and
    # append tblen zeros to compensate for the decoder delay
    tx_bin = np.append(np.unpackbits(np.array(tx_im)), np.zeros(tblen))
    
    
    
    # simulate channel encoding
    encoder = komm.ConvolutionalStreamEncoder(code)
    code_word = encoder(tx_bin)  
    
    # simulate modulation
    tx_data = qpsk.modulate(code_word)
    
    # list containing decoding decision methods
    d = args.d   
    decoder = komm.ConvolutionalStreamDecoder(code, traceback_length=tblen, input_type=d)
    
    string = " ".join([d, "decoding"])
    print(" ".join(["Simulating", string, "..."]))
    

    
    # loop to to simulate transmission with the SNR value in range 0 to max_snr
    for dB in range(max_snr):
        # simulate noise in channel
        rx_data = awgn[dB](tx_data)
        
        # simulate demodulation
        rx_demod = qpsk.demodulate(rx_data, decision_method=d)
        
        # simulate channel decoding
        rx_bin = decoder(rx_demod)
        
        # total number of errors after discarding first tblen bits of rx_bin
        num_error = np.sum(rx_bin[tblen:] != tx_bin[:-tblen])
        
        # simulated BER for corresponding SNR[dB]
        ber[dB] = num_error / num_bits
        nonzero_index = np.nonzero(ber) # indices up to non-zero BER
        
        snr[dB] = dB
        
    # plot simulated BER against SNR for all the Convolutional codes
    plt.figure(2)
    plt.scatter(snr[nonzero_index], ber[nonzero_index])
    plt.plot(snr[nonzero_index], ber[nonzero_index], label = string)
        
    plt.yscale('log')
    plt.grid(True)
    plt.xlabel('SNR [dB]')
    plt.ylabel('BER')
    plt.legend(loc = 'upper right')
    plt.title('BER against SNR Comparison (with Convolutional Code)')
        
    plt.show()