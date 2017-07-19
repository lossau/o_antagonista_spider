import json
import datetime
import scrapy


class OAntagonistaSpider(scrapy.Spider):
    name = 'o_antagonista'
    base_url = 'http://www.oantagonista.com/pagina/%s'
    current_page = 1
    last_page = 5
    start_urls = [base_url % current_page]
    download_delay = 1.5
    posts = []

    def parse(self, response):

        for post in response.css('article.post'):

            try:
                post_date = datetime.datetime.strptime(
                    post.css('time ::text').extract_first(), '%d.%m.%y').strftime('%d/%m/%y')
            except:
                post_date = ''

            try:
                post_time = post.css('span ::text')[4].extract().strip()
            except:
                post_time = ''

            self.posts.append({
                'id': post.css('article.post ::attr(id)').extract_first(),
                'title': post.css('a ::text').extract_first(),
                'summary': post.css('p ::text').extract_first(),
                'time': post_time,
                'date': post_date,
                'page': self.current_page})

        with open('posts.json', 'w+') as f:
            try:
                existing_posts = json.loads(f.read())
            except:
                existing_posts = []
            f.write(json.dumps(existing_posts + self.posts))

        if self.current_page < self.last_page:
            self.current_page = self.current_page + 1
            yield scrapy.Request(self.base_url % self.current_page)
