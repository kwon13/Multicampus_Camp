from tqdm import tqdm
from seleniumwire import webdriver 
from time import sleep
import requests
import json
import pandas as pd

def google_reviews(store_list,gu,count=10):

    #드라이버 실행
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('./chromedriver',options=options)   #chromedriver 경로 지정!
    driver.get('https://www.google.co.kr/maps')
    sleep(3)

    # 리스트 형식으로 저장된 가게 하나씩 검색
    for store in store_list:
        count=count
        driver.get('https://www.google.co.kr/maps')
        result_list=[]
        sleep(3)
        query_input=driver.find_element_by_class_name('tactile-searchbox-input')
        query_input.send_keys(gu+store+'\n')
        
        # 의도한 가게와 검색결과가 같은지 확인
        sleep(5)
        check=input('일치하는 가게를 클릭 후 y를 눌러주세요(이외 멈춤)')
        if check.upper()=='Y':
            pass
        else:
            break
        now_url=driver.current_url
        
        # 리뷰 더보기로 이동
        more_btn=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button')
        more_btn.click()
        views=int(more_btn.text[2:-1])//10
        
        # div태그 스크롤 
        sleep(8)
        js_scripts = '''
        let aa = document.getElementsByClassName('section-scrollbox')[0];
        setTimeout(()=>{aa.scroll(0,1000000)}, 1000);
        '''
        driver.execute_script(js_scripts)
        sleep(3) 
        
        # 헤더값 찾기
        for request in driver.requests:
            if request.response:
                pb=request.url.split('pb=')
                if len(pb)==2:
                    if pb[1][:6]=='!1m2!1':
                        url_l=request.url.split('!2m2!1i')
                        break
                        
        # json파일 들고와 리뷰 10개씩 저장하기
        # 리뷰의 수가 count보다 작을 경우 count를 리뷰의 수로 변경
        if count>views:
            for number in tqdm(range(views)):
                resp=requests.get((url_l[0]+'!2m2!1i'+'{}'+url_l[1]).format(number))
                review = json.loads(resp.text[5:])
                for user in range(10):
                    result_list.append({
                        'ID':review[2][user][0][1],
                        '내용':review[2][user][3],
                        '날짜':review[2][user][1],
                        '별점':review[2][user][4]})
        else:
            for number in tqdm(range(count)):
                resp=requests.get((url_l[0]+'!2m2!1i'+'{}'+url_l[1]).format(number))
                review = json.loads(resp.text[5:])
                for user in range(10):
                    result_list.append({
                        'ID':review[2][user][0][1],
                        '내용':review[2][user][3],
                        '날짜':review[2][user][1],
                        '별점':review[2][user][4]})
                    
        # csv로 저장
        df=pd.DataFrame(result_list)
        df.to_csv('{}.csv'.format(store))


# 검색하고 싶은 가게 리스트 형식으로 저장

store_list=['알베르','아우어베이커리 도산본점','C27','카페 노티드','테라로사 코엑스점','겟썸커피','클로리스 티 룸 코엑스몰점','트리아농',
'카페413프로젝트','에이블','듀자미','세시셀라 도산공원점','테라로사 포스코센터점','겟썸커피','기욤 청담점','카페 마마스 코엑스점','우유니아이스크림','더달달',
'티컬렉티브','빌리엔젤 강남역점','카페 마마스 역삼점','이디야커피랩','아우어베이커리 가로수길점','르알래스카 가로수길점'
,'버터핑거 팬케익스 청담동점','로네펠트','맘마미아','이코복스','꽁티드툴레아','우나스 (Unas)','메종드라 카테고리','마크레인 커피','베질루르','파넬 카페'
,'블루보틀 역삼 카페','식물학','랑데자뷰','클로리스 티 앤 커피','타르틴 베이커리 도산점','더닐크팩토리카페','10 꼬르소꼬모 카페',
'타이거슈가 강남점','투썸플레이스 신논현역점','폴인 팬케이크 강남점','컬렉션라운지','스템커피','브라이언스커피','더앨리 가로수길점','펠트 도산공원점','쁠로13']

google_reviews(store_list,'강남',4)