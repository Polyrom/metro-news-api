CREATE_NEWS_TABLE = '''
CREATE TABLE IF NOT EXISTS metro_news (
                    id INTEGER PRIMARY KEY,
                    headline TEXT,
                    image_url TEXT,
                    pub_date DATE
                 )
'''

SELECT_NEWS_SINCE_DATE = '''
SELECT * FROM metro_news
WHERE pub_date >= ?
'''

INSERT_NEWS_ITEM = '''
INSERT INTO metro_news (headline, image_url, pub_date)
VALUES (?, ?, ?)
'''
