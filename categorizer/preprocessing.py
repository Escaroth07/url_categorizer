import tldextract
from urllib.parse import urlparse, urlunparse, parse_qs

def preprocess_url(url):
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    scheme = parsed.scheme.lower()
    path = parsed.path
    qs = parse_qs(parsed.query)
    qs = {k: v for k, v in qs.items() if not k.startswith('utm_')}
    new_query = '&'.join(f"{k}={v[0]}" for k, v in qs.items())
    return urlunparse((scheme, netloc, path, '', new_query, ''))

def extract_domain_features(url):
    ext = tldextract.extract(url)
    return {
        "tld": ext.suffix,
        "domain": ext.domain,
        "subdomain": ext.subdomain,
    }
