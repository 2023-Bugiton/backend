# 부기톤 "소확행"
### 실행과정
1. 이미지와 같이 복사하기 버튼을 클릭한다.
<img width="1409" alt="image" src="https://github.com/2023-Bugiton/backend/assets/70803824/87e42815-7f86-4aff-9fb0-405622c9abe6">
<br><br>
2. 터미널 창에서 원하는 폴더 위치에서 `git clone "복사한 링크"` 를 입력한다. (git 설치 필수)
<br><br>
3. 다운 받은 폴더 위치로 이동한다. (최상위 폴더에 manage.py 파일이 위치하도록) ex) `cd bugiton`
<br>   만약 현재 폴더 위치에 manage.py 파일이 있다면 이동할 필요 없다.
<br><br>
5. 가상환경을 만들어준다.
<h3>window</h3>
python -m venv venv

<h3>mac</h3>
python3 -m venv venv

<br><br>
6. 가상환경을 실행한다.
<h3>window</h3>
venv/scripts/activate

<h3>mac</h3>
source venv/bin/activate

<br><br>
7. pip install -r requirements.txt 를 터미널 창에서 실행한다.

<br><br>
8번 이후부터 mac일 경우 python 대신 python3로 쓴다.
8. python manage.py makemigrations
9. python manage.py migrate
10. python manage.py migrate --run-syncdb
11. 서버 실행 python manage.py runserver
