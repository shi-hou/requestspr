from enum import IntEnum
import urllib.request

import requests

"""
requests在我开启Clash时发送请求会报错，遂自行封装了下
"""


class ProxyMode(IntEnum):
    """代理模式"""

    NoProxy = 1
    '''不进行代理'''

    FollowSystem = 2
    '''使用系统代理'''

    Static = 3
    '''使用静态代理'''


__NO_PROXIES = {'http': None, 'https': None}
__static_proxies = __NO_PROXIES
__proxy_mode = ProxyMode.FollowSystem
'''代理模式, 默认为使用系统代理'''


def __requests_proxies() -> dict:
    """根据代理模式获取代理"""
    if __proxy_mode is ProxyMode.NoProxy:
        return __NO_PROXIES
    if __proxy_mode is ProxyMode.FollowSystem:
        proxies = urllib.request.getproxies()
        for protocol, url in proxies.items():
            # 移除urllib.request.getproxies()中url的协议头
            if '://' in url:
                proxies[protocol] = url.split('://')[1]
        return proxies
    if __proxy_mode is ProxyMode.Static:
        return __static_proxies


def set_proxy_mode(mode: ProxyMode, static_proxies: dict = None):
    """
    设置代理模式

    :param mode: 代理模式
    :param static_proxies: 若设置为静态代理，需提供代理信息，如：{'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}
    """
    if mode is ProxyMode.Static:
        if not static_proxies:
            raise Exception('需提供静态代理static_proxies')
        global __static_proxies
        __static_proxies = static_proxies
    global __proxy_mode
    __proxy_mode = mode


def request(method, url, **kwargs):
    kwargs['proxies'] = __requests_proxies()
    return requests.request(method, url, **kwargs)


def get(url, params=None, **kwargs):
    return request("get", url, params=params, **kwargs)


def options(url, **kwargs):
    return request("options", url, **kwargs)


def head(url, **kwargs):
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request("post", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    return request("put", url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    return request("patch", url, data=data, **kwargs)


def delete(url, **kwargs):
    return request("delete", url, **kwargs)
