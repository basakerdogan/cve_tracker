from flask import Flask,request, render_template, url_for,redirect
import requests,json

app = Flask(__name__)

@app.route('/')
def main_page():
    cve_dict = {}
    page = request.args.get('page', 1, type=int)  # Sayfa numarasını al, varsayılan olarak 1.
    per_page = 20  # Her sayfada görüntülenecek öğe sayısı.
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate=2024-03-01T00:00:00.000-05:00&pubEndDate=2024-04-14T23:59:59.999-05:00"
    req = requests.get(url = api_url)
    data = json.loads(req.text)
    for i in range(len(data["vulnerabilities"])):
        cve_id = data["vulnerabilities"][i]["cve"]["id"]
        cve_desc = data["vulnerabilities"][i]["cve"]["descriptions"][0]["value"]
        cve_metric_check =  data["vulnerabilities"][i]["cve"]["metrics"]
        try:
            cve_base_severity = cve_metric_check["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
        except KeyError:
            cve_base_severity = None

        cve_dict[i] = {"cve_id": cve_id, "cve_desc": cve_desc, "cve_base_severity": cve_base_severity }

    return render_template('main_page.html', cve_dict = cve_dict, cve_len = len(cve_dict), page=page, per_page=per_page , total_pages=20)

@app.route('/cve/<cve_id>',methods=['POST','GET'])
def cve(cve_id):
    cve_id = request.form['cve_id']
    api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    req = requests.get(url = api_url)
    data = json.loads(req.text)
    cve_desc = data["vulnerabilities"][0]["cve"]["descriptions"][0]["value"]
    cve_base_severity = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
    return render_template('detail.html', cve_desc = cve_desc , cve_base_severity = cve_base_severity, cve_id= cve_id)


if __name__ == '__main__':
    app.run(debug=True)

