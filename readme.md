# requestspr

![PyPI](https://img.shields.io/pypi/v/requestspr)
![PyPI - License](https://img.shields.io/pypi/l/requestspr)

> 在启动了Clash的情况下，requests发送请求会报错，于是稍微封装了下

## Install
```
pip install requestspr
```

## Example

```python
from requestspr import Requests, ProxyMode


def twitter():
    """请求推特页面"""
    try:
        return requests.get('https://twitter.com/')
    except Exception as e:
        return e


if __name__ == '__main__':
    # 在开着Clash的情况下

    requests = Requests()

    # 获取代理信息
    print(requests.get_proxies())

    # 默认使用系统代理, 请求成功
    print(twitter())

    # 不使用系统代理，请求超时
    requests.set_proxy_mode(ProxyMode.NoProxy)
    print(twitter())

    # 自行设置代理
    requests.set_proxy_mode(ProxyMode.Static, {'https': '127.0.0.1:7890'})
    print(twitter())

```