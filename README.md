# Python Web Crawler

The requirements of this project were as listed:

Phase 1
● You should write an application that takes as input a starting URL for your crawl. The application should
then do the following:
1. Fetch the HTML document at that URL
2. Parse out URLs in that HTML document
3. Log/print the URL visited along with all the URLs on the page
4. Loop back to step 1 for each of these new URLs

Phase 2
● In addition to the basic crawler requirements above, your application should fetch URLs in parallel to
speed up the crawl and avoid blocking the whole process on single slow page loads. We encourage you
to make use of any managed thread pool functionality provided by the language you choose to simplify
your implementation.

Phase 3
● You should also include at least one test that can be run against your application to show it works as
expected. Please also document the command to run your test(s) against the application.

# Instructions for running script
Clone the repo onto your local machine.
```
git clone https://github.com/kanupriyaa97/crawler.git
```

Navigate to the root directory.
```
cd crawler
```

Activate your virtualenv for Python.

Install dependencies from requirements.txt
```
pip install -r requirements.txt
```

Run the crawler:
```
python main.py
```

To run the tests:
```
python test.py
```
