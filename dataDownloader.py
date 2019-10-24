# imports
import requests
import time
import sys
from newspaper import Article, ArticleException

print('running downloader...')

# api key
api_key = 'A6vW3SGfzFTfLTAYG43inWPchbnQIKdm'

# meta data initialize
meta_file = open('meta.data', 'w+')
file_id = 0

# url to grab all articles from January 2019 (2019/1)
# iterate over all possible dates (1851-2019) (1-12)
# 1851 changed to 1852 to fix requests error
for year in range(2019, 1919, -1):
    for month in range(1, 13, 1):
        month_count = 0
        # req_url
        req_url = 'https://api.nytimes.com/svc/archive/v1/' + str(year) + '/' + str(month) + '.json?api-key=' + api_key

        # may have to add time.sleep() # sleep to avoid 429 errors
        # requests returns a json object
        req = requests.get(req_url).json()
        time.sleep(1)

        # catch 'response not found' - not sure what causes this yet
        try :
            # req['response']['docs'] is a list of dictionaries
            # iterate over all docs
            # we need to grab the doc date and text
            for doc in req['response']['docs']:

                article_url = doc['web_url']
                passed = False
                try :
                    article = Article(article_url)
                    article.download()
                    article.parse()
                    passed = True
                except ArticleException :
                    pass

                # BUG: the same article is being printed every time?
                locked_text = 'TimesMachine is an exclusive benefit for home delivery and digital subscribers.'
                if locked_text not in article.text[:100] and passed :  # article is textual
                    # file name is unique ID only
                    filename = str(file_id) + '.data'

                    # write article text to file
                    f = open(filename, 'w+')
                    try:
                        f.write(article.text)
                    except UnicodeEncodeError:
                        # we'll just skip over unicode errors for now
                        pass
                    f.close()

                    # write meta data
                    # we could use the API to add other features to data in the future
                    # this would require a rerun of the downloader
                    meta_data = (str(file_id) + ', '  # id
                                 + str(year) + ', '  # year
                                 + str(month) + ', ' # date
                                 + doc['news_desk'].replace(' ', '').replace('/', '') + '\n' ) # category
                    meta_file.write(meta_data)

                    file_id += 1  # increment file id

            # only grab 500 articles from each month to cut down on time for now
            month_count += 1
            if month_count > 500 :
                break

        except KeyError :
            pass
            #print('response not found.')
    print('done with year ', year)

meta_file.close()
