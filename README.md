# 트위치 라이브 다운로더
## 기능
수행 시 자동으로 해당 스트리머의 방송 시작을 감지하여 자동으로 다운로드 합니다.
### 광고제거 기능
트위치 터보나 해당 채널 구독자만 가능합니다.
아래 이미지와 같이 개발자 도구에서 cookies 를 찾아 해당 키값을 복사합니다.
account.example.json 파일에 각 키에 해당하는 값을 붙여넣고 해당 파일명을 account.json 으로 변경합니다.
![explain remove ad](https://github.com/MinsuChae/twitch_live_downloader/blob/main/image.png?raw=true)
### 저장 장소
info.json 파일에서 output 파일을 지정합니다.
윈도우를 기준으론 파일 탐색기에서 경로를 복사하여 붙여넣은 후 \\가 나오는 부분을 \\\\으로 변경해주시기 바랍니다.
## 수행방법
### 스탠다드 얼론
윈도우 기반으로 작성하였습니다.
크롬 버전은 115 버전을 기준으로 작성하였습니다.
python 3.11 에서 테스트를 진행하였습니다.
pip install -e requirements.txt
을 통해 필요한 라이브러리를 수행하시기 바랍니다.
python download.py streamer_id
streamer_id 에 자동으로 녹화할 스트리머 ID를 넣어주세요.
### Docker
우분투를 기반으로 작성하였습니다.
수행에 필요한 파일들이 전부 있습니다.
docker build -t twitch_download .
을 통해 해당 이미지를 빌드합니다.

docker create -e USER=streamer_id --restart=always -v host_path:container_path --name twitch_down twitch_download
를 통해 컨테이너를 생성합니다.
streamer_id 에 자동으로 녹화할 스트리머 ID를 넣어주세요.
host_path 는 리눅스에서 저장할 경로입니다.
container_path 는 내부 컨테이너에서 사용할 경로입니다. 기본값은 /Download 입니다.
해당값 변경 시 info.json 파일 값도 변경하셔야 합니다. 

docker start twitch_down
를 통해 컨테이너를 수행합니다.
(내부적으로 python 을 foreground로 수행되기 때문에 위와 같이 실행하시는게 편합니다.)
## 사용하는 프로그램 및 라이브러리
[python](https://www.python.org/)
[selenium-wire](https://pypi.org/project/selenium-wire/)
[requests](https://pypi.org/project/requests/)
[ffmpeg](https://www.ffmpeg.org/)
[chrome](https://www.google.com/chrome/)
[chromedriver](https://chromedriver.chromium.org/downloads)


