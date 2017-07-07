#coding:utf8

#20170705爬取百度百科的python词条页面1000个相关词条的标题和简介
#入口页http://baike.baidu.com/item/Python
#通过浏览器的检查，审查元素，获取URL格式
#词条页面URL：/item/Python
#数据格式：标题：<dd class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTittle-"><h1>...</h1><#/dd>
#		简介：<div class="lemma-summary" label-module="lemmaSummary">...</div>
#页面变吗：UTF-8



import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
	"""docstring for SpiderMain"""
	def __init__(self):
		super(SpiderMain, self).__init__()

		self.urls = url_manager.UrlManager()
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.outputer = html_outputer.HtmlOutputer()

	def craw(self, root_url):
		count = 1
		self.urls.add_new_url(root_url)
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()
				print new_url
				print 'craw %d : %s' % (count, new_url)
				html_cont = self.downloader.download(new_url)
				new_urls, new_data = self.parser.parse(new_url, html_cont)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)

				if count == 3:
					break
				count = count + 1

			
			#error handler
			except:
				print 'craw failed'

		self.outputer.output_html()
			

if __name__ == "__main__":
	root_url = "http://baike.baidu.com/item/Python"
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)
