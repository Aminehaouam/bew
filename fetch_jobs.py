"""Run LOCALLY (own internet connection): fetch details for the candidates.

    pip install requests
    python fetch_jobs.py candidates.json jobs_raw

Reads candidates.json (refnr list), calls the documented Jobsuche API
(X-API-Key: jobboerse-jobsuche) for each job's details, saves the raw JSON to
jobs_raw/<refnr>.json and writes jobs_raw/_summary.json with every e-mail
address found in the ad text. It does not touch the website's security
question. Upload the jobs_raw folder (zipped) afterwards.

Optional: python fetch_jobs.py --search jobs_raw   # also pages through the search
for the three search terms and writes jobs_raw/_search_<term>.json.
"""
import base64, json, os, re, sys, time
import requests

BASE = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
HEAD = {"X-API-Key": "jobboerse-jobsuche"}
MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TERMS = ["Elektroniker Betriebstechnik", "Elektroniker für Betriebstechnik", "Industrieelektriker"]


def get(url, **params):
    r = requests.get(url, headers=HEAD, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def search_all(term, out):
    page, items = 1, []
    while True:
        data = get(f"{BASE}/pc/v4/app/jobs", angebotsart=4, was=term, page=page, size=50)
        batch = data.get("stellenangebote", [])
        if not batch:
            break
        items += batch
        page += 1
        time.sleep(1)
    json.dump(items, open(os.path.join(out, f"_search_{term}.json"), "w"), ensure_ascii=False, indent=1)
    print(term, len(items), "Treffer")


def main():
    args = sys.argv[1:]
    do_search = "--search" in args
    args = [a for a in args if a != "--search"]
    if do_search:
        out = args[0]
        os.makedirs(out, exist_ok=True)
        for t in TERMS:
            search_all(t, out)
        return
    cand, out = json.load(open(args[0])), args[1]
    os.makedirs(out, exist_ok=True)
    summary = []
    for c in cand:
        code = base64.b64encode(c["refnr"].encode()).decode()
        try:
            d = get(f"{BASE}/pc/v4/jobdetails/{code}")
        except Exception as e:  # keep going, report at the end
            summary.append({"refnr": c["refnr"], "firma": c["firma"], "fehler": str(e)})
            print("FEHLER", c["firma"], e)
            continue
        json.dump(d, open(os.path.join(out, c["refnr"] + ".json"), "w"), ensure_ascii=False, indent=1)
        mails = sorted(set(MAIL.findall(json.dumps(d, ensure_ascii=False))))
        summary.append({"refnr": c["refnr"], "firma": c["firma"], "emails": mails})
        print(c["firma"], mails)
        time.sleep(1)
    json.dump(summary, open(os.path.join(out, "_summary.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
