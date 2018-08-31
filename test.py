import requests
from bs4 import BeautifulSoup

url = 'https://movie.naver.com/movie/running/current.nhn'
req = requests.get(url).content
bs4 = BeautifulSoup(req,"html.parser")

title_tag = bs4.select('dt.tit > a')
star_tag = bs4.select('dl.info_star > dd > div > a > span.num')
reserve_tag = bs4.select('dl.info_exp > dd > div > span.num')
img_tag = bs4.select('div.thumb > a > img')

movie_dict = {}

for i in range(0,10) :
    movie_dict[i] = {
        "title" : title_tag[i].text,
        "star" : star_tag[i].text,
        "reserve" : reserve_tag[i].text,
        "img" : img_tag[i].get('src')
    }

print(movie_dict)