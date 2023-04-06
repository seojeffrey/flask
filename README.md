# Flask Project

* 작성자: 서성빈
* 최초 작성일: 2023/03/30


### 구현한환경
* Flask + Gunicorn + Nginx
* alembic library
* Docker

### 실행방법
1. docker-compose -f docker-compose.yml up -d
2. alembic upgrade head

#. 완료


### test 툴 
* test.http (intellij에서 사용 가능)
* http://localhost:5000  * 웹뷰 - 로그인만 가능