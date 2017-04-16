import newspaper
import datetime


class NewsScraper:

    def __init__(self):
        self._news_sites = [
            'http://www.cnn.com',
            'http://www.foxnews.com',
            'http://www.cbs.com',
            'http://www.bbc.com/news',
            'http://www.bbc.co.uk',
            'http://www.time.com',
            'http://www.cnbc.com',
            'http://www.pcmag.com',
            'http://theatlantic.com',
            'http://www.vice.com',
            'http://www.npr.org']

        self._categories = {
            'americas': True,
            'asia': True,
            'default': True,
            'entertainment': True,
            'europe': True,
            'health':True,
            'middle-east': True,
            'politics': True,
            'science': True,
            'tech': True,
            'travel': True,
            'trending': True,
            'us': True,
            'world': True
        }

        self._curr_article_index = 0
        self._curr_article_index_max = 0
        self._curr_site_index = -1
        self._curr_paper = None
        self._curr_paper_name = ''

        self._site_index_max = len(self._news_sites)

        self._article_urls = []

        self._eodb = False

        self._next_paper()

    @staticmethod
    def hot():
        return newspaper.hot()

    @staticmethod
    def popular_urls():
        return newspaper.popular_urls()

    @staticmethod
    def fetch_paper(url):
        return newspaper.build(url, memorize_articles=False, fetch_images=False, language='en')

    def end(self):
        return self._eodb

    def paper_name(self):
        if self.end():
            return ''
        return self._curr_paper_name

    def num_paper_articles(self):
        if self.end() or self._curr_paper is None:
            return -1
        return self._curr_paper.size()

    def next_article(self):
        if self.end():
            return ''

        while self._curr_article_index >= self._curr_article_index_max:
            self._curr_site_index += 1
            if self._curr_site_index == self._site_index_max:
                self._eodb = True
                return ''
            self._next_paper()
            if self.end():
                return ''

        a = self._curr_paper.articles[self._curr_article_index]
        self._curr_article_index += 1
        a.download()
        try:
            a.parse()
            buffer = '{0};{1}\n{2}\n{3}'.format(self.paper_name(), datetime.date.today(), a.title.lower(), a.text)
        except newspaper.ArticleException or FileNotFoundError:
            return ''
        return buffer

    def _next_paper(self):
        if self._curr_paper is not None:
            del self._curr_paper
        self._curr_site_index += 1
        if self._curr_site_index == self._site_index_max:
            self._eodb = True
            return
        self._curr_paper = self.fetch_paper(self._news_sites[self._curr_site_index])
        self._curr_paper_name = self._curr_paper.brand
        self._curr_article_index_max = self._curr_paper.size()
        self._curr_article_index = 0

if __name__ == '__main__':
    scrapper = NewsScraper()
    scrapper.next_article()
    while not scrapper.end():
        print('paper -> {0} : {1}'.format(scrapper.paper_name(), scrapper.num_paper_articles()))
        scrapper._next_paper()

