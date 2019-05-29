
# 소스 폴더
 - 모듈별 소스코드 기재
 동일한 소스 코드를 여러 폴더로 중복 관리하지 않기 위해 아래의 파일경로에서 모듈을 관리합니다. 
 - 댓글 긍정/부정/중립 분류 모듈 코드 -> src//ohtube/yougam/code/predict_sentiment
 - 댓글 6가지 감성 분류 모듈 코드 -> src/ohtube/yougam/code/predict_sentiment6
 - 영상 속 표정 분석 모듈 코드 -> src/ohtube/yougam/code/Video_module
 - 웹 모듈 코드 -> src/ohtube/yougam/templates/yougam


# 소스 실행

소스코드 실행시 pip3 install -r requirements.txt 명령어를 통해 requirements속 pip패키지들을 설치 합니다. 
추가로 jdk까지 아래의 명령어로 설치
- $ sudo apt update
- $ sudo apt install default-jre
- $ sudo apt install default-jdk

ohtube 폴더 속 manage.py가 있는 폴더에서 아래의 명령어로 실행
- python3 manage.py runsslserver 0.0.0.0:8000 
