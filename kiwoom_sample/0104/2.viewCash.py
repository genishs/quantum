import requests
import json

# 계좌평가잔고내역요청
def fn_kt00018(token, data, cont_yn='N', next_key=''):
    host = 'https://api.kiwoom.com'  # 실전투자
    endpoint = '/api/dostk/acnt'
    url = host + endpoint

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
        'authorization': f'Bearer {token}',  # 접근토큰
        'cont-yn': cont_yn,  # 연속조회여부
        'next-key': next_key,  # 연속조회키
        'api-id': 'kt00018',  # TR명
    }

    response = requests.post(url, headers=headers, json=data)

    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    MY_ACCESS_TOKEN = 'Z7FjNZ69I0TvgCqgrMbkfHTzactTYgAz8_cJebVcvWj_l_8IMUX1hiYhVspzfkvKj6JBwaL06O8_GDdza1bNtg'  # 접근토큰

    params = {
        'qry_tp': '1',  # 조회구분 1:합산, 2:개별
        'dmst_stex_tp': 'KRX',  # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
    }

    fn_kt00018(token=MY_ACCESS_TOKEN, data=params)