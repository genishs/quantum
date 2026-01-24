# quantum
이 깃허브 저장소는 OSGEO 서울 공부 집단 구성원들이 같이 공부하는 Udemy의 [챗GPT와 파이썬으로 주식 자동매매 앱 및 웹 투자 리포트 만들기](https://www.udemy.com/course/gpt-trading/) 강좌에 대한 실습 코드를 담고 있습니다.

강좌와 다른 점은 다음과 같습니다.

* 강좌는 키움증권의 OCX를 쓰기 때문에 반드시 윈도우에서 32비트 파이썬을 써야 하나 본 저장소 소스는 키움증권 REST API를 쓰므로 OS 제한이 없습니다.
* 키움증권 Rest API 명세 등의 개발 정보 및 키 발급은 '[키움 REST API](https://openapi.kiwoom.com/main/home)' 를 참조하시기 바랍니다 (로그인, 키움증권 계좌 필수). 크롬 브라우저 이외의 다른 브라우저에서는 동작이 원활치 않습니다.
* 키움증권 Rest API를 이용하는 파이썬 코딩은 '[키움증권 REST API 기초부터 실전까지](https://www.youtube.com/playlist?list=PLlbsy38S8CCyrKyL4JTTkBE4L9m1cw7No)를 참조 바랍니다.
* 강좌는 Anaconda를 사용하나 본 저장소 소스는 uv 기반으로 작성합니다. pip, venv도 쓸 필요 없습니다.

## 개발 시작하는 방법
### 준비물
* 자신의 github 계정
* uv를 설치한 컴퓨터

### 사전 작업
1. 깃허브에 로그인
2. [손형수님의 quantum 깃허브 저장소](https://github.com/genishs/quantum)를 포크(fork)
3. 위에서 만들어진 자신의 깃허브 저장소를 자신의 PC로 clone 하여 로컬 저장소 생성

아래는 손형수님의 quantum 깃허브 저장소를 포크하여 만든 깃허브 저장소(ryudaewan/quantum)를 자신의 컴퓨터로 clone 하는 예시입니다. 윈도우 아니고 유닉스 쉘에서 돌린 것입니다.

```
$ git clone https://github.com/ryudaewan/quantum.git
Cloning into 'quantum'...
remote: Enumerating objects: 57, done.
remote: Counting objects: 100% (57/57), done.
remote: Compressing objects: 100% (37/37), done.
remote: Total 57 (delta 19), reused 45 (delta 10), pack-reused 0 (from 0)
Receiving objects: 100% (57/57), 20.10 KiB | 4.02 MiB/s, done.
Resolving deltas: 100% (19/19), done.

$ cd quantum

$
```
4. quantum 파이썬 환경 활성화
```
$ source .venv/Scripts/activate

(quantum) $
```

5. 프로젝트에 필요한 라이브러리 등을 내려받는 동기화 작업 실시. uv sync가 뭐하는 것인진 스스로 파악 요망.
```
(quantum) $ uv sync
Installed 7 packages in 231ms
 + certifi==2026.1      
 + charset-normalizer==3.4.4
 + idna==3.11
 + python-dotenv==1.2.1
 + requests==2.32.5
 + urllib3==2.6.3
 + websocket-client==1.9.0

(quantum) $ 
```

윈도우에서도 유닉스 쉘을 쓸 수 있는데, 아래와 같은 방법이 있습니다.
* 윈도우용 Git 깔면 같이 깔리는 bash를 씁니다.
* WSL을 씁니다.

## 설정파일(config.toml)
아래는 본 프로젝트에서 만드는 애플리케이션 설정 파일인 config.toml 예시입니다. 키움증권 rest api는 모의 투자용과 실거래용
두 개가 있습니다. 따러서 설정 파일도 공통 부분과 실거래용 (real_trading), 모의 투자용(paper_trading)으로
나뉩니다.

```
# 실거래 / 모의 투자 상관없이 모두 쓰이는 설정 정보
[default]
is_paper_trading = "False" # True: 모의 투자, False: 실거래

# 실거래 api 호출 관련 설정 정보
[real_trading]
base_url = "https://api.kiwoom.com"
api_key_file = "keys/api_keys_real_trading.toml" # api_keys_real_trading_sample.toml 복사해서 만드세요. 인생 꼬이기 싫으시면 이 파일은 절대 github에 공표하지 말 것!

# 모의 투자 api 호출 관련 설정 정보
[paper_trading]
base_url = "https://mockapi.kiwoom.com"
api_key_file = "keys/api_keys_paper_trading.toml" # api_keys_paper_trading_sample.toml 복사해서 만드세요. 인생 꼬이기 싫으시면 이 파일은 절대 github에 공표하지 말 것!
```

## 키 파일 (key file)
키움 rest api 사이트에서 발급 받는 app_key, app_secret 값 및, 토큰 발급용 api를 호출하여 발급 받는 토큰, 그 토큰의 만료 일시를 저장하는 파일입니다.
config.toml 의 is_paper_trading 값이 "True" 면 모의 투자 api 호출용 키 파일을 읽고, "False" 면 실거래 api 호출용 키 파일 읽습니다. 

이 키 파일 정보가 노출되면 굉장히 큰 금전적 손실 야기할 수 있으므로 이 키 파일들은 깃 버전 관리 대상에 넣지 마시고, 깃허브에 push 절대로 하시면 안됩니다!!!

```
#####################################################################
#      api_keys_paper_trading.toml은 이 파일 복사해서 만드세요.      #
#####################################################################

# 모의 투자용 API 키 정보
[paper_trading]
# api key 발급에 필요한 정보. 키움 rest api 개발자 사이트에서 신청하여 받는다.
app_key = "<<사용자의 모의 투자용 access token 발급 시 쓰는 app key>>"
app_secret = "<<사용자의 모의 투자용 access token 발급 시 쓰는  app_secret>>"

# 키움 rest api 호출 시 http 요청 헤더의 Authentication 필드에 넣어야 할 값.
access_token = "<<사용자의 모의 투자용 access token>>"
# api_key 만료 일시
access_token_expiration_datetime = "<<사용자의 모의 투자용 access token 만료 일시>>" # 키 발급 api 응답의 expires_dt 필드 값을 그대로 쓰시면 됩니다.

```