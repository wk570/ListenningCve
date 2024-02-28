
from flask import Flask, render_template
import config
from exts import db
from flask_migrate import Migrate
from blueprints.article import bp
from blueprints.nvdcve import pb
from blueprints.gitcve import sb

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

app.register_blueprint(bp)
app.register_blueprint(pb)

app.register_blueprint(sb)
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")
 


if __name__ == '__main__':
    app.run(debug=True,  port=80)
# host="0.0.0.0",