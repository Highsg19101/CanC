import socket
import message
 
from message import Message
from message_header import Header
from message_body  import BodyRequest, BodyResponse, BodyData, BodyResult
 
 
#socket.send/socket.recv 유틸리티 클래스
class MessageUtil:
    #보내기
    #정적메서드
    @staticmethod
    def send(socket, msg):
        sent = 0
        #bytes[] 구하기
        buffer = msg.GetBytes()
        
        #msg 크기만큼 send() 반복
        while sent<msg.GetSize():
            sent += socket.send(buffer)
 
 
    #받기
    @staticmethod
    def receive(socket):
        #헤더[MSGID+MSGTYPE+BODYLEN+FRAGMENTED+LASTMSG+SEQ]
        #헤더크기
        headerSize = 16
        #헤더버퍼
        headerBuffer = bytes()
 
        #헤더읽기
        while headerSize>0:
            buffer = socket.recv(headerSize) #헤더크기만큼 읽기
            if not buffer:
                return None
 
            #헤더(bytes)읽어서 담기
            headerBuffer += buffer;
            headerSize -= len(buffer) #헤더크기에서 빼서 헤더크기만큼 다읽었으면 반복문 나오기
 
 
        #헤더객체 생성
        header = Header(headerBuffer)
 
 
 
        #바디
        #바디크기
        bodySize = header.BODYLEN
        #바디버퍼
        bodyBuffer = bytes()
 
        #바디읽기
        while bodySize > 0:
            buffer = socket.recv(bodySize)  #바디크기만큼 읽기
            if not buffer:
                return None
 
            #바디(bytes)읽어서 담기
            bodyBuffer += buffer
            bodySize -= len(buffer) #바디크기에서 빼서 바디크기만큼 다읽었으면 반복문 나오기
 
 
        #바디객체 생성
        body = None
        if header.MSGTYPE == message.REQ_FILE_SEND:
            body = BodyRequest(bodyBuffer)
        elif header.MSGTYPE == message.REP_FILE_SEND:
            body = BodyResponse(bodyBuffer)
        elif header.MSGTYPE == message.FILE_SEND_DATA:
            body = BodyData(bodyBuffer)
        elif header.MSGTYPE == message.FILE_SEND_RES:
            body = BodyResult(bodyBuffer)
        else:
            #Exception 타입 에러 발생
            raise Exception("Unknown MSGTYPE : {0}".format(header.MSGTYPE))
 
 
 
        #메시지 = 헤더+바디 객체 생성
        msg = Message()
        msg.Header = header
        msg.Body = body
 
        return msg
