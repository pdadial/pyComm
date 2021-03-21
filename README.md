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
  * Simulation of transmission and reception over a noisy (AWGN) channel.
  * Perform parity test at the receiver. If the received data is different from parity setting at the transmitter do an automatic-repeat-request and retransmit the word.
  * Determine bit error rate and the ratio of the total number of ARQs to the number of pixels.
  * Plot an I-Q constellation diagram.
* Forward Error Correction: Block codes, Convolutional Codes
* Differential Coding
* Costas Loop

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
`git clone https://github.com/prateeksd/pyComm`

## Usage
* #### Modulation Schemes
       Run sim_mod.py specifing one modulation schemes: `BPSK`, `QPSK`, `4-QAM`, `16-QAM`, `256-QAM`
       <br />
      `python sim_mod.py --scheme QPSK`

## Acknowledgement
This project was part of the course Digital Communication, taught by [dchutchings](https://github.com/dchutchings) of University of Glasgow
