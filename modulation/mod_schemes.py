import komm
import numpy as np

class ModScheme:
    def create_object(self,x):
        """

        Creates an instance of the corresponding modulation scheme
        Parameters
        ----------
        x : string containing the name of the modulation scheme
        
        Returns
        -------
        instance of the corresponding modulation scheme 
        k : bits per symbol
        """
        if x == 'BPSK':
            k = 1
            obj = komm.PSKModulation(2)
            
        if x == 'QPSK':
            k = 2
            obj = komm.PSKModulation(4, phase_offset=np.pi/4)
            
        if x == '4-QAM':
            k = 2
            obj = komm.QAModulation(4, base_amplitudes=1/np.sqrt(2.))
            
        if x == '16-QAM':
            k = 4
            obj = komm.QAModulation(16, base_amplitudes=1/np.sqrt(10.))
            
        if x == '256-QAM':
            k = 8
            obj = komm.QAModulation(256, base_amplitudes=1/np.sqrt(170.))
        return obj, k
