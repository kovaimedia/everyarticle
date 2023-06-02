class PIBPipeline:
    def process_item(self, item, spider):
        articles = item['articles']
        print("Scraped Articles:", articles)
        # Process the scraped articles as needed
        return item