import scrapy

from scrapy.loader import ItemLoader
from ..items import LovcenbankaItem
from itemloaders.processors import TakeFirst


class LovcenbankaSpider(scrapy.Spider):
	name = 'lovcenbanka'
	start_urls = ['https://lovcenbanka.me/me/novosti']

	def parse(self, response):
		post_links = response.xpath('//h2[@class="ba-blog-post-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="ba-blog-posts-pagination"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="blog-content-wrapper"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="intro-post-date"]/text()').get()

		item = ItemLoader(item=LovcenbankaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
