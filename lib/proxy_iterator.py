proxies = [{"http": "http://192.168.0.96:4234"},
           {"http": "http://192.168.0.93:4234"},
           {"http": "http://192.168.0.90:4234"},
           {"http": "http://192.168.0.94:4234"},
           {"http": "http://192.168.0.98:4234"},
           {"http": "http://192.168.0.99:4234"},
           {"http": "http://192.168.0.100:4234"},
           {"http": "http://192.168.0.101:4234"},
           {"http": "http://192.168.0.102:4234"},
           {"http": "http://192.168.0.103:4234"}, ]


class Proxy:
    def __init__(self):
        self.data = proxies
        self.index = len(proxies)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            self.index = len(proxies) - 1
        else:
            self.index = self.index - 1
        return self.data[self.index]


if __name__ == '__main__':
    p = Proxy()
    for i in range(11):
        print(next(p))
