import hashlib
import asyncio
import time
import feedparser
import aiohttp
from flask import Flask, render_template
import config
from exts import db
from flask_migrate import Migrate
from models import FeedModel, RssLink
import logging
from blueprints.article import bp
from blueprints.nvdcve import pb
from blueprints.gitcve import sb

from apscheduler.schedulers.background import BackgroundScheduler
from flask.logging import default_handler

semaphore = asyncio.Semaphore(10)
app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

app.register_blueprint(bp)
app.register_blueprint(pb)

app.register_blueprint(sb)
db.init_app(app)
migrate = Migrate(app, db)

stream_handler = logging.StreamHandler()
handler = logging.FileHandler('flask.log')
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s %(filename)s %(funcName)s %(lineno)d %(message)s",
    datefmt="%Y-%m-%d %X"
)
handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
app.logger.removeHandler(default_handler)
app.logger.addHandler(handler)
app.logger.addHandler(stream_handler)

max_retry_count = 3
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
scheduler = BackgroundScheduler()
scheduler.start()


def job1():
    print("0000000000000")
    try:
        with app.app_context():
            new_list = asyncio.run(main())
            rsslinks = RssLink.query.all()
            for rsslink in rsslinks:
                db.session.delete(rsslink)
            db.session.commit()
            for list in new_list:
                if list is not None:
                    if list.get('entries') is not None:
                        for entry in list.get('entries'):
                            data_str = entry.get('title') + entry.get('link') + entry.get('feed_date')
                            md5_hash = hashlib.md5(data_str.encode()).hexdigest()
                            link = RssLink(title=entry.get('title'), link=entry.get('link'),
                                           Feed_id=list.get('feed_id'),
                                           date=entry.get('feed_date'), md5_hash=md5_hash)
                            db.session.add(link)
                        db.session.commit()
                    else:
                        continue
    except Exception as e:
        print(e)


scheduler.add_job(func=job1, id="job_1", trigger="interval", seconds=6000, replace_existing=False)


@app.route("/")
def index():
    print(1)
    print(2)
    return render_template("index.html")


async def get_text(index: str, url: str, session, retry_count=0):
    start_time = time.perf_counter()
    try:
        app.logger.info(f"Fetching text for URL: {url}")
        async with session.get(url=url) as resp:
            text = await resp.text()
            cost_time = time.perf_counter() - start_time
            app.logger.debug(f"Retrieved text for URL: {url}, 花费时间: {cost_time}, 重试次数: {retry_count}")
            return {"id": str(index), "content": text}
    except asyncio.TimeoutError:
        app.logger.warning(f"Timeout error occurred for URL: {url}")
        # 处理超时错误，重新尝试请求
        if retry_count < max_retry_count:
            app.logger.info(f"Retrying request for URL: {url}")
            return await get_text(index, url, session, retry_count + 1)
        else:
            app.logger.error(f"Exceeded maximum retry count for URL: {url}")
            return
    except Exception as e:
        app.logger.error(f"{e}-{url}")
        return


def deal_content(id, content):
    if content is not None:
        try:
            app.logger.info(f"Processing content for ID: {id}")
            feed = feedparser.parse(content)
            if hasattr(feed, "bozo_exception"):
                app.logger.warning(f"{id}:{feed.get('bozo_exception')}")
                return
            feed_title = feed.get('feed').get('title')

            entries = []
            for entry in feed.entries:  # 只获取前两个条目
                entry_title = entry.get('title')
                entry_link = entry.get('link')
                temp_entry_date = entry.get('published_parsed')
                formatted_date = time.strftime("%Y年%m月%d日", temp_entry_date)
                entries.append({'title': entry_title, 'link': entry_link, 'feed_date': formatted_date})

            app.logger.info(f"success processed content for {feed_title}")
            return {'feed_id': id, 'feed_title': feed_title, 'entries': entries}
        except Exception as e:
            app.logger.error(f"Error processing content for ID {id}: {e}")
    else:
        app.logger.warning("Content is None for ID {id}")


async def main():
    Feeds = FeedModel.query.all()
    test_urls = []
    for feed in Feeds:
        test_urls.append(feed.link)
    conn = aiohttp.TCPConnector(ssl=False)
    timeout = aiohttp.ClientTimeout(total=330, connect=2, sock_connect=10, sock_read=7)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [asyncio.create_task(get_text(str(index), url, session)) for index, url in
                 enumerate(test_urls, start=1)]
        resps = await asyncio.gather(*tasks)
        datas = []
        for resp in resps:
            if resp is not None:
                item = deal_content(resp.get('id'), resp.get('content'))
                datas.append(item)
            else:
                continue
    return datas


if __name__ == '__main__':
    app.run(debug=True, port=80)

# host="0.0.0.0",