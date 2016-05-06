# coding: utf-8
import urllib
import json
import time
import sys
import web

reload(sys)
sys.setdefaultencoding('utf-8')

movie_ids = []

douban_url = 'http://api.douban.com/v2/movie/top250?start=%d&count=50'
douban_movie_url = 'http://api.douban.com/v2/movie/subject/%s'
db = web.database(dbn='sqlite', db='MovieSite.db')

def add_movie(data):
	print data
	movie = json.loads(data)
	if movie.has_key('title'):
		db.insert('movie',
			id = int(movie['id']),
			title = movie['title'],
			origin = movie['original_title'],
			rating = movie['rating']['average'],
			url = movie['alt'],
			image = movie['images']['large'],
			directors = ','.join([d['name'] for d in movie['directors']]),
			casts = ','.join([d['name'] for d in movie['casts']]),
			year = movie['year'],
			genres = ','.join(movie['genres']),
			countries = ','.join(movie['countries']),
			summary = movie['summary'])
	else:
		print movie['msg']

def get_poster(id, url):
	pic = urllib.urlopen(url).read()
	file_name = 'static/poster/%d.jpg'%id
	f = file(file_name, 'wb')
	f.write(pic)
	f.close()

# # 获取id列表
# for index in range(0, 250, 50):
# 	print index
# 	response = urllib.urlopen(douban_url%index)
# 	data = response.read()
# 	# print data
# 	data_json = json.loads(data)
# 	movie250 = data_json['subjects']

# 	for movie in movie250:
# 		movie_ids.append(movie['id'])
# 		print movie['id'], movie['title']

# 	time.sleep(3)

# print movie_ids

# # 下载列表并存储db
# count = 0 
# for mid in movie_ids:
# 	print count, mid
# 	response = urllib.urlopen(douban_movie_url%mid)
# 	data = response.read()
# 	add_movie(data)
# 	count +=1
# 	time.sleep(3)

if __name__ == '__main__':
	# 获取图片并存储到本地目录

	movies = db.select('movie')
	count = 0

	for m in movies:
		get_poster(m.id, m.image)
		count +=1
		print count, m.title
		time.sleep(3)
