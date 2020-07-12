# NNIE Python Interface

Python remote interface for Huawei HiSilicon's NNIE NPUs.

## Introduction

This repo provides interface for using NNIE's wk models 
remotely with the `nnie_transfer_server` authored by me 
running on the Hi3516/Hi3519 platforms.

## Usage
* Build the [nnie_transfer_server](https://github.com/sunnyden/nnie_transfer_server) following
 the instructions and run it on the remote board.
* Install the NNIE python interface by executing `pip3 install nnie`
* Make sure your device can reach your HiSilicon board through network.
* Sample codes are provided below:
```python
import cv2
from nnie.nnie import NNIE
net = NNIE(file='path/to/your/model.wk',ipaddr='192.168.31.20',port=7777)
image = cv2.imread("path/to/your/image.jpg")
network_input_width = 320
network_input_height = 240
image = cv2.resize(image, (network_input_width, network_input_height))
result = net(data=image) # You may change 'data' into other names according 
result = net(image=image) # to the name of your model's input layer
```
