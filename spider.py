import json
import datetime
import scrapy


class OAntagonistaSpider(scrapy.Spider):

    name = 'o_antagonista'
    base_url = 'http://www.oantagonista.com/pagina/%s'
    current_page = 1
    last_page = 1
    start_urls = [base_url % current_page]
    download_delay = 0.5
    posts = []

    def parse(self, response):

        for post in response.css('article.post'):

            post_id = post.css('article.post ::attr(id)').extract_first()
            post_summary = post.css('p ::text').extract_first()
            post_title = post.css('h2 ::text').extract_first()

            post_date_time = post.css('time.entry-date ::text').extract_first()
            try:
                post_date = datetime.datetime.strptime(
                    post_date_time, '%d.%m.%y %H:%M').strftime('%d/%m/%y')
            except:
                post_date = ''

            try:
                post_time = datetime.datetime.strptime(
                    post_date_time, '%d.%m.%y %H:%M').strftime('%H:%M')
            except:
                post_time = ''

            self.posts.append({
                'id': post_id or '',
                'title': post_title or '',
                'summary': post_summary or '',
                'time': post_time,
                'date': post_date,
                'page': str(self.current_page)
            })

        with open('posts.json', 'r+') as f:
            try:
                posts_file = f.read()
                f.seek(0)
                f.truncate(0)
                existing_posts = json.loads(posts_file)
            except Exception as e:
                existing_posts = []
            write_posts = existing_posts + self.posts
            f.write(json.dumps(write_posts, ensure_ascii=False).encode('utf8'))

        if self.current_page < self.last_page:
            self.current_page = self.current_page + 1
            yield scrapy.Request(self.base_url % self.current_page)
