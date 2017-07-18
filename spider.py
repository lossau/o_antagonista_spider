import json
import scrapy


class OAntagonistaSpider(scrapy.Spider):
    name = 'o_antagonista'
    quotes_base_url = 'http://www.oantagonista.com/pagina/%s'
    current_page = 1
    last_page = 10
    start_urls = [quotes_base_url % current_page]
    download_delay = 1.5
    blog_posts = []

    def parse(self, response):

        for post in response.css('article.post'):
            self.blog_posts.append({
                'id': post.css('article.post ::attr(id)').extract_first(),
                'title': post.css('a ::text').extract_first(),
                'summary': post.css('p ::text').extract_first(),
                'time': post.css('span ::text')[4].extract().strip(),
                'date': post.css('time ::text').extract_first(),
                'page': self.current_page})

        with open('posts.json', 'w+') as f:
            try:
                existing_posts = json.loads(f.read())
            except:
                existing_posts = []
            f.write(json.dumps(existing_posts + self.blog_posts))

        if self.current_page < self.last_page:
            self.current_page = self.current_page + 1
            yield scrapy.Request(self.quotes_base_url % self.current_page)
