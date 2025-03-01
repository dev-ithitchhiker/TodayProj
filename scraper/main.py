import json
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin
from pytrends.request import TrendReq
import ssl
# import matplotlib.pyplot as plt  # 차트 출력용 (Remove this line)
import pandas as pd  # 데이터프레임 타입 확인용
from requests_html import HTMLSession  # new import for direct scraping
from collections import Counter  # 추가: 빈도 수 계산을 위한 모듈

# 네이버 검색 순위 조회 함수 (Naver DataLab API 사용)
def get_naver_top_keywords():
    client_id = "iadTa6sAGB10LJN2NyqX"
    client_secret = "Y3jQXZ6KD8"
    url = "https://openapi.naver.com/v1/datalab/search"
    body = json.dumps({
        "startDate": "2023-01-01",
        "endDate": "2023-12-31",
        "timeUnit": "month",
        "keywordGroups": [
            {"groupName": "한글", "keywords": ["한글", "korean"]},
            {"groupName": "영어", "keywords": ["영어", "english"]}
        ],
        "device": "pc",
        "ages": ["1", "2"],
        "gender": "f"
    })

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    req.add_header("Content-Type", "application/json")
    
    context = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(req, data=body.encode("utf-8"), context=context)
        retCode = response.getcode()
        if (retCode == 200):
            response_body = response.read()
            data = json.loads(response_body.decode('utf-8'))
            keywords = []
            if 'results' in data:
                for result in data['results']:
                    if 'keywords' in result:
                        keywords.extend(result['keywords'])
            else:
                print("Unexpected API response structure.")
            return keywords
        else:
            print(f"Error Code: {retCode}")
            return []
    except Exception as e:
        print(f"Error retrieving Naver DataLab keywords: {e}")
        return []

# 구글 트렌드 조회 함수 (수정됨)
def get_google_trend_keywords():
    pytrends = TrendReq(geo='KR', timeout=(10, 25), retries=2, backoff_factor=0.1)
    try:
        try:
            trending_searches = pytrends.trending_searches()
        except Exception as e:
            try:
                print(f"Error retrieving trending_searches : {e}")
                trending_searches = pytrends.realtime_trending_searches(pn='KR')
            except Exception as e:
                print(f"Error retrieving realtime_trending_searches: {e}")
                trending_searches = pytrends.today_searches(pn='KR')
        
        print("Raw Google Trends data:")
        print(trending_searches)
        
        if isinstance(trending_searches, pd.DataFrame):
            if trending_searches.empty:
                print("Empty DataFrame from Google Trends.")
                return []
            if 'exploreLink' in trending_searches.columns:
                keywords = trending_searches['exploreLink'].apply(lambda x: x.split('=')[1].split('&')[0]).tolist()
            else:
                keywords = trending_searches.iloc[:, 0].tolist()
        elif isinstance(trending_searches, pd.Series):
            keywords = trending_searches.tolist()
        else:
            print("Unknown data structure returned from Google Trends.")
            return []
        
        from urllib.parse import unquote_plus  # URL 디코딩 함수
        import re  # 정규식 모듈
        # First, decode each keyword string
        decoded_keywords = [unquote_plus(kw) for kw in keywords]
        # Then, extract only the substring between "q=" and "&"
        final_keywords = []
        for k in decoded_keywords:
            m = re.search(r'q=([^&]+)', k)
            if m:
                final_keywords.append(m.group(1))
            else:
                final_keywords.append(k)
        print("Final Extracted Keywords:", final_keywords)
        return final_keywords
    except Exception as e:
        print(f"Error retrieving Google Trends: {e}")
        return []

# 새 함수: Google Trends 웹페이지를 직접 스크래핑하여 상위 10개 키워드 조회 (수정됨)
def get_top10_google_trend_direct():
    session = HTMLSession()
    r = session.get("https://trends.google.co.kr/trending?geo=KR")
    r.html.render(sleep=2, scrolldown=2)
    main_section = r.html.find("[role='main']", first=True)
    if not main_section:
        print("Main section not found.")
        return []
    selector = "#trend-table > div.enOdEe-wZVHld-zg7Cn-haAclf > table > tbody:nth-child(3) > tr > td.enOdEe-wZVHld-aOtOmf.xm9Xec > div > div:nth-child(1) > div"
    elements = main_section.find(selector)
    # print(f"Selector '{selector}' found {len(elements)} elements")
    keywords = []
    for elem in elements:
        if elem.text.strip():
            # Split by newline and take the first part (the actual keyword)
            keyword = elem.text.strip().split('\n')[0]
            keywords.append(keyword)
    print("Directly Scraped Keywords:", keywords)
    return keywords[:10]

