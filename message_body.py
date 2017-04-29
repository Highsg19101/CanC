from message import ISerializable
import message
import struct
 
#파일전송요청 - FILESIZE[8bytes] + FILENAME[(Bodylen-FileSize)bytes]
#unsigned long long + bytes[len(FILENAME)]
class BodyRequest(ISerializable):
    def __init__(self, buffer):
        if buffer != None:
            slen = len(buffer)
 
            #unsigned long long, bytes[slen-8]
            self.structFmt = str.format("=Q{0}s", slen-8)
            self.structLen = struct.calcsize(self.structFmt)
 
            if slen>8:
                slen = slen - 8 #unsigned long long(FILESIZE) 크기만큼 뺌
            else:
                slen = 0
 
 
            #bytes->튜플데이터로 변환
            unpacked = struct.unpack(self.structFmt, buffer)
 
            self.FILESIZE = unpacked[0]
            #문자열로 디코딩
            self.FILENAME = unpacked[1].decode(encoding="utf-8").replace("\x00","")
 
        else:
            self.structFmt = str.format("=Q{0}s", 0)
            self.structLen = struct.calcsize(self.structFmt)
            self.FILESIZE = 0
            self.FILENAME = ""
 
 
    def GetBytes(self):
        #FILENAME문자열을 bytes로 인코딩
        buffer = self.FILENAME.encode(encoding="utf-8")
 
        #unsigned long long, bytes[FILENAME bytes]
        self.structFmt = str.format("=Q{0}s", len(buffer))
 
        #튜플데이터->bytes로 변환
        return struct.pack(self.structFmt, *(self.FILESIZE,
                                             buffer))
 
 
 
    def GetSize(self):
        #FILENAME문자열을 bytes로 인코딩
        buffer = self.FILENAME.encode(encoding="utf-8")
 
        #unsigned long long, bytes[FILENAME bytes]
        self.structFmt = str.format("=Q{0}s", len(buffer))
        self.structLen = struct.calcsize(self.structFmt)
 
        return self.structLen;
        
 
 
#파일전송응답 - MSGID[4byte] + RESPONSE[1byte]
#unsigned int + Byte
class BodyResponse(ISerializable):
    def __init__(self, buffer):
        #unsigned int, Byte
        self.structFmt = "=IB"
        self.structLen = struct.calcsize(self.structFmt)
 
        if buffer != None:
            #bytes->튜플데이터로 변환
            unpacked = struct.unpack(self.structFmt, buffer)
 
            self.MSGID = unpacked[0]    #파일전송요청 식별
            self.RESPONSE = unpacked[1] #파일전송요청 수락
 
        else:
            self.MSGID = 0
            self.RESPONSE = message.DENIED  #파일전송요청 거절
            
 
    def GetBytes(self):
        return struct.pack(self.structFmt, *(self.MSGID,
                                             self.RESPONSE))
 
 
    def GetSize(self):
        return self.structLen
    
 
 
#파일전송데이터 - DATA[header.BODYLEN]
#bytes[header.BODYLEN]
class BodyData(ISerializable):
    def __init__(self, buffer):
        if buffer!=None:
            self.DATA = buffer
 
 
    def GetBytes(self):
        return self.DATA
 
 
    def GetSize(self):
        return len(self.DATA)
 
 
 
#파일수신결과 - MSGID[4byte] + RESULT[byte]
#unsigned int + Byte
class BodyResult(ISerializable):
    def __init__(self, buffer):
        #unsigned int , Byte
        self.structFmt = "=IB"
        self.structLen = struct.calcsize(self.structFmt)
 
        if buffer != None:
            #bytes->튜플데이터로 변환
            unpacked = struct.unpack(self.structFmt, buffer)
            self.MSGID = unpacked[0]
            self.RESULT = unpacked[1]
        else:
            self.MSGID = 0
            self.RESULT = message.FAIL
 
 
    def GetBytes(self):
        #튜플데이터->bytes로 변환
        return struct.pack(self.structFmt, *(self.MSGID,
                                             self.RESULT))
 
 
    def GetSize(self):
        return self.structLen
