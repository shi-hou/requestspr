import requestsp as requests


def google_search(text: str):
    """谷歌搜索"""
    return requests.get(f'https://www.google.com/search?q={text}')


if __name__ == '__main__':
    # 默认使用系统代理, 请求成功
    print(google_search('test'))

    # 不使用系统代理，请求失败
    # requests.set_proxy_mode(requests.ProxyMode.NoProxy)
    # print(google_search('test'))

    # 自行设置代理
    # requests.set_proxy_mode(requests.ProxyMode.Static, {'https': '127.0.0.1:7890'})
    # print(google_search('test'))