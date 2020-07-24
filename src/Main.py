from twitterscraper.query import query_user_info
from twitterscraper.query import query_tweets_from_user
from twitterscraper.tweet import Tweet
from twitterscraper.ts_logger import logger
from twitterscraper.user import User
import pandas as pd
from multiprocessing import Pool
import time
from IPython.display import display
import os
import requests

# todo : 外部化
target_account_id = 'avogado6'
page_limit = 500;

#フォルダが無い場合、作成を行う
def try_make_dir():
    if os.path.exists(target_account_id) == False :
        os.makedirs(target_account_id)

#保存先パスを生成
def make_save_path( file_name : str ) : 
    return target_account_id +'/'+ file_name

#ツイート取得  
def get_tweet( ):
    tweet_list = query_tweets_from_user( target_account_id , page_limit )
    for tweet in tweet_list:
        analysis_tweet(tweet)

# ツイート解析
def analysis_tweet( tweet : Tweet ):
    for url in tweet.img_urls :
        get_image_by_url(url)

# URL取得
def get_image_by_url( url : str ):
    response = requests.get(url)
    image = response.content
    str_arr = url.split('/')
    file_name = str_arr[len(str_arr)- 1];
    save_image( image , file_name )

# 指定のファイルネームで保存
def save_image( image : bytes , file_name : str ):
    save_path = make_save_path(file_name)
    if os.path.exists( save_path ) :
        print("exists file : " + save_path ); #既に存在する
        return ;

    with open(save_path, "wb") as io:
        io.write(image)
        print("save file : " + save_path ); 
        
# 開始
def main():
    try_make_dir() #フォルダ作成
    get_tweet()
    #test()

if __name__ == '__main__':
    main()