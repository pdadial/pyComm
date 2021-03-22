import numpy as np


def diff_encode(tx_bin, Nbits, Ndummy):
    """

    Differential encoder
    
    Parameters
    ----------
    tx_bin : input binary array
    Nbits : number of bits to be transmitted
    Ndummy : number of dummy bits to cover any locking delay
    
    Returns
    
    -------
    tx_diff : encoded binary array for transmission
    """
    # Differential Encoding:
    tx_diff = np.zeros(1, dtype=bool)
    for i in range(Nbits + Ndummy):
        tx_diff = np.append(tx_diff, tx_diff[i]^tx_bin[i])
    return tx_diff


def diff_decode(rx_diff, Nbits):
    """

    Differential decoder
    
    Parameters
    ----------
    rx_diff : received encoded binary array
    Nbits : number of bits to be transmitted
    
    Returns
    
    -------
    rx_bin : decoded binary array
    """
    rx_bin = np.empty(0, dtype=bool)
    Nbits = Nbits-1
    for i in range(Nbits):
        rx_bin = np.append(rx_bin, rx_diff[i]^rx_diff[i+1]).astype(bool)
    return rx_bin