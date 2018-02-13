import scrapy

class RoadSpider(scrapy.Spider):
    name = 'road_spider'
    start_urls = [
        'http://autostrada.info/ru/reviews/page/1/',
    ]

    def parse(self, response):
        for review in response.css('div.col-md-12.reviewBlock'):
            tmp = review.css('p.comment.break-word::text').extract_first()
            tmp1 = review.css('a.label.label-code::text').extract_first()
            tmp2 = review.css('a.highwayLabel::text').extract_first()

            tmp = tmp.replace('\r\n', ' ')
            tmp = tmp.replace('\n', '')
            dd = {
                'title': tmp1 + ' ' + tmp2,
                'subtitle': review.css('div.col-sm-8.b-rate.hidden-xs b::text').extract_first(),
                'date': review.css('strong.reviewDate::text').extract_first(),
                'rate': review.css('span.b-stars::attr(title)').extract_first(),
                'description': tmp,
            }
            try:
                dd['date'] = dd['date'].replace('\t', '')
                dd['date'] = dd['date'].replace('\n', '')
                dd['date'] = dd['date'].replace('\u0433.', '')
            except:
                pass

            yield dd

        next_page = response.css('li.next a::attr(href)').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)