from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.1'
with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='requestspr',  # package name
    version=VERSION,  # package version
    description='在启动了Clash的情况下，requests发送请求会报错，于是稍微封装了下',  # package description
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
    ],
)
