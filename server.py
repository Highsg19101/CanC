import os
import sys
import socket
import socketserver
import struct
import message
 
from message import Message
from message_header import Header
from message_body import BodyData, BodyRequest, BodyResponse, BodyResult
from message_util import MessageUtil
 
 
 
uploadDir = ""
 
 
 
#서버핸들러
class FileReceiveHandler(socketserver.BaseRequestHandler):
 
    #클라이언트의 접속 요청 처리
    def handle(self):
        print("클라이언트 : {0} 접속".format(self.client_address[0]))
 
        #클라이언트와 연결된 소켓 객체 생성
        sock = self.request 
 
 
 
        #클라이언트로부터 Message(header+body)를 읽는다
        #요청메시지 읽기
        requestMsg = MessageUtil.receive(sock)
        if requestMsg.Header.MSGTYPE != message.REQ_FILE_SEND:  #message.REQ_FILE_SEND : message모듈의 REQ_FILE_SEND변수
            client.close()
            return
        
        #요청메시지 - 파일전송요청 객체 생성
        bodyRequest = BodyRequest(None)
 
 
 
        #응답메시지 생성
        responseMsg = Message()
        
        #응답메시지 바디 생성 - 파일전송응답 객체 생성
        responseMsg.Body = BodyResponse(None)
        responseMsg.Body.MSGID = requestMsg.Header.MSGID
        responseMsg.Body.RESPONSE = message.ACCEPTED
 
        #응답메시지 헤더 생성
        responseMsg.Header = Header(None)
        responseMsg.Header.MSGID = 1
        responseMsg.Header.MSGTYPE = message.REP_FILE_SEND
        responseMsg.Header.BODYLEN = responseMsg.Body.GetSize()
        responseMsg.Header.FRAGMENTED = message.NOT_FRAGMENTED
        responseMsg.Header.LASTMSG = message.LASTMSG
        responseMsg.Header.SEQ = 0
 
        #응답메시지 전송
        MessageUtil.send(sock, responseMsg)
 
 
 
        print("파일 전송을 시작합니다..")
 
        #요청메시지에서 파일크기와 파일명을 가져온다
        fileSize = requestMsg.Body.FILESIZE 
        fileName = requestMsg.Body.FILENAME
 
        #읽어들인 파일크기
        receiveFileSize = 0
 
        #파일쓰기
        with open(uploadDir+"\\"+fileName, "wb") as file:
            receiveMSGID = -1
            previousSEQ = 0
 
            while True:
                #파일전송메시지 읽기
                receiveMsg = MessageUtil.receive(sock)
                
                if receiveMsg == None:  #receiveMsg가 none이거나 파일전송데이터 타입이 아니면 종료
                    break
                if receiveMsg.Header.MSGTYPE != message.FILE_SEND_DATA:
                    break
                if receiveMSGID == -1:     #MSGID가 다르면 종료
                    receiveMSGID = receiveMsg.Header.MSGID
                elif receiveMSGID != receiveMsg.Header.MSGID:
                    break
                if previousSEQ != receiveMsg.Header.SEQ: #SEQ(메시지 파편 번호)순서가 틀려지면 종료
                    print("{0} , {1}".format(previousSEQ, receiveMsg.Header.SEQ))
                    break
 
 
                print("#", end="")
                previousSEQ += 1
 
                #파일쓰기
                file.write(receiveMsg.Body.GetBytes())
                receiveFileSize += receiveMsg.Body.GetSize()
 
 
                #마시막 메시지이면 종료
                if receiveMsg.Header.LASTMSG == message.LASTMSG:
                    break
            #//end - while
 
            #파일닫기
            file.close()
        #//end - with open
            
 
        print()
        print("수신된 파일 크기 : {0} bytes".format(receiveFileSize))
 
 
        #수신결과메시지 생성
        resultMsg = Message()
        
        #수신결과메시지 바디 생성 - 파일수신결과 객체 생성
        resultMsg.Body = BodyResult(None)
        resultMsg.Body.MSGID = requestMsg.Header.MSGID
        resultMsg.Body.RESULT = message.SUCCESS
 
        #수신결과메시지 헤더 생성
        resultMsg.Header = Header(None)
        resultMsg.Header.MSGID = 2
        resultMsg.Header.MSGTYPE = message.FILE_SEND_RES
        resultMsg.Header.BODYLEN = resultMsg.Body.GetSize()
        resultMsg.Header.FRAGMENTED = message.NOT_FRAGMENTED
        resultMsg.Header.LASTMSG = message.LASTMSG
        resultMsg.Header.SEQ = 0
 
 
        #수신받은 파일크기와 헤더의 파일크기정보가 같으면 성공 
        if fileSize == receiveFileSize:
            MessageUtil.send(sock, resultMsg)   #수신결과메시지 전송
        else:
            resultMsg.Body = BodyResult(None)
            resultMsg.Body.MSGID = reqMsg.Header.MSGID
            resultMsg.Body.RESULT = message.FAIL
            MessageUtil.send(client, rstMsg)    #수신결과메시지 전송
 
 
        print("파일 전송을 마쳤습니다.")
 
        #소켓닫기
        sock.close()
 
 
 
if __name__ == "__main__":
 
    uploadDir = "D:\\study\\python\\python_ex_1\\ch13"
    #디렉토리있는지 체크
    if os.path.isdir(uploadDir)==False:
        os.mkdir(uploadDir) #없으면 디렉토리를 만든다
 
 
    server = None
    try:
        server = socketserver.TCPServer(("127.0.0.1", 8080), FileReceiveHandler)
 
        print("파일 업로드 시작")
        #클라이언트의 접속요청을 수신대기
        server.serve_forever()
    except Exception as err:
        print(err)
 
    print("서버를 종료합니다")
