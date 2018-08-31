import os
import random
import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello() :
    return '챗봇 페이지 입니다.'
    
@app.route('/keyboard')
def keyboard() : 
    keyboard = {
        "type" : "buttons",
        "buttons" : ["메뉴", "로또", "고양이", "영화"]
        }
    return jsonify(keyboard)

@app.route('/message', methods =['POST'])
def message() : 
   user_msg = request.json['content']
   img_bool = False
   
   if user_msg == "메뉴" :
       menu = ["갈비탕", "소갈비살", "짬뽕", "대하구이","삼겹살"]
       return_msg = random.choice(menu)
   elif user_msg == "로또":
       return_msg = "행운의 로또 번호 : " + str( sorted( random.sample(range(1,46) ,6) ) )
   elif user_msg == "고양이" :
       img_bool = True
       url = 'https://api.thecatapi.com/v1/images/search?mime_types=jpg'
       req = requests.get(url).json()
       return_img = req[0]['url']
       return_msg = "고양이 귀엽다"
   elif user_msg == "영화" :
       url = 'https://movie.naver.com/movie/running/current.nhn'
       req = requests.get(url).content
       bs4 = BeautifulSoup(req,"html.parser")
       
       title_tag = bs4.select('dt.tit > a')
       star_tag = bs4.select('dl.info_star > dd > div > a > span.num')
       reserve_tag = bs4.select('dl.info_exp > dd > div > span.num')
       img_tag = bs4.select('div.thumb > a > img')
       
       movie_dict = {}

       for i in range(0,10):
            movie_dict[i] = {
               "title" : title_tag[i].text,
               "star" : star_tag[i].text,
               "reserve" : reserve_tag[i].text,
               "img" : img_tag[i].get('src')
           }
       pick_movie = movie_dict[random.randrange(0,10)]
       return_msg = "영화제목 : %s\n평점 : %s\n예매율 : %s" % (pick_movie['title'], pick_movie['star'], pick_movie['reserve'])
       return_img = pick_movie['img']
       img_bool = True
        
   else : 
       return_msg = "카테고리만 사용 가능!!"
       
   if img_bool == True :
       return_json = {
           "message" : {
                "text" : return_msg,
                "photo" : {
                    "url" : return_img,
                    "height" : 630,
                    "width" : 720,
                }
           },
           "keyboard" : {
                "type" : "buttons",
                "buttons" : ["메뉴", "로또", "고양이", "영화"]
            }
       }
   else :
       return_json = {
           "message" : {
                "text" : return_msg
           },
           "keyboard" : {
                "type" : "buttons",
                "buttons" : ["메뉴", "로또", "고양이", "영화"]
            }
       }
   
   return jsonify(return_json)

app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT', 8080)))
