import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from scipy import special
from mod_schemes import ModScheme
import komm

if __name__ ==  '__main__':
    """
    
    Main function
    
    """
    
    # arguments
    import argparse
    # Create argument parser object
    parser = argparse.ArgumentParser()

    parser.add_argument('--scheme', '-s', action='store')
    # Create a namespace
    args = parser.parse_args()
    
    
    
    # input image
    tx_im = Image.open("DC4_150x100.pgm")
    # number of pixels
    Npixels = tx_im.size[1] * tx_im.size[0]
    
    # # plot input image
    # plt.figure(1)
    # plt.imshow(np.array(tx_im),cmap="gray",vmin=0,vmax=255)
    
    # flatten the image into a 1D array
    tx_bin = np.unpackbits(np.array(tx_im))
    
        
    
    mod = ModScheme()
    
    # modulation scheme object and corresponding bits per symbol
    obj,k = mod.create_object(args.scheme)

    # maximim SNR[dB] value
    max_snr = 10
    n = 0
    num_bits = 8*Npixels
    
    # array to store simulated bit error ratio
    ber = np.empty(max_snr)
    # array to store theoretical bit error ratio
    ber_th = np.empty(max_snr)
    # array to store signal-to-noise[dB] ratio for the channel
    snr = np.empty(max_snr)
    # array to store automatic-repeat-request ratio
    arq_ratio = np.empty(max_snr)
    
    
    
    string = ' '.join(["Performing", args.scheme, "for signal-to-noise ratio in range 0 to", str(max_snr-1), "dB..."])
    print(string)
    
    
    
    # loop to to simulate the transmission with SNR[dB] up to the maximum value
    while n<max_snr:
        # additive white gaussian noise source with SNR=n[dB]
        awgn = komm.AWGNChannel(snr=10**(n/10.))
        # reset the counter which adds the total number of ARQs
        arq = 0
        # array to store received binary sequence
        rx_bin = np.empty(num_bits, dtype=int)
        # list to store received complex-valued data 
        rx_data = []
        
        
        
        # loop to simulate the transmission of an 8-bit word at a time
        for j in range(0, num_bits, 8):
            # replace the LSB of each 8-bit word with even parity bit
            temp = tx_bin[j:j+8]
            temp[-1] = np.sum(temp[:-1])%2
            tx_bin[j:j+8] = temp
            
            # simulate modulation
            tx_data = obj.modulate(tx_bin[j:j+8])
            
            
            
            # set the retransmission flag
            resend = True
            
            # loop to simulate automatic-repeat-request
            while resend:
                # simulate noise in channel (returns complex-valued data)
                rx_data_byte = awgn(tx_data)
                # simulate demodulation
                rx_demod_byte = obj.demodulate(rx_data_byte)
                
                # parity test at the receiver
                if np.sum(rx_demod_byte)%2 != 0:
                    # if incorrect then increment counter and retransmit
                    arq += 1
                else:
                    # else reset the retransmission flag
                    resend = False
            
            
            
            # append the received complex-valued data
            rx_data.append(list(rx_data_byte))
            # store the received byte
            rx_bin[j:j+8] = rx_demod_byte
        
        
        
        # total number of errors
        num_error = np.sum(rx_bin != tx_bin)
        
        # simulated BER for corresponding SNR[dB]
        ber[n] = num_error / num_bits
        nonzero_index = np.nonzero(ber) # indices up to non-zero BER
        # theoretical BER for corresponding SNR[dB]
        ber_th[n] = 0.5 * special.erfc(np.sqrt((10**(n/10.))/k)) 
        # ASQR ratio for corresponding SNR[dB]
        arq_ratio[n] = arq / Npixels
        snr[n] = n
        n += 1

    
    
    # plot simulated BER against SNR for individual modulation schemes 
    # plot theoretical BER against SNR for individual modulation schemes 
    plt.figure(figsize=(8,20))
    plt.suptitle(args.scheme)
    plt.subplot(211)
    plt.scatter(snr[nonzero_index], ber[nonzero_index])
    plt.plot(snr[nonzero_index], ber[nonzero_index], label = 'Simulated Dependence')
    plt.plot(snr[nonzero_index], ber_th[nonzero_index], label = 'Theoretical Dependence')
    plt.xlabel('SNR [dB]')
    plt.ylabel('BER')
    plt.yscale('log')
    plt.legend(loc = 'upper right')
    plt.grid(True)
    
    # plot ARQ ratio against SNR for individual modulation schemes 
    plt.subplot(212)
    plt.scatter(snr, arq_ratio) #plot points
    plt.plot(snr, arq_ratio) #plot lines
    plt.xlabel('SNR [dB]')
    plt.ylabel('ARQ Ratio')
    plt.yscale('log')
    plt.grid(True)
    
    
    
    # # plot received image for individual modulation schemes
    # rx_im = np.packbits(rx_bin).reshape(tx_im.size[1], tx_im.size[0])
    # plt.figure()
    # plt.imshow(np.array(rx_im), cmap="gray", vmin=0, vmax=255)
    # plt.title(i[0] + ' Received Image')
    
    
    
    # plot I-Q constellation for individual modulation schemes
    plt.figure()
    plt.axes().set_aspect("equal")
    plt.scatter(np.asarray(rx_data)[:10000].real, np.asarray(rx_data)[:10000].imag, s=1, marker=".")
    plt.title(args.scheme + ' I-Q Constellation Diagram')
                    
    plt.show()