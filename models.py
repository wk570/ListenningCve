import hashlib

from exts import db


class FeedModel(db.Model):
    __tablename__ ="feed_links"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)


class RssLink(db.Model):
    __tablename__ = "links"
    title = db.Column(db.String(1000), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(100))
    md5_hash = db.Column(db.String(32), primary_key=True, unique=True)  # 使用 MD5 哈希作为主键

    Feed_id = db.Column(db.Integer, db.ForeignKey("feed_links.id"))

    def generate_md5_hash(self):
        data_str = self.title + self.link  # 可根据需要拼接其他字段
        md5_hash = hashlib.md5(data_str.encode()).hexdigest()
        return md5_hash


class CveModel(db.Model):
    __tablename__ = "cve"
    id = db.Column(db.String(100), primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)
