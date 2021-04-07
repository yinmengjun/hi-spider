import requests
from lxml import etree
from fake_useragent import UserAgent


class Login(object):

    def __init__(self):
        ua = UserAgent()
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': ua.random
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.session = requests.Session()

    def get_authenticity_token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        html = etree.HTML(response.text)
        authenticity_token = html.xpath('//*[@id="login"]/div[4]/form/input[1]/@value')
        return authenticity_token

    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'authenticity_token': self.get_authenticity_token()[0],
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        print(response.status_code)


if __name__ == "__main__":
    login = Login()
    login.login(email='yinmengjun0000@qq.com', password='xxx')
