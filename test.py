import unittest
from unittest.mock import patch, Mock
from main import Crawler


class MyTest(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(['rescale.com'], 'https://www.rescale.com')

    def testClean(self):
        # given
        paths = ['https://www.rescale.com/?kanu=engineer&sky=blue',
                 'https://www.google.com',
                 'http://sunsetjeans.com',
                ]

        # when
        results = self.crawler.clean(paths)

        # then
        self.assertEqual(1, len(results))
        self.assertEqual(results, ['https://www.rescale.com/'])

    @patch.object(Crawler, "download_url")
    def testCrawler(self, mock_download):
        # given
        mock_download.return_value = '''
        <!DOCTYPE html>
        <html>
        <body>
            <a id="top-nav-products" class="nav-top-level-link " href="/products/platform/"> Products </a>
            <a class="cta ba b--light-gray bg-white w-100 flex flex-column" href="https://www.rescale.com/safecdp/"></a>
            <a href="https://twitter.com/rescaleinc" class="dib mh1 o-80 glow" target="_blank"></a>
        </body>
        </html>
        '''

        # when
        self.crawler.get_urls(self.crawler.queue.get())

        # then
        self.assertEqual(self.crawler.queue.get(), 'https://www.rescale.com/products/platform/')
        self.assertEqual(self.crawler.queue.get(), 'https://www.rescale.com/safecdp/')
        self.assertTrue(self.crawler.queue.empty())


if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()
