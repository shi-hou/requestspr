import os

if __name__ == '__main__':
    print(os.system('python setup.py sdist build'))
    print(os.system('python setup.py bdist_wheel --universal'))
    print(os.system('twine upload dist/*'))
