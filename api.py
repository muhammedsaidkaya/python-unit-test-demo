import requests

class API():

    def __init__(self):
        pass

    def request(self, page, count):
        if page == None or count == None:
            raise ValueError
        try:
            return requests.get(f'https://jsonapi/articles?page={page}&count={count}')
        except:
            return None

    def closer(self, something):
        return something.close()