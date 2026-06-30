import scrapy


BASE_URL = "https://docs.python.org/3/"


class DocsSpider(scrapy.Spider):
    name = "docs"
    start_urls = [BASE_URL]
    MAX_PAGES = 50

    def __init__(self):
        super().__init__()
        self.visited = set()
        self.page_count = 0

    def parse(self, response):
        if response.url in self.visited:
            return

        self.visited.add(response.url)
        self.page_count += 1
        print("Page Count:", self.page_count)



        paragraphs = []
        for p in response.xpath("//p | //li | //dd"):
            text = " ".join( t.strip()
                for t in p.xpath(".//text()").getall()
                if t.strip()
            )

            text = " ".join(text.split())
            if text:
                paragraphs.append(text)



        headings = []
        for h in response.xpath("//h1 | //h2 | //h3"):
            text = " ".join(
                t.strip()
                for t in h.xpath(".//text()").getall()
                if t.strip()
            )

            text = " ".join(text.split())
            if text:
                headings.append(text)



        yield {
            "title": response.xpath("//title/text()").get(default="").strip(),
            "url": response.url,
            "paragraphs": paragraphs,
            "headings": headings,
            "links": response.xpath("//a/@href").getall()
        }

        if self.page_count >= self.MAX_PAGES:
            return

        for href in response.xpath("//a/@href").getall():
            if self.page_count >= self.MAX_PAGES:
                break
            url = response.urljoin(href).split("#")[0]
            if (
                url.startswith(BASE_URL)
                and url not in self.visited
                and "#" not in url
            ):

                yield scrapy.Request(url,callback=self.parse)