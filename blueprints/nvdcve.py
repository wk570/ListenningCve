import json

import requests
from flask import Blueprint, request, render_template
import config

headers = {
    "apiKey": config.api_key
}
pb = Blueprint('nvdcve', __name__, url_prefix='/nvdcve')
url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?"


@pb.route("/", methods=['GET'])
def test():
    return render_template("cve.html")


@pb.route("/commit", methods=['POST'])
def commit():
    data: dict = request.get_json()
    print(data)
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    temp_url = f"{url}pubStartDate={startDate}&pubEndDate={endDate}"
    print(temp_url)
    resp = requests.get(temp_url, headers=headers, verify=False)
    print("****************")
    data = json.loads(resp.text, strict=False)
    cve_list = data.get('vulnerabilities')
    sorted_data = sorted(cve_list, key=compare_cve, reverse=True)
    resp_data = deal_data(sorted_data)
    print(resp_data)
    return resp_data


def deal_data(datas: list):
    new_data = []
    for data in datas:
        id = data.get('cve').get('id')
        published = data.get('cve').get('published')
        lastModified = data.get('cve').get('lastModified')
        references = []
        for reference in data.get('cve').get('references'):
            references.append(reference.get('url'))

        for desc in data.get('cve').get('descriptions'):
            if desc["lang"] == "en":
                descriptions = desc.get('value')
        try:
            if data.get('cve').get('metrics'):
                if data.get('cve').get('metrics').get('cvssMetricV31'):
                    pri = data.get('cve').get('metrics').get('cvssMetricV31')[0]
                    privilegesRequired = pri.get('cvssData').get('privilegesRequired')
                    baseSeverity = pri.get('cvssData').get('baseSeverity')
                elif data.get('cve').get('metrics').get('cvssMetricV30'):
                    pri = data.get('cve').get('metrics').get('cvssMetricV30')[0]
                    privilegesRequired = pri.get('cvssData').get('privilegesRequired')
                    baseSeverity = pri.get('cvssData').get('baseSeverity')
                else:
                    pri = data.get('cve').get('metrics').get('cvssMetricV2')[0]
                    privilegesRequired = pri.get('cvssData').get('privilegesRequired')
                    baseSeverity = pri.get('cvssData').get('baseSeverity')
            else:
                privilegesRequired = "NONE"
                baseSeverity = "NONE"

            descriptions = descriptions.encode('utf-8').decode('raw_unicode_escape').replace(r"\n", '')
            new_data.append(
                {"id": id, "descriptions": descriptions, "published": published, "lastModified": lastModified,
                 "baseSeverity": baseSeverity, "privilegesRequired": privilegesRequired})
        except Exception as e:
            print(e)
            print(id)
            print(data)
    return new_data


def compare_cve(cve: dict):
    try:
        base_severity_priority = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        privileges_required_priority = {"NONE": 1, "LOW": 2, "HIGH": 3}

        base = cve.get("cve").get("metrics").get("cvssMetricV31")
        date = cve.get("cve").get("published")
        if base:
            base_severity = base[0]["cvssData"]["baseSeverity"]
            privileges_required = base[0]["cvssData"]["privilegesRequired"]
            base_severity_priority_value = base_severity_priority.get(base_severity, 0)
            print(base_severity_priority_value)
            privileges_required_priority_value = privileges_required_priority.get(privileges_required, 0)
            return base_severity_priority_value, privileges_required_priority_value, date
        else:
            return 0, 0, date
    except Exception as e:
        print(e)
        print("1")
        return 0, 0, date


if __name__ == '__main__':
    pass
