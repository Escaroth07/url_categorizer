from urllib.parse import urlparse
import requests
import csv
from io import StringIO

def match_blacklist(url, domain_blacklists):
    netloc = urlparse(url).netloc
    domain_parts = netloc.split('.')
    for category, domains in domain_blacklists.items():
        # Check full netloc and all its parent domains
        for i in range(len(domain_parts)-1):
            candidate = '.'.join(domain_parts[i:])
            if candidate in domains:
                return category
    return None

def load_steven_black_blacklists():
    url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
    resp = requests.get(url)
    lines = resp.text.splitlines()
    domains = set()
    for line in lines:
        if line.startswith("0.0.0.0"):
            parts = line.split()
            if len(parts) >= 2:
                domain = parts[1]
                if domain.startswith("www."):
                    domain = domain[4:]
                domains.add(domain)
    return {"ads": domains}

def load_urlhaus_blacklist():
    url = "https://urlhaus.abuse.ch/downloads/csv/"
    resp = requests.get(url)
    raw = "\n".join([line for line in resp.text.splitlines() if not line.startswith('#')])
    f = StringIO(raw)
    reader = csv.DictReader(f)
    domains = set()
    for row in reader:
        try:
            url_value = row["url"]
            host = url_value.split('/')[2] if "://" in url_value else url_value
            host = host.split(":")[0]
            if host.startswith("www."):
                host = host[4:]
            domains.add(host)
        except Exception:
            continue
    return {"malware": domains}
