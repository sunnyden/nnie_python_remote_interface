import socket
import struct
from nnie.blob import NNIEBlob


class NNIE:
    def __init__(self,file,ipaddr,port):
        self.address = ipaddr
        self.port = port
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,True)
        #self.client.ioctl(socket.SIO_KEEPALIVE_VALS,(1,60*1000,30*1000))
        self.client.connect((self.address, self.port))
        #self.client.setblocking(False)
        self.headers = b'\x30\x00\xFA\xCA'
        operation_code = struct.pack('I', 0)
        with open(file, 'rb') as file:
            file.seek(0, 2)
            size = file.tell()
            file.seek(0, 0)
            filedata = file.read(size)
            print(12 + size)
            lendata = struct.pack('I', 12 + size)
            self.client.sendall(self.headers)
            self.client.sendall(lendata)
            self.client.sendall(operation_code)
            self.client.sendall(filedata)
            self.blobs = {}
            self.input_blobs = {}
            self.output_blobs = {}
            result,return_error = self.recvall()
            length = len(result)
            #print("err")
            if not return_error:
                struct_size = struct.unpack('I',result[8:12])[0]
                blob_count = int((length-12)/struct_size)
                print("blob count",blob_count)
                for i in range(blob_count):
                    base = i * struct_size + 12
                    #print("%d %d %d %d %d %d %d %s"%())
                    str_end_idx = 0

                    for j in range(base + 7 * 4,base + struct_size):
                        if result[j] == 0:
                            str_end_idx = j
                            break
                    integer_data = struct.unpack("7I", result[base:base + 7 * 4])
                    blob_name = result[base + 7 * 4:str_end_idx].decode()
                    self.blobs[blob_name] = NNIEBlob(integer_data[0],integer_data[1],integer_data[2],integer_data[3],
                                                     integer_data[4],integer_data[5],integer_data[6],blob_name)
                    if integer_data[6] == 1:
                        self.input_blobs[integer_data[0]] = NNIEBlob(integer_data[0], integer_data[1], integer_data[2],
                                                                     integer_data[3],integer_data[4], integer_data[5],
                                                                     integer_data[6], blob_name)
                    else:
                        self.output_blobs[integer_data[0]] = NNIEBlob(integer_data[0], integer_data[1], integer_data[2],
                                                                      integer_data[3], integer_data[4], integer_data[5],
                                                                      integer_data[6], blob_name)
                    print(struct.unpack("7I", result[base:base + 7 * 4]),result[base + 7 * 4:str_end_idx].decode())
            else:
                print("Error when loading models")

    def __call__(self, *args, **kwargs):
        package = bytearray()
        package.extend(self.headers)
        operation_code = struct.pack('I', 1)
        #print(len(kwargs))
        blob_data = bytearray()
        forward_id = -1
        for key,value in kwargs.items():
            forward_id = self.blobs[key].id
            blob_data.extend(self.blobs[key].getBlobData(value))
        package.extend(struct.pack('I',18+len(blob_data)))
        package.extend(operation_code)
        package.extend(struct.pack('I',len(kwargs)))
        package.extend(blob_data)
        package.extend(struct.pack('I',forward_id))
        self.client.sendall(package)
        result, return_error = self.recvall()
        result_blobs = []
        if not return_error:
            blob_count = struct.unpack('I', result[8:12])[0]
            offset = 12
            for i in range(blob_count):
                blob_id = struct.unpack('I', result[offset:offset+4])[0]
                offset+=4
                blob_len = struct.unpack('I', result[offset:offset + 4])[0]
                offset += 4
                result_blobs.append(self.output_blobs[blob_id].storeBlobData(result[offset:offset + blob_len]))
                offset += blob_len
            return tuple(result_blobs)


        else:
            print("Recv Error when forwarding")

    def recvall(self):
        self.client.setblocking(False)
        result = bytearray()
        return_error = False
        length = 0
        while True:
            try:
                buf = self.client.recv(2048)
                result.extend(buf)
                if len(result) > 8:
                    if result[0] != 0x30 or result[1] != 0x00 or result[2] != 0xFA or result[3] != 0xCA:
                        return_error = True
                        break
                    length = struct.unpack('I', result[4:8])[0]
                    if length == len(result):
                        break
            except:
                ignore = 1
            #print(length, len(result))
        self.client.setblocking(True)
        return result,return_error
