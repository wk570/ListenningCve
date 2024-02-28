from flask import Blueprint, request, render_template
from exts import db
import asyncio
import time
from models import RssLink, FeedModel
import feedparser
import aiohttp
from config import test_urls 

bp = Blueprint('article', __name__, url_prefix='/article')

max_retry_count = 3



@bp.route('/')
def article():
    rss_url_models = FeedModel.query.all()
    datas = []
    for rss_url_model in rss_url_models:
        id = rss_url_model.id
        link_models = RssLink.query.filter_by(Feed_id=id).all()
        if link_models:
            entries = []
            for link_model in link_models:
                entries.append({"title": link_model.title, "link": link_model.link, "date": link_model.date})

            datas.append({"rss_title": rss_url_model.title, "rss_id": id, "entries": entries})
        else:
            print(1)

    return render_template("article.html", datas=datas)


async def get_text(index: str, url: str, session, retry_count=0):
    start_time = time.perf_counter()
    try:
        async with session.get(url=url) as resp:
            text = await resp.text()
            cost_time = time.perf_counter() - start_time
            print(f"{url}花费的时间为{cost_time}-重试次数{retry_count}")
            return {"id": str(index), "content": text}
    except asyncio.TimeoutError:
        # 处理超时错误，重新尝试请求
        if retry_count < max_retry_count:
            return await get_text(index, url, session, retry_count + 1)
        else:
            print(f"Exceeded maximum retry count for URL: {url}")
            return
    except Exception as e:
        print(f"{e}-{url}")
        return


def deal_content(id, content):
    if content is not None:
        try:
            feed = feedparser.parse(content)
            if hasattr(feed, "bozo_exception"):
                print(id)
                return
            feed_title = feed.get('feed').get('title')
            entries = []
            for entry in feed.entries[:2]:  # 只获取前两个条目
                entry_title = entry.get('title')
                entry_link = entry.get('link')
                temp_entry_date = entry.get('published_parsed')
                formatted_date = time.strftime("%Y年%m月%d日", temp_entry_date)
                entries.append({'title': entry_title, 'link': entry_link, 'feed_date': formatted_date})
            return {'feed_id': id, 'feed_title': feed_title, 'entries': entries}
        except Exception as e:
            print(e)
    else:
        pass


async def main():
    conn = aiohttp.TCPConnector(verify_ssl=False)
    timeout = aiohttp.ClientTimeout(total=330, connect=2, sock_connect=10, sock_read=7)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [asyncio.create_task(get_text(str(index), url, session)) for index, url in
                 enumerate(test_urls, start=1)]
        resps = await asyncio.gather(*tasks)
        datas = []
        for resp in resps:
            if resp is not None:
                datas.append(deal_content(resp.get('id'), resp.get('content')))
            else:
                continue
    return datas



@bp.route("/refresh", methods=["POST", ])
def test():
    lists = asyncio.run(main())
    print(lists)
    rsslinks = RssLink.query.all()
    for rsslink in rsslinks:
        db.session.delete(rsslink)
    db.session.commit()
    for list in lists:
        if list is not None:
            for entry in list.get('entries'):
                link = RssLink(title=entry.get('title'), link=entry.get('link'), Feed_id=list.get('feed_id'),
                               date=entry.get('feed_date'))
                db.session.add(link)
            db.session.commit()
    return '', 204


@bp.route("/refresh/detail/<rss_id>")
def rss_detail(rss_id):
    Feed = FeedModel.query.get(rss_id)
    feed_title = Feed.title
    print(feed_title)
    link = Feed.link
    feed = feedparser.parse(link)
    datas = []
    for entry in feed.entries:
        title = entry.get('title')
        link = entry.get('link')
        temp_entry_date = entry.get('published_parsed')
        formatted_date = time.strftime("%Y年%m月%d日", temp_entry_date)
        datas.append({"title": title, "link": link, "date": formatted_date})

    return render_template("detail.html", datas=datas, title=feed_title)


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(time.perf_counter() - start_time)
