import requests
import os
import json
from dotenv import load_dotenv

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
