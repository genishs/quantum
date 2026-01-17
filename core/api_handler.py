import requests
import os
import json
from dotenv import load_dotenv
import websocket
import threading
import time

load_dotenv() # .env 파일 로드

class KiwoomREST:
    def __init__(self):
        self.base_url = os.getenv("KIWOOM_API_BASE_URL")
        self.app_key = os.getenv("KIWOOM_APPKEY")
        self.app_secret = os.getenv("KIWOOM_SECRETKEY")
        self.access_token = None
        
        # 필수 환경변수 확인
        if not self.base_url or not self.app_key or not self.app_secret:
            raise ValueError("필수 환경변수가 .env 파일에 없습니다. (KIWOOM_API_BASE_URL, KIWOOM_APPKEY, KIWOOM_SECRETKEY)")
        
        # 최초 실행 시 토큰 발급 시도
        self._get_access_token()

    def _get_access_token(self):
        """
        인증 토큰(Access Token) 발급
        OAuth2 client_credentials 방식을 사용합니다.
        """
        path = "/oauth2/token" 
        url = self.base_url + path
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret
        }
        
        try:
            print(f"[Quantum] 토큰 발급 시도...")
            print(f"[Quantum] URL: {url}")
            print(f"[Quantum] AppKey: {self.app_key[:10]}...")
            
            res = requests.post(url, headers=headers, json=body)
            
            print(f"[Quantum] 응답 상태코드: {res.status_code}")
            print(f"[Quantum] 응답 내용: {res.text}")
            
            if res.status_code == 200:
                data = res.json()
                self.access_token = data.get('token')
                
                if self.access_token:
                    print(f"[Quantum] 토큰 발급 성공: {self.access_token[:20]}...")
                else:
                    print(f"[Error] 응답에 'token' 필드가 없습니다.")
                    print(f"[Error] 응답 데이터: {data}")
                    raise Exception("토큰 필드를 찾을 수 없음")
            else:
                print(f"[Error] 토큰 발급 실패 (Status: {res.status_code})")
                raise Exception(f"토큰 발급 실패: {res.status_code}")
            
        except Exception as e:
            print(f"[Error] 토큰 발급 중 오류: {e}")
            raise

    def get_header(self):
        """API 요청 시 필요한 공통 헤더"""
        return {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.access_token}",
            "api-id": "kt00018",
        }

    def get_price(self, code):
        """주식 호가 조회"""
        path = "/api/dostk/mrkcond"
        url = self.base_url + path
        
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.access_token}",
            "api-id": "ka10004",
        }
        
        # 삼성전자 호가 조회 파라미터
        # stk_cd 형식: KRX:종목코드 (KRX 거래소)
        params = {
            "stk_cd": f"KRX:{code}"  # 종목 코드 (KRX:005930 형식)
        }
        
        try:
            print(f"[Quantum] {code} 종목 시세 조회 요청 중...")
            print(f"[Quantum] URL: {url}")
            print(f"[Quantum] 요청 파라미터: {params}")
            
            res = requests.post(url, headers=headers, json=params)
            
            print(f"[Quantum] 응답 상태코드: {res.status_code}")
            print(f"[Quantum] 응답 내용: {res.text}")
            
            if res.status_code == 200:
                data = res.json()
                
                # return_code가 0이면 성공
                if data.get('return_code') == 0:
                    print(f"[Quantum] 조회 성공")
                    return data
                else:
                    print(f"[Error] API 오류: {data.get('return_msg')}")
                    return None
            else:
                print(f"[Error] 조회 실패 (Status: {res.status_code})")
                return None
                
        except Exception as e:
            print(f"[Error] 조회 중 오류: {e}")
            return None

    def get_realtime_price(self, code):
        """주식 실시간 호가 조회"""
        path = "/api/dostk/realtimeindex"
        url = self.base_url + path
        
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.access_token}",
            "api-id": "ka10006",  # 실시간 호가 조회용 api-id
        }
        
        # 실시간 호가 조회 파라미터
        params = {
            "stk_cd": f"KRX:{code}"  # 종목 코드 (KRX:005930 형식)
        }
        
        try:
            print(f"[Quantum] {code} 종목 실시간 시세 조회 요청 중...")
            print(f"[Quantum] URL: {url}")
            
            res = requests.post(url, headers=headers, json=params)
            
            print(f"[Quantum] 응답 상태코드: {res.status_code}")
            
            if res.status_code == 200:
                data = res.json()
                
                # return_code가 0이면 성공
                if data.get('return_code') == 0:
                    print(f"[Quantum] 실시간 호가 조회 성공")
                    return data
                else:
                    print(f"[Error] API 오류: {data.get('return_msg')}")
                    return None
            else:
                print(f"[Error] 실시간 호가 조회 실패 (Status: {res.status_code})")
                return None
                
        except Exception as e:
            print(f"[Error] 실시간 호가 조회 중 오류: {e}")
            return None

    def monitor_order(self, code, duration=10):
        """
        삼성전자 주문체결 정보 실시간 모니터링 (WebSocket)
        
        Args:
            code (str): 종목코드 (예: 005930)
            duration (int): 모니터링 시간 (초)
        """
        # WebSocket URL
        ws_url = "wss://api.kiwoom.com:10000/api/dostk/websocket"
        
        print(f"\n[Quantum] {code} 주문체결 실시간 모니터링 시작 ({duration}초)...")
        print(f"[Quantum] WebSocket 연결 중: {ws_url}")
        
        self.ws_connected = False
        self.ws = None
        
        def on_message(ws, message):
            """WebSocket 메시지 수신 핸들러"""
            try:
                data = json.loads(message)
                print(f"\n[Quantum] 실시간 데이터 수신:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"[Error] 메시지 파싱 오류: {e}")
        
        def on_error(ws, error):
            """WebSocket 에러 핸들러"""
            print(f"[Error] WebSocket 오류: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            """WebSocket 연결 종료 핸들러"""
            print(f"[Quantum] WebSocket 연결 종료")
            self.ws_connected = False
        
        def on_open(ws):
            """WebSocket 연결 성공 핸들러"""
            print(f"[Quantum] WebSocket 연결 성공")
            self.ws_connected = True
            
            # 주문체결 정보 등록 요청
            register_data = {
                "trnm": "REG",
                "grp_no": "0001",
                "refresh": "1",
                "data": [
                    {
                        "item": f"KRX:{code}",
                        "type": "00"  # 주문체결
                    }
                ]
            }
            
            try:
                ws.send(json.dumps(register_data))
                print(f"[Quantum] 주문체결 정보 등록 요청 전송")
            except Exception as e:
                print(f"[Error] 등록 요청 전송 오류: {e}")
        
        try:
            # WebSocket 클라이언트 생성
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                header=[f"Authorization: Bearer {self.access_token}"]
            )
            
            # WebSocket을 별도 스레드에서 실행
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
            # 지정된 시간만큼 모니터링
            time.sleep(duration)
            
            # 연결 해제 요청
            if self.ws_connected:
                unregister_data = {
                    "trnm": "REMOVE",
                    "grp_no": "0001",
                    "data": [
                        {
                            "item": f"KRX:{code}",
                            "type": "00"
                        }
                    ]
                }
                try:
                    self.ws.send(json.dumps(unregister_data))
                    print(f"[Quantum] 주문체결 정보 등록 해제 요청 전송")
                except Exception as e:
                    print(f"[Error] 등록 해제 요청 전송 오류: {e}")
            
            # WebSocket 종료
            self.ws.close()
            
        except Exception as e:
            print(f"[Error] 모니터링 중 오류: {e}")
