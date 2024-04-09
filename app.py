from flask import Flask, render_template
import requests,json

app = Flask(__name__)

@app.route('/')
def main_page():
    cve_dict = {}
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?resultsPerPage=10&startIndex=0"
    req = requests.get(url = api_url)
    data = json.loads(req.text)
    for i in range(len(data["vulnerabilities"])):
        cve_id = data["vulnerabilities"][i]["cve"]["id"]
        cve_desc = data["vulnerabilities"][i]["cve"]["descriptions"][0]["value"]
        cve_base_severity = data["vulnerabilities"][i]["cve"]["metrics"]["cvssMetricV2"][0]["baseSeverity"]
        cve_dict[i] = {"cve_id": cve_id, "cve_desc": cve_desc, "cve_base_severity": cve_base_severity }

    return render_template('main_page.html', cve_dict = cve_dict, cve_len = len(cve_dict))


if __name__ == '__main__':

	app.run()
