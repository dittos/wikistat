# WikiStat


## 환경

* Python 2.x
* pip


## 준비

    pip install -r requirements.txt

virtualenv 사용을 권장합니다.


## 생성

수집: `logs` 디렉토리에 날짜별 통계 파일이 저장됩니다.

    python -m wikistat.collect

리포트 생성: `index.html`이 생성됩니다.

    python -m wikistat.report

두가지를 주기적으로 실행해주면 됩니다.
