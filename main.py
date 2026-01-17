from core.api_handler import KiwoomREST

def main():
    print("="*30)
    print("   Quantum (REST API Ver.)   ")
    print("="*30)

    # 브로커 객체 생성 (자동으로 토큰 발급 시도)
    broker = KiwoomREST()
    
    # 삼성전자(005930) 가격 조회 테스트
    price_info = broker.get_price("005930")
    print(f"결과: {price_info}")

if __name__ == "__main__":
    main()