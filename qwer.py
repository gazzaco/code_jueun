
from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__) # flask를 사용하여 새로운 flask 애플리케이션 생성

@app.route('/') #flask 에서 URL라우팅을 설정하는데 사용 URL에 대해 지정된 함수 실행하도록 지시
def index(): #HTML폼을 포함한 문자열 반환하여 HTML로 렌더링함
    return ''' 
        <form action="/search" method="post">
            <input type="text" name="query" placeholder="검색어를 입력하세요">
            <input type="submit" value="검색">
        </form>
    '''
#return 함수가 반환할 값 지정(여기서는 HTML코드반환)
#1. 사용자가 폼을 제출하면 폼 데이터가 '/search' URL로 전송됨
#2. 사용자가 입력하지 않았을 때 "검색어입력하시오"라고 표시됨
#3. 제출버튼 생성 후 클릭시 폼 제출되기(제출버튼에 표시 될 텍스트를 "검색"으로)


#사용자가 제출한 검색어를 네이버 검색엔진에서 검색하고, 검색결과를 웹 페이지에 표시함
@app.route('/search', methods=['POST']) #'/search'경로에 대한 post요청처리
def search():
    query = request.form['query'] #사용자 입력 검색어 값 가져오기
    url = f"https://search.naver.com/search.naver?query={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    #1. 입력값 포함한 네이버 검색 URL 만들기
    #2. 웹스크래핑시 서버로부터 차단 피하기위해 필요함
    #3. request사용하여 네이버 검색 페이지에 GET요청 보내기

    if response.status_code == 200: # 요청 성공했는지 확인
        soup = BeautifulSoup(response.text, 'html.parser') #HTML파서 생성
        results = soup.find_all(class_='qbGlu') #class가 'ouxiq'인 모든 요소 찾기
        output = ''.join([str(result) for result in results]) #검색결과 문자열로 변환하여 큰문자열로 결합
    else: #요청실패시 출력메시지
        output = '검색 결과를 불러오는 데 실패했습니다.'
    
    # HTML 문자열을 렌더링
    return render_template_string('''
        <h1>검색 결과</h1>
        <div>{{ results|safe }}</div>
        <a href="/">다시 검색</a>
    ''', results=output)
#result 변수를 HTML로 렌더링 safe는 이 내용이 안전하다고 알려주는거 라는데 잘 모르겟음
#다시 검색페이지로 돌아갈 수 있는 링크 제공

if __name__ == '__main__':
    app.run(debug=True) #애플리케이션 실행 메서드 디버그 모드 활성화

#사진 띄우고 싶은데 띄우지를 못하겠어