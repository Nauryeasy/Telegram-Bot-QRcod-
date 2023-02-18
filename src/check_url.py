import requests
import socket
import ssl


def is_redirect(link):
    response = requests.head(link, allow_redirects=False)
    return response.status_code in (301, 302)


def has_suspicious_js(link):
    response = requests.get(link)
    js_code = response.text
    return "eval(" in js_code or "document.location.replace(" in js_code


def is_solution(link):
    response = requests.get(link)
    content_type = response.headers['content-type']
    return 'application/octet-stream' in content_type or '.exe' in link or '.dll' in link


def is_https(link):
    return link.startswith('https://')


def has_ssl_cert(link):
    url = requests.head(link).url
    domain = url.split('//')[1].split('/')[0]
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssl_sock:
            cert = ssl_sock.getpeercert()
            return bool(cert)


def is_suspicious(link):
    return any(site in link for site in ['google', 'facebook', 'amazon', 'twitter', 'linkedin', 'youtube'])


def is_long_level(link):
    return len(link.split('.')) > 4


def is_unreadable(link):
    return any(char in link for char in ['xn--', 'xn----', 'xn------'])


def check_link(link):
    stats = {
        'redirect': is_redirect(link),
        'https': is_https(link),
        'ssl': has_ssl_cert(link),
        'suspicious': is_suspicious(link),
        'solution': is_solution(link),
        'suspicious_js': has_suspicious_js(link),
        'Long level': is_long_level(link),
        'Unreadability': is_unreadable(link)
    }
    return stats
