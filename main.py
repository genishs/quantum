from core.api_handler import KiwoomREST

def main():
    print("="*30)
    print("   Quantum (REST API Ver.)   ")
    print("="*30)

    # 브로커 객체 생성 (자동으로 토큰 발급 시도)
    broker = KiwoomREST()
    
    # 삼성전자(005930) 가격 조회 테스트
    print("\n[1] 호가 조회:")
    price_info = broker.get_price("005930")
    print(f"결과: {price_info}")
    
    # 삼성전자(005930) 실시간 호가 조회 테스트
    print("\n[2] 실시간 호가 조회:")
    realtime_info = broker.get_realtime_price("005930")
    print(f"결과: {realtime_info}")
    
    # 삼성전자(005930) 주문체결 실시간 모니터링
    print("\n[3] 주문체결 실시간 모니터링:")
    broker.monitor_order("005930", duration=10)

if __name__ == "__main__":
    main()