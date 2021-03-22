## Table of contents
* [General info](#general-info)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Acknowledgement](#acknowledgement)

## General info
Digital communication simulation in Python.

### Features
* #### Modulation Schemes: BPSK, QPSK, 4-QAM, 16-QAM, 256-QAM
  * Transmission and reception over a noisy (AWGN) channel with signal-to-noise ratio from 0 to 9dB.
  * Parity test at the receiver: if the received data is different from parity setting at the transmitter do an automatic-repeat-request and retransmit the word.
  * Determine bit error rate.
  * Plot I-Q constellation diagram.
* #### Forward Error Correction: BCH code, Convolutional Code
  * Simulation over a noisy channel using QPSK.
  * Determine bit error rate.
  * Coding and decoding using (n,k) BCH codes.

    |m  |n  |k  |t  |
    |---|---|---|---|
    |3  |7  |4  |1  |
    |4  |15 |5  |3  |
    |5  |31 |6  |7  |
    |6  |63 |6  |11 |
  * Coding and decoding using convolutional code using soft(or)hard decoding.

![alt text](https://github.com/pdadial/pyComm/blob/main/images/conv%20encoder.png "rate 1/2 convolutional encoder")
* #### Differential Coding
* #### Costas Loop
  * BPSK modulation/demodulation.
  * Carrier Recovery using Costas Loop.
  * Implement differential coding to deal with any ambiguity in the recovered data.

![alt text](https://github.com/pdadial/pyComm/blob/main/images/costas_loop.png "classical costas loop")

## Prerequisites
Anaconda enviroment recommended
<br />
Individual modules:

NumPy      `pip install numpy`<br />
Scipy         `pip install scipy`<br />
Matplotlib `pip install matplotlib`<br />
komm       `pip install komm`

## Installation
Clone the repository
<br />
`git clone https://github.com/pdadial/pyComm.git`

## Usage
* #### Modulation Schemes
       Run sim_mod.py specifing one of the modulation schemes: `BPSK`, `QPSK`, `4-QAM`, `16-QAM`, `256-QAM`
       <br />
       `python sim_mod.py --scheme QPSK`

## Acknowledgement
This project was part of the course Digital Communication, taught by [dchutchings](https://github.com/dchutchings) of University of Glasgow
