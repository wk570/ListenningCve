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

    current_app.logger.info("Rendering CVE template")
    return render_template("cve.html")


@pb.route("/commit", methods=['POST'])
def commit():
    try:
        current_app.logger.info("Received POST request to commit data")
        data: dict = request.get_json()
        current_app.logger.debug(f"Received data: {data}")
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        temp_url = f"{url}pubStartDate={startDate}&pubEndDate={endDate}"
        current_app.logger.debug(f"Constructed URL: {temp_url}")
        resp = requests.get(temp_url, headers=headers, verify=False)
        current_app.logger.info("Request sent to external API")
        current_app.logger.debug(f"Response status code: {resp.status_code}")
        data = json.loads(resp.text, strict=False)
        cve_list = data.get('vulnerabilities')
        sorted_data = sorted(cve_list, key=compare_cve, reverse=True)
        resp_data = deal_data(sorted_data)
        current_app.logger.info("Data processed successfully")
        return resp_data

    except requests.RequestException as e:
        current_app.logger.error(f"RequestException occurred in commit route: {e}")
        error_message = "An error occurred while fetching data. Please try again later."
        return jsonify({"error": error_message}), 500
    except Exception as e:
        current_app.logger.error(f"An error occurred in commit route: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


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
            current_app.logger.error(f"Error processing data: {e}")
            current_app.logger.debug(f"Data causing the error: {data}")
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
            privileges_required_priority_value = privileges_required_priority.get(privileges_required, 0)
            return base_severity_priority_value, privileges_required_priority_value, date
        else:
            return 0, 0, date
    except Exception as e:
        current_app.logger.error(f"an error happened in compare: {e}")
        return 0, 0, date



if __name__ == '__main__':
    pass
