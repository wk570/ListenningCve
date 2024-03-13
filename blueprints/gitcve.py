import datetime
import re
from lxml import etree
import requests
from flask import Blueprint, render_template,  jsonify, current_app

from exts import db
from models import CveModel
import config
import requests

sb = Blueprint('gitcve', __name__, url_prefix='/git')
cve_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name="
header = {
    'Authorization': f"token {config.GITHUB_TOKEN}",
    'Connection': 'close'
}


@sb.route("/", methods=['GET'])
def index():
    try:
        current_app.logger.info("Rendering gitcve template")
        existing_list = []
        cves = CveModel.query.all()
        for cve in cves:
            current_app.logger.debug(f"Found CVE: {cve.id}")
            current_app.logger.debug(f"URL: {cve.url}")
            current_app.logger.debug(f"Created at: {cve.created_at}")
            existing_list.append({"cve_name": cve.id, "cve_url": cve.url, "created_at": cve.created_at})

        return render_template('gitcve.html', existing_list=existing_list)
    except Exception as e:
        current_app.logger.error(f"An error occurred in index route: {e}")
        return "An error occurred", 500


@sb.route("/update", methods=['GET'])
def update():
    try:
        current_app.logger.info("Updating CVE list from GitHub")
        today_lists = get_today_cve_from_github()
        new_today_list = []
        for item in today_lists:
            users = CveModel.query.filter_by(id=item.get('cve_name')).all()
            if len(users) == 0:
                new_today_list.append(item)
                cve = CveModel(id=item.get('cve_name'), url=item.get('cve_url'), created_at=item.get('created_at'))
                db.session.add(cve)
        db.session.commit()

        current_app.logger.debug(f"Today's CVE list: {today_lists}")
        current_app.logger.debug(f"Newly added CVEs: {new_today_list}")
        return jsonify(new_today_list)

    except requests.RequestException as e:
        current_app.logger.error(f"RequestException occurred in update route: {e}")
        error_message = "An error occurred while fetching data. Please try again later."
        return jsonify({"error": error_message}), 500
    except Exception as e:
        current_app.logger.error(f"An error occurred in update route: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


def get_today_cve_from_github():
    today_cve_list = []
    try:
        year = datetime.datetime.now().year
        api = f"https://api.github.com/search/repositories?q=CVE-{year}&sort=updated"
        session = requests.session()
        resp = session.get(api, headers=header, timeout=10, verify=False)
        current_app.logger.info("Request sent to external API")
        current_app.logger.debug(f"Response status code: {resp.status_code}")
        resp_json = resp.json()
        items = resp_json.get('items', [])
        patten_cve = r'CVE-\d+-\d+'
        patten_date = r'\d{4}-\d{2}-\d{2}'
        today_date = datetime.date.today()

        for item in items[:30]:
            try:
                cve_name = item.get('name', '').upper()
                cve_name = re.findall(patten_cve, cve_name)[0] if re.findall(patten_cve, cve_name) else None
                created_at = item.get('created_at', '')
                created_at = re.findall(patten_date, created_at)[0] if re.findall(patten_date, created_at) else None
                cve_url = item.get('html_url', '')

                if created_at == str(today_date):
                    if exist_cve(cve_name):
                        today_cve_list.append({"cve_name": cve_name, "cve_url": cve_url, "created_at": created_at})
                    else:
                        current_app.logger.warning(f"Invalid CVE: {cve_name}")
                else:
                    current_app.logger.info(f"CVE {cve_name} 不是今天更新的CVE, 更新时间为 {created_at}")

            except Exception as e:
                current_app.logger.error(f"Error processing CVE data: {e}")
                raise

    except Exception as e:
        current_app.logger.error(f"Error fetching data from GitHub API: {e}")
        raise

    return today_cve_list




def exist_cve(cve_name):
    try:
        query_cve_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_name
        response = requests.get(query_cve_url, timeout=10)
        html = etree.HTML(response.text)
        title = html.xpath("/html/head/title/text()")

        if 'ERROR' in title:
            return 0
        else:
            return 1
    except Exception as e:
        current_app.logger.error(f"Error checking existence of CVE {cve_name}: {e}")
        return 0


if __name__ == '__main__':
    pass
