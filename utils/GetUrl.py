from urllib.parse import urlparse, parse_qs


def get_url_data(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    return query_params