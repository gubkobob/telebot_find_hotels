import requests


def request_to_api(url, headers, querystring):
    try:
        response = requests.request(
            "GET", url=url, headers=headers, params=querystring, timeout=10
        )
        if response.status_code == requests.codes.ok:
            return response
    except Exception as exc:
        print(exc)
        return None
