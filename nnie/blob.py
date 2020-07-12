import cv2
import numpy as np
import struct
class NNIEBlob:
    def __init__(self,id,segmentId,layerId,width,height,channel,isInput,name):
        self.id = id
        self.segmentId = segmentId
        self.layerId =layerId
        self.width = width
        self.height = height
        self.channel = channel
        self.isInput = isInput
        self.name = name
        self.data = None

    def checkDimension(self, image):
        return image.shape[0] == self.height and image.shape[1] == self.width and image.shape[2] == self.channel

    def getBlobData(self, image):
        ret_data = bytearray()
        chn_data = bytearray()
        ret_data.extend(struct.pack("I",self.id))
        channel_blobs = cv2.split(image)
        for channel in channel_blobs:
            listdata = channel.reshape(channel.shape[0] * channel.shape[1]).tolist()
            data = struct.pack("%sB" % (channel.shape[0] * channel.shape[1]),*listdata)
            chn_data.extend(data)
        ret_data.extend(struct.pack("I", len(chn_data)))
        ret_data.extend(chn_data)
        return ret_data

    def storeBlobData(self, blob):
        if len(blob) == self.channel * self.width * self.height*4:
            self.data = struct.unpack("%sf" % (self.height * self.width *self.channel),blob)
            self.data = np.reshape(self.data,(self.channel,self.height,self.width))
            return self.data
        return None


