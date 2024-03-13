from flask import Blueprint,  render_template,  current_app, jsonify

import time
from models import RssLink, FeedModel


bp = Blueprint('article', __name__, url_prefix='/article')

proxies = "http://127.0.0.1:7890"


@bp.route('/get_data', methods=['GET'])
def get_data():
    try:
        current_app.logger.info("Fetching RSS feed data...")
        rss_url_models = FeedModel.query.all()
        datas = []
        for rss_url_model in rss_url_models:
            id = rss_url_model.id
            title = rss_url_model.title
            link_models = RssLink.query.filter_by(Feed_id=id).order_by(RssLink.date.desc()).limit(2).all()
            if link_models:
                entries = []
                for link_model in link_models:
                    entries.append({"title": link_model.title, "link": link_model.link, "date": link_model.date})

                datas.append({"rss_title": rss_url_model.title, "rss_id": id, "entries": entries})
            else:
                current_app.logger.warning(f"No link models found for Feed : {title}")
        print(datas)
        return jsonify(datas)
    except Exception as e:
        current_app.logger.error(f"{e}")
        return jsonify({'error': str(e)})


@bp.route('/')
def article():
    return render_template("article.html")



@bp.route("/detail/<rss_id>")
def rss_detail(rss_id):
    try:
        current_app.logger.info(f"Fetching details for RSS ID: {rss_id}")
        Feed = FeedModel.query.filter_by(id=rss_id)
        feed_title = Feed[0].title
        RssLinks = RssLink.query.filter_by(Feed_id=rss_id).order_by(RssLink.date.desc()).all()
        datas=[]
        for rsslink in RssLinks:
            title = rsslink.title
            link = rsslink.link
            date = rsslink.date
            datas.append({"title": title, "link": link, "date": date})

        return render_template("detail.html", datas=datas, title=feed_title)
    except Exception as e:
        current_app.logger.error(f"An error occurred in rss_detail route: {e}")
        return "1"


if __name__ == '__main__':
    start_time = time.perf_counter()
    current_app.logger.info(f"Execution time: {time.perf_counter() - start_time} seconds")
