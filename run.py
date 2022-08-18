import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from spiders import MaroofMainInfo
from spiders import CheckWebsites
from spiders import GooglePlay
from spiders import TwitterScrape
import pandas as pd

def get_urls(filename, field):
    data = pd.read_csv(filename, usecols=[field])
    data = data[data.values != 'None']
    link_list = data.values.tolist()
    link_list = sum(link_list, [])
    print(link_list)
    return link_list

def connect_files(filenames):
    df2 = pd.read_csv(f'files/{filenames[0]}.csv')
    df2.sort_values(by="Twitter", inplace=True, ascending=False)
    df1 = pd.read_csv(f'files/{filenames[1]}.csv') # find better ver
    df1.sort_values(by="Twitter", inplace=True, ascending=False)
    df = pd.merge_ordered(df1, df2)

    df1 = pd.read_csv(f'files/{filenames[2]}.csv')  # find better ver
    df1.sort_values(by="Website", inplace=True, ascending=False)
    df.sort_values(by="Website", inplace=True, ascending=False)
    df = pd.merge_ordered(df, df1)

    df1 = pd.read_csv(f'files/{filenames[3]}.csv')  # find better ver
    df1.sort_values(by="Android", inplace=True, ascending=False)
    df.sort_values(by="Android", inplace=True, ascending=False)

    df = df.reindex(columns=['Name', 'Activity', 'Rating', 'Ratters','ResComments','CRNumber','Phone','Email','Twitter',
                             'followers_count', 'num_tweets','ret','rep','fav','Insta','Whatsapp','Website','ECommerce',
                             'Android', 'downloads', 'reviews', 'score', 'last_patch', 'IOS', 'Location'])
    df.to_csv('files/final.csv', index=False)

def main():
    process = CrawlerProcess(settings={
        'FEED_URI': 'files/Maroof.csv',
        'FEED_FORMAT': 'csv',
    })
    process.crawl(MaroofMainInfo.MarofMainInfoSpider)
    process.start()
    process2 = CrawlerProcess(settings={
        'FEED_URI': 'files/Website.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_FIELDS': [
            'Website',
            'ECommerce'
            ]
    })
    process2.crawl(CheckWebsites.CheckWebSpider)
    process2.start()

    process3 = CrawlerProcess(settings={
        'FEED_URI': 'files/googleplay.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_FIELDS': [
            'downloads',
            'reviews'
        ]
    })
    process3.crawl(GooglePlay.GooglePlay)
    process3.start()

    twit_obj = TwitterScrape.TwiterScraper(get_urls('files/Maroof.csv', 'Twitter'))
    twit_obj.send_usernames()

    filenames = ['files/Maroof.csv', 'files/twitter.csv', 'files/Website.csv', 'files/googleplay.csv']
    connect_files(filenames)


if __name__ == '__main__':
    main()