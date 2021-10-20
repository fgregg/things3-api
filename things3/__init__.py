import requests

class URL(str):
    def __truediv__(self, val):
        return URL(self + '/' + val)

class Things(requests.Session):
    BASE_URL = URL('https://cloud.culturedcode.com/version/1')

    def __init__(self, history_key=None):
        self.history_key = history_key
        super().__init__()

    def login(self, username, password):
        response = self.get(self.BASE_URL / 'account' / username,
                            headers={'Authorization': 'Password ' + password})
        auth_dict = response.json()
        self.history_key = auth_dict['history-key']
        return auth_dict

    @property
    def history_index(self):
        response = self.get(self.BASE_URL / 'history' / self.history_key)
        return response.json()

    @property
    def items(self):
        response = self.get(self.BASE_URL / 'history' / self.history_key / 'items')
        return response.json()
                            


if __name__ == '__main__':
    import os
    from pprint import pprint as print
    things = Things()
    print(things.login(os.environ['THINGS_USERNAME'],
                       os.environ['THINGS_PASSWORD']))
    print(things.history_index)
    print(things.items)    