# 요청 에러 핸들링 함수
def safe_request(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} for url: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    return None

# 구글 뉴스 스크래핑 함수 (수정됨: urljoin 사용)
def scrape_google_news(keyword):
    url = f'https://news.google.com/search?q={keyword}&hl=ko&gl=KR&ceid=KR%3Ako'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Referer": "https://www.google.com/"
    }
    response = safe_request(url, headers)
    if not response:
        return []
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for item in soup.select('article'):
            title_tag = item.select_one('h3 a')
            if title_tag and title_tag.has_attr('href'):
                title = title_tag.text.strip()
                # urljoin을 사용하여 상대 URL을 절대 URL로 변환
                link = urljoin('https://news.google.com/', title_tag['href'])
                articles.append({
                    'source': 'Google News',
                    'keyword': keyword,
                    'title': title,
                    'url': link,
                })
        return articles
    except Exception as e:
        print(f"Error parsing Google News for {keyword}: {e}")
        return []

# 네이버 뉴스 스크래핑 함수
def scrape_naver_news(keyword):
    url = f'https://search.naver.com/search.naver?where=news&query={keyword}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Referer": "https://www.naver.com/"
    }
    response = safe_request(url, headers)
    if not response:
        return []
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for item in soup.select('.news_tit'):
            if item.has_attr('href'):
                title = item.text.strip()
                link = item['href']
                articles.append({
                    'source': 'Naver News',
                    'keyword': keyword,
                    'title': title,
                    'url': link,
                })
        return articles
    except Exception as e:
        print(f"Error parsing Naver News for {keyword}: {e}")
        return []

# 트위터(X) 트렌드 스크래핑 (API 필요, 현재 Mock 데이터 사용)
def scrape_twitter(keyword):
    return [
        {'source': 'Twitter', 'keyword': keyword, 'title': f'{keyword} 관련 트윗 1', 'url': 'https://twitter.com/example1'},
        {'source': 'Twitter', 'keyword': keyword, 'title': f'{keyword} 관련 트윗 2', 'url': 'https://twitter.com/example2'}
    ]

# 인스타그램 해시태그 스크래핑 (API 필요, 현재 Mock 데이터 사용)
def scrape_instagram(keyword):
    return [
        {'source': 'Instagram', 'keyword': keyword, 'title': f'{keyword} 인기 게시물 1', 'url': 'https://instagram.com/example1'},
        {'source': 'Instagram', 'keyword': keyword, 'title': f'{keyword} 인기 게시물 2', 'url': 'https://instagram.com/example2'}
    ]

# 여러 키워드에 대해 자동 스크래핑
def scrape_multiple_topics():
    all_news = []
    # naver_keywords = get_naver_top_keywords()
    google_top10_keywords = get_top10_google_trend_direct()
    google_keywords = get_google_trend_keywords()
    
    # 가져온 키워드를 합치고 중복 제거
    combined_keywords = list(set(google_top10_keywords + google_keywords))
    
    # 상위 10개 키워드 사용 (필요에 따라 조정)
    top_keywords = combined_keywords[:10]
    
    for keyword in top_keywords:
        print(f"Scraping news for: {keyword}")
        all_news.extend(scrape_google_news(keyword))
        all_news.extend(scrape_naver_news(keyword))
        all_news.extend(scrape_twitter(keyword))
        all_news.extend(scrape_instagram(keyword))
        time.sleep(5)  # 서버 과부하 방지
    return all_news

# 새 함수: 전체 뉴스 결과에서 'keyword' 필드를 취합하여 빈도수가 높은 상위 10개 키워드를 출력
def get_top10_frequent_keywords(news_results):
    all_keywords = [article['keyword'] for article in news_results if 'keyword' in article]
    counter = Counter(all_keywords)
    top10 = counter.most_common(10)
    print("Top 10 Frequent Keywords:")
    for kw, freq in top10:
        print(f"{kw}: {freq}")
    return top10

