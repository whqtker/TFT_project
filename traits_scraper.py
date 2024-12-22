import requests
from bs4 import BeautifulSoup
import json
from db import insert_data

def traits_scraper(season):
    # 웹 페이지 URL
    url = f'https://lolchess.gg/synergies/set{season}/table'

    # HTML 가져오기
    response = requests.get(url)
    html_content = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_content, 'html.parser')

    # <script> 태그 찾기
    script_tag = soup.find('script', id='__NEXT_DATA__')

    # JSON 데이터 추출
    if script_tag:
        json_data = script_tag.string
        data = json.loads(json_data)  # JSON 문자열을 파이썬 객체로 변환

        try:
            set = data['props']['pageProps']['set']
            traits_data = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['traits']

            for trait in traits_data:
                trait['set'] = set

            insert_data('tft', 'traits', traits_data)

        except KeyError as e:
            print(f"데이터 구조에서 경로를 찾을 수 없습니다: {e}")
    else:
        print('해당 <script> 태그를 찾을 수 없습니다.')