import requests
import json
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# 1. 접근토큰 발급 함수
def fn_au10001(data, base_url):
    endpoint = '/oauth2/token'
    url = base_url + endpoint

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }

    response = requests.post(url, headers=headers, json=data)

    print('Token 발급 응답 Code:', response.status_code)
    print('Token 발급 응답 Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Token 발급 응답 Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))

    return response.json()

# 2. 예시 조회 API 함수 (예: 계좌 잔고 조회)
def fn_au20001(token, base_url):
    endpoint = '/v1/account/balance'  # 예시 엔드포인트 (실제 API 문서 참고 필요)
    url = base_url + endpoint

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': f"Bearer {token}"
    }

    # 조회에 필요한 요청 데이터 예시 (계좌번호 등은 API 문서 참고)
    data = {
        # 'acc_no': '1234567890',  # 계좌번호 등 필요 시 추가
    }

    response = requests.post(url, headers=headers, json=data)

    print('조회 응답 Code:', response.status_code)
    print('조회 응답 Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('조회 응답 Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))

    return response.json()

if __name__ == '__main__':
    # 1) .env 파일에서 API 인증정보 및 설정값 로드
    appkey = os.getenv('KIWOOM_APPKEY')
    secretkey = os.getenv('KIWOOM_SECRETKEY')
    api_base_url = os.getenv('KIWOOM_API_BASE_URL')
    
    if not appkey or not secretkey or not api_base_url:
        print("오류: .env 파일에서 필수 환경변수를 찾을 수 없습니다.")
        print("프로젝트 루트 디렉토리의 .env 파일을 확인하세요.")
        exit(1)
    
    # 2) 접근토큰 발급 요청 데이터
    params = {
        'grant_type': 'client_credentials',
        'appkey': appkey,
        'secretkey': secretkey
    }

    # 3) 토큰 발급
    token_response = fn_au10001(data=params, base_url=api_base_url)
    access_token = token_response.get('token', '')

    if access_token:
        print(f"발급된 Access Token: {access_token}")

        # 4) 토큰으로 조회 API 호출 (주석 해제 후 사용)
        # 조회 결과 예시 출력
        # 조회 API는 실제 API 문서에 맞게 엔드포인트와 요청 데이터를 수정하세요.
        # response = fn_au20001(access_token, api_base_url)
    else:
        print("Access Token 발급 실패")