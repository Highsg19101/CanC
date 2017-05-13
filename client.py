import os
import sys
import socket
import struct
import message
 
from message import Message
from message_header import Header
from message_body import BodyData, BodyRequest, BodyResponse, BodyResult
from message_util import MessageUtil
 
resultM = ""
 
#파일하나 전송하고 종료
def sendImage():
 
    filepath = "/home/pi/ABO2/image.jpg"
 
    #서버와 연결된 소켓 객체 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #서버 연결 요청
        sock.connect(("192.168.0.57", 8080))
 
 
 
        #요청메시지 생성
        requestMsg = Message()
        filesize = os.path.getsize(filepath)
 
        #요청메시지 바디 생성 - 파일전송요청 객체 생성
        requestMsg.Body = BodyRequest(None)
        requestMsg.Body.FILESIZE = filesize
        requestMsg.Body.FILENAME = filepath[filepath.rindex("/")+1:]
 
        #요청메시지 헤더 생성
        requestMsg.Header = Header(None)
        requestMsg.Header.MSGID = 1
        requestMsg.Header.MSGTYPE = message.REQ_FILE_SEND
        requestMsg.Header.BODYLEN = requestMsg.Body.GetSize()
        requestMsg.Header.FRAGMENTED = message.NOT_FRAGMENTED
        requestMsg.Header.LASTMSG = message.LASTMSG
        requestMsg.Header.SEQ = 0
 
        #요청메시지 전송
        MessageUtil.send(sock, requestMsg)
 
 
 
        #응답메시지 읽기
        responseMsg = MessageUtil.receive(sock)
        if responseMsg.Header.MSGTYPE != message.REP_FILE_SEND: #파일응답코드가 아니면 종료
            exit(0)
        if responseMsg.Body.RESPONSE ==message.DENIED:  #서버가 거부하면 종료
            exit(0)
 
 
 
        #파일 읽기
        with open(filepath, "rb") as file:
            totalsize = 0
            msgSEQ = 0
 
            fragmented = 0
            if filesize < 4096: #메시지분할여부 - 4096바이트 이상이면 분할
                fragmented = message.NOT_FRAGMENTED
            else:
                fragmented = message.FRAGMENTED
 
 
            while totalsize<filesize:
                readBytes = file.read(4096)
                totalsize += len(readBytes)
 
 
                #파일전송메시지 생성
                fileMsg = Message()
 
                #파일전송메시지 바디 생성 - 파일전송데이터 객체 생성
                fileMsg.Body = BodyData(readBytes)
 
                #파일전송메시지 헤더 생성
                fileMsg.Header = Header(None)
                fileMsg.Header.MSGID = 2
                fileMsg.Header.MSGTYPE = message.FILE_SEND_DATA
                fileMsg.Header.BODYLEN = fileMsg.Body.GetSize()
                fileMsg.Header.FRAGMENTED = fragmented
                fileMsg.Header.SEQ = msgSEQ
                if totalsize < filesize:
                    fileMsg.Header.LASTMSG = message.NOT_LASTMSG
                else:
                    fileMsg.Header.LASTMSG = message.LASTMSG
 
                
                msgSEQ += 1 #메시지 번호 1증가
                
                print("#", end="")
 
 
                #파일전송메시지 전송
                MessageUtil.send(sock, fileMsg)
            #//end while
                
 
            #파일닫기
            file.close()
        #//end with open
 
 
        print()
        
        golobal resultM
        resultM = str(sock.recv(1024), "utf-8")
        
        #결과메시지 읽기
        resultMsg = MessageUtil.receive(sock)
 
        result = resultMsg.Body
        print("파일 전송 성공 : {0}".format(result.RESULT==message.SUCCESS))
    except Exception as err:
        print("예외발생 : "+err, end="")
 
 
    #소켓닫기
    sock.close()
    
    print("클라이언트를 종료합니다.")
    return resultM
