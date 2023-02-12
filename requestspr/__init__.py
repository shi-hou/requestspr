from enum import IntEnum
import urllib.request

import requests as req

"""
requests在我开启Clash时发送请求会报错，遂自行封装了下
"""

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'


class ProxyMode(IntEnum):
    """代理模式"""

    NoProxy = 1
    '''不进行代理'''

    FollowSystem = 2
    '''使用系统代理'''

    Static = 3
    '''使用静态代理'''


class Requests:
    __NO_PROXIES = {'http': None, 'https': None}
    __static_proxies = __NO_PROXIES

    def __init__(self, user_agent=DEFAULT_USER_AGENT, timeout=(5, 5), proxy_mode=ProxyMode.FollowSystem,
                 static_proxies: dict = None):
        """
        :param user_agent: 发送请求的请求头的默认User-Agent
        :param timeout: 发送请求的默认timeout
        :param proxy_mode: 设置默认的代理模式，只在发请求时不提供proxies有效
        :param static_proxies: 若设置代理模式为ProxyMode.Static，则需提供
        """
        self.user_agent = user_agent
        self.timeout = timeout
        self.set_proxy_mode(proxy_mode, static_proxies)

    def __requests_proxies(self) -> dict:
        """根据代理模式获取代理"""
        if self.proxy_mode is ProxyMode.NoProxy:
            return self.__NO_PROXIES
        if self.proxy_mode is ProxyMode.FollowSystem:
            proxies = urllib.request.getproxies()
            for protocol, url in proxies.items():
                # 移除urllib.request.getproxies()中url的协议头
                if '://' in url:
                    proxies[protocol] = url.split('://')[1]
            return proxies
        if self.proxy_mode is ProxyMode.Static:
            return self.__static_proxies

    def set_proxy_mode(self, mode: ProxyMode, static_proxies: dict = None):
        """
        设置代理模式

        :param mode: 代理模式
        :param static_proxies: 若设置为静态代理，需提供代理信息，如：{'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}
        """
        if mode is ProxyMode.Static:
            if not static_proxies:
                raise Exception('需提供静态代理static_proxies')
            self.__static_proxies = static_proxies
        self.proxy_mode = mode

    def request(self, method, url, **kwargs):
        kwargs.setdefault('proxies', self.__requests_proxies())
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('User-Agent', self.user_agent)
        kwargs.setdefault('timeout', self.timeout)
        return req.request(method, url, **kwargs)

    def get(self, url, params=None, **kwargs):
        return self.request("get", url, params=params, **kwargs)

    def options(self, url, **kwargs):
        return self.request("options", url, **kwargs)

    def head(self, url, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        return self.request("head", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request("post", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("put", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("patch", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("delete", url, **kwargs)

    get_proxies = __requests_proxies
    '''获取代理信息'''
