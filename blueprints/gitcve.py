import datetime
import re
from lxml import etree
import requests
from flask import Blueprint, render_template,  jsonify

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
    existing_list = []
    cves = CveModel.query.all()
    for cve in cves:
        print(cve.id)
        print(cve.url)
        print(cve.created_at)
        existing_list.append({"cve_name": cve.id, "cve_url": cve.url, "created_at": cve.created_at})

    return render_template('gitcve.html', existing_list=existing_list)


@sb.route("/update", methods=['GET'])
def update():
    today_lists = get_today_cve_from_github()
    new_today_list = []
    for item in today_lists:
        users = CveModel.query.filter_by(id=item.get('cve_name')).all()
        if len(users) == 0:
            new_today_list.append(item)
            cve = CveModel(id=item.get('cve_name'), url=item.get('cve_url'), created_at=item.get('created_at'))
            db.session.add(cve)
    db.session.commit()

    print(today_lists)
    print(new_today_list)
    return jsonify(new_today_list)
    # if exist_cve("CVE-2024-21413"):
    #     print(2)


def get_today_cve_from_github():
    today_cve_list = []
    try:
        year = datetime.datetime.now().year
        print(year)
        api = f"https://api.github.com/search/repositories?q=CVE-{year}&sort=updated"
        session = requests.session()
        try:
            resp = session.get(api, headers=header, timeout=10, verify=False)
        except:
            resp = session.get(api, headers=header, timeout=10, verify=False)
        resp_json = resp.json()
        # print(resp_json)
        items = resp_json['items']
        # print(len(items))
        patten_cve = r'CVE-\d+-\d+'
        patten_date = r'\d{4}-\d{2}-\d{2}'
        today_date = datetime.date.today()
        # datetime.timedelta(-1)
        print(len(items))
        for i in range(30):
            try:
                cve_name = items[i].get('name').upper()
                cve_name = re.findall(patten_cve, cve_name)[0]  # CVE全称呼
                print(cve_name)
                created_at = items[i].get('created_at')
                created_at = re.findall(patten_date, created_at)[0]  # 日期
                print(created_at)
                cve_url = items[i].get('html_url')
                print(cve_url)
                if created_at == str(today_date):
                    if exist_cve(cve_name):
                        print(f"{cve_name}存在")
                        today_cve_list.append({"cve_name": cve_name, "cve_url": cve_url, "created_at": created_at})
                    else:
                        print(f"无效{cve_name}")
                else:
                    print("[-] 该{}的更新时间为{}, 不属于今天的CVE".format(cve_name, created_at))

            except Exception as e:
                print(2)
                print(e)
    except Exception as e:
        print(e)

    return today_cve_list


def exist_cve(cve_name):
    try:
        query_cve_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_name
        response = requests.get(query_cve_url, timeout=10)
        print(f"{cve_name}查询")
        html = etree.HTML(response.text)
        title = html.xpath("/html/head/title/text()")
        print(title)
        if 'ERROR' in title:
            return 0
        else:
            return 1
    except Exception as e:
        return 0



if __name__ == '__main__':
    pass
