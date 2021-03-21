
import komm

class BCH:
    def create_bch_codes(m, t):
        """

        Creates BCH binary codes which can correct up to t bit errors
        Parameters
        ----------
        m : positive integer (>=3)
        t : number of bit errors to be corrected
        
        Returns
        -------
        instance of the BCH code
        """
        code = komm.BCHCode(m,t)        
        return code
    
class ConvCode:
    def create_conv_codes(m, t):
        """

        Creates rate 1/2 convolutional code with [0o7, 0o5] as the feedforward polynomial
        Parameters
        ----------
        m : positive integer (>=3)
        t : number of bit errors to be corrected
        
        Returns
        -------
        instance of the BCH code
        """
        code = komm.ConvolutionalCode(feedforward_polynomials=[[0o7, 0o5]])
        # the traceback depth in the Viterbi algorithm
        # usually 6 times the constraint length (3 in this case)
        tblen = 18       
        return code