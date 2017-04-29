from message import ISerializable
import struct
 
 
class Header(ISerializable):
    def __init__(self, buffer):
        self.struct_fmt = "=3I2BH" #unsigned int[3], byte[2], unsigend short
        self.struct_len = struct.calcsize(self.struct_fmt) #format의 길이계산
 
        if buffer != None:
            #bytes->튜플 데이터로 변환
            unpacked = struct.unpack(self.struct_fmt, buffer)
 
            self.MSGID = unpacked[0]
            self.MSGTYPE = unpacked[1]
            self.BODYLEN = unpacked[2]
            self.FRAGMENTED = unpacked[3]
            self.LASTMSG = unpacked[4]
            self.SEQ = unpacked[5]
 
 
    def GetBytes(self):
        #튜플->bytes로 변환
        return struct.pack(self.struct_fmt, *(self.MSGID,
                                              self.MSGTYPE,
                                              self.BODYLEN,
                                              self.FRAGMENTED,
                                              self.LASTMSG,
                                              self.SEQ)
                           )
 
    def GetSize(self):
        return self.struct_len