def scrape_dcinside_board_list(board_id="dcbest"):
    BASE_URL = "https://gall.dcinside.com/board/lists"
    params = {"id": board_id}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(BASE_URL, params=params, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    soup = BeautifulSoup(resp.content, "html.parser")
    # Find all rows in tbody
    contents = soup.find("tbody").find_all("tr")
    posts = []
    for row in contents:

        # skip when '#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child(1) > td.gall_num' value is not number
        try:
            int(row.find("td", class_="gall_num").text)
        except:
            continue

        post = {}
        # 제목 추출
        title_tag = row.find("a")
        # 제목 추출할 때 <strong> 태그가 존재하면 태그 내용만 제거하여 제목에 추가
        strong_tag = title_tag.find("strong")
        if strong_tag:
            post["title"] = title_tag.text.replace(strong_tag.text, "").strip()
        else:
            post["title"] = title_tag.text.strip()

        # 글쓴이, IP 추출
        writer_cell = row.find("td", class_="gall_writer ub-writer")
        if writer_cell:
            nickname_tag = writer_cell.find("span", class_="nickname")
            post["writer"] = nickname_tag.text.strip() if nickname_tag and nickname_tag.text else "없음"
            ip_tag = writer_cell.find("span", class_="ip")
            post["ip"] = ip_tag.text.strip() if ip_tag and ip_tag.text else "없음"
        else:
            post["writer"] = "없음"
            post["ip"] = "없음"
        # 날짜 추출
        date_tag = row.find("td", class_="gall_date")
        if date_tag:
            date_attrs = date_tag.attrs
            if len(date_attrs) == 2 and "title" in date_attrs:
                post["date"] = date_attrs["title"]
            else:
                post["date"] = date_tag.text.strip()
        else:
            post["date"] = "없음"
        # 조회수 추출
        views_tag = row.find("td", class_="gall_count")
        post["views"] = views_tag.text.strip() if views_tag and views_tag.text else "0"
        # 추천수 추출
        recommend_tag = row.find("td", class_="gall_recommend")
        post["recommend"] = recommend_tag.text.strip() if recommend_tag and recommend_tag.text else "0"
        posts.append(post)
    return posts

# 새 함수: 게시물들의 조회수 평균을 내고 평균보다 높은 게시물만 반환
def filter_posts_by_average_views(posts):
    view_counts = []
    for post in posts:
        try:
            views_str = post["views"].strip()
            if views_str in ("-", ""):
                v = 0
            else:
                v = int(views_str.replace(",", ""))
        except Exception as e:
            v = 0
        view_counts.append(v)
    if not view_counts:
        return [], 0
    avg_views = sum(view_counts) / len(view_counts)
    print(f"Average views: {avg_views:.2f}")
    filtered = [post for post in posts if int(post["views"].replace(",", "")) > avg_views]
    return filtered, avg_views

if __name__ == '__main__':
    
    # news_results = scrape_multiple_topics()
    # print(json.dumps(news_results, indent=2, ensure_ascii=False))
    # get_top10_frequent_keywords(news_results)

    # # get dc_inside post
    dc_posts = scrape_dcinside_board_list("dcbest")
    # print("DC Inside Board Posts:")
    # for i, post in enumerate(dc_posts, 1):
    #     print(f"{i}. {post['title']} / {post['date']} / {post['views']} / {post['recommend']}")
    
    # # 필터링: 평균 조회수보다 높은 게시물만 출력
    filtered_posts, avg_views = filter_posts_by_average_views(dc_posts)
    print(f"\nDC Inside Board Posts with Views Higher Than Average({avg_views}):")
    for i, post in enumerate(filtered_posts, 1):
        print(f"{i}. {post['title']} / {post['date']} / {post['views']} / {post['recommend']}")

    # Do split post title by space and count the frequency of each word
    title_words = []
    for post in filtered_posts:
        title_words.extend(post["title"].split())
    word_counter = Counter(title_words)
    print("\nTop 10 Frequent Words in Post Titles:")
    for word, freq in word_counter.most_common(10):
        print(f"{word}: {freq}")
