from exts import db


class FeedModel(db.Model):
    __tablename__ ="feed_links"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)


class RssLink(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(100))

    Feed_id = db.Column(db.Integer, db.ForeignKey("feed_links.id"))


class CveModel(db.Model):
    __tablename__ = "cve"
    id = db.Column(db.String(100), primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)