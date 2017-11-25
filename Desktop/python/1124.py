import re
import requests
import codecs
import time
import random
import io
from bs4 import BeautifulSoup

absolute = 'https://movie.douban.com/subject/27103757/comments'
absolute_url = 'https://movie.douban.com/subject/27103757/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
url = 'http://m.douban.com/movie/subject/27103757/comments?start={}&amp;limit=20&amp;sort=new_score&amp;status=P&amp;'
header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', 'Connection': 'keep-alive'}

def get_data(html):
    soup=BeautifulSoup(html,'lxml')
    comment_list = soup.select('.comment > p')#class
    #print comment_list
    #print soup.select('#paginator > a')
    if(len(soup.select('#paginator > a'))<2):
        next_page= soup.select('#paginator > a')[0].get('href')#id
    else:
        next_page = soup.select('#paginator > a')[2].get('href')#id
    
    date_nodes = soup.select('..comment-time')#span class
    #print date_nodes
    return comment_list,next_page,date_nodes

if __name__ == '__main__':
    f_cookies = open('cookies.txt', 'r')
    cookies = {}
    for line in f_cookies.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    html = requests.get(absolute_url, cookies=cookies, headers=header).content
    comment_list = []
    # get comments
    comment_list, next_page,date_nodes= get_data(html,)
    soup = BeautifulSoup(html, 'lxml')
    comment_list = []
    i = 1
    while (next_page != []):  #check the 'next' button
        with io.open("comments.txt", 'a', encoding='utf-8') as f:
            for node in zip(comment_list, date_nodes):
                comment = node[0].get_text().strip().replace("\n", "")
                date = node[1].get_text().strip()
                f.writelines(comment+' '+ date + '\n')
                print 'ok'

        print(absolute + next_page)
        html = requests.get(absolute + next_page, cookies=cookies, headers=header).content
        soup = BeautifulSoup(html, 'lxml')
        comment_list, next_page,date_nodes = get_data(html)

        time.sleep(1 + float(random.randint(1, 100)) / 20)