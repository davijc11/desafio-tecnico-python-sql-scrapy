import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        for book in response.css('article.product_pod'):
            detail_url = book.css('h3 a::attr(href)').get()
            detail_url = response.urljoin(detail_url)
            
            titulo_completo = book.css('h3 a::attr(title)').get()
            
            yield response.follow(
                detail_url, 
                self.parse_book, 
                meta={'titulo': titulo_completo}
            )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        titulo = response.meta.get('titulo')
        
        if not titulo:
            titulo = response.css('h1::text').get()

        img_url = response.css('.item.active img::attr(src)').get()
        img_url = response.urljoin(img_url)

        yield {
            'titulo': titulo,
            'preco': response.css('p.price_color::text').get(),
            'estoque': response.xpath('normalize-space(//p[@class="instock availability"])').get(),
            'descricao': response.css('#product_description ~ p::text').get(),
            'imagem_url': img_url,
        }