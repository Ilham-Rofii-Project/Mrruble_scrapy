import scrapy


class Result7Spider(scrapy.Spider):
    name = 'result'
    allowed_domains = ['www.mrrubble.co.uk']
    start_urls = ['https://www.mrrubble.co.uk/blog/']

    def parse(self, response):
        # fixed_html = str(BeautifulSoup(response.body, "html5lib"))
        # resp= Selector(text=fixed_html)

        for i in response.xpath("//h3[@class='post_title']/a"):
            title = i.xpath(".//text()").get()
            # title = title[5:]
            # title = title[:-3]
            link = i.xpath(".//@href").get()
            # yield {'title':title,
            #        'link':link}

            yield response.follow(url=link, callback=self.parse_article, meta={'title': title,
                                                                               'link': link})

        next_page = 'https://www.mrrubble.co.uk/blog/page/2/'
        for i in range(2,6):
            next_page=next_page[:-2]+str(i)+'/'
            yield (scrapy.Request(url=next_page, callback=self.parse))

    def parse_article(self, response):
        title = response.request.meta['title']
        link = response.request.meta['link']
        date = response.xpath("//div[@class='singledate col span_1_of_2']/text()").get()
        date=date.strip()
        image = response.xpath("//div[@class='pic']/a/img/@src").get()

        text = ''
        text += title + '\n'

        url = response.xpath("//p/a/strong/span/text()")
        text_link = []
        for i in url:
            text_link += [i.get()]
        # text_link = ['nchvanjsafhsndfuasjnfmashfnsadfunsa']
        url = response.xpath("//div[@class='post_description']/descendant::node()/text()")
        for i in url:
            exists = False
            for j in text_link:
                if i.get().strip() == j.strip():
                    exists = True
            if exists == True:
                text = text[:-1]
                text += ' ' + i.get() + ' '
            else:
                text += i.get().strip() + '\n'
        text2 = ''
        for i in text.split('\n'):
            if i != '':
                text2 += i + '\n'
        yield {'title': title,
               'date': date,
               'link': link,
               'text': text2,
               'image': image}
