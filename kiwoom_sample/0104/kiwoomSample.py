import requests
import json
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# 1. 접근토큰 발급 함수
def get_token(app_key, app_secret):
    """접근토큰을 발급받는 함수"""
    host = 'https://api.kiwoom.com'  # 실전투자 URL
    endpoint = '/oauth2/token'
    url = host + endpoint
    
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    
    data = {
        'grant_type': 'client_credentials',
        'appkey': app_key,
        'secretkey': app_secret
    }

    response = requests.post(url, headers=headers, json=data)

    print('--- 토큰 발급 응답 ---')
    print('Token 발급 응답 Code:', response.status_code)
    if response.status_code == 200:
        token_data = response.json()
        print('Token 발급 응답 Body:', json.dumps(token_data, indent=4, ensure_ascii=False))
        return token_data.get('token')
    else:
        print('Token 발급 실패:', response.text)
        return None

# 2. 계좌평가잔고내역요청 함수
def get_account_balance(token, data, cont_yn='N', next_key=''):
    """계좌평가잔고내역을 조회하는 함수"""
    host = 'https://api.kiwoom.com'  # 실전투자
    endpoint = '/api/dostk/acnt'
    url = host + endpoint

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'authorization': f'Bearer {token}',
        'cont-yn': cont_yn,
        'next-key': next_key,
        'api-id': 'kt00018',
    }

    response = requests.post(url, headers=headers, json=data)

    print('\n--- 잔고 조회 응답 ---')
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))


# 실행 구간
if __name__ == '__main__':
    # --- .env 파일에서 API 인증정보 로드 ---
    MY_APP_KEY = os.getenv('KIWOOM_APPKEY')
    MY_APP_SECRET = os.getenv('KIWOOM_SECRETKEY')
    
    if not MY_APP_KEY or not MY_APP_SECRET:
        print("오류: .env 파일에서 KIWOOM_APPKEY와 KIWOOM_SECRETKEY를 찾을 수 없습니다.")
        print("프로젝트 루트 디렉토리에 .env 파일을 생성하고 API 인증정보를 입력하세요.")
        exit(1)

    # -------------------------

    # 1. 접근토큰 발급
    access_token = get_token(MY_APP_KEY, MY_APP_SECRET)

    # 2. 토큰 발급 성공 시 잔고 조회 실행
    if access_token:
        print(f"\n발급된 Access Token: {access_token[:15]}...") # 토큰 일부만 출력

        # 계좌평가잔고내역요청 파라미터
        params = {
            'qry_tp': '1',  # 조회구분 1:합산, 2:개별
            'dmst_stex_tp': 'KRX',  # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
        }

        # 3. 잔고 조회 API 호출
        get_account_balance(token=access_token, data=params)
    else:
        print("\nAccess Token 발급에 실패하여 잔고 조회를 실행할 수 없습니다.")
