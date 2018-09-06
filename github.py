from requests import Session
from urllib.parse import quote
from pyquery import PyQuery as pq

class github:

    def __init__(self,username:str,password:str):
        self.username=username
        self.password=password
        self.session=Session()
        self.url_login,self.url_logout,self.url_session,self.repos_list_url="https://github.com/login","https://github.com/logout","https://github.com/session","https://github.com/"+quote(self.username)
        self.headers={
            'User-Agent':'Mozilla/5.0'
        }

    def getData(self)->dict:
        data={}
        try:
            r=self.session.get(url=self.url_login,headers=self.headers,timeout=30)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            PQ=pq(r.text)
            authenticity_token=PQ('input')('[name="authenticity_token"]').attr('value')
            data={
                'authenticity_token':authenticity_token,
                'commit':'Sign+in',
                'login':self.username,
                'password':self.password,
                'utf8':'✓'
            }
        except Exception as e:
            print('getData',e.args)
        finally:
            return data

    def login(self):
        try:
            data=self.getData()
            r=self.session.post(url=self.url_session,data=data,timeout=60)
            r.raise_for_status()
        except Exception as e:
            print('login',e.args)
        finally:
            return None

    def logout(self):
        try:
            form_data=self.getData()
            data={
                'utf8':form_data['utf8'],
                'authenticity_token':form_data['authenticity_token']
            }
            r=self.session.post(url=self.url_logout,data=data,timeout=60)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
        except Exception as e:
            print('logout',e.args)
        finally:
            return None

    def repos_list(self):
        lis=[]
        try:
            r=self.session.get(url=self.repos_list_url,timeout=60)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            PQ=pq(r.text)
            for inf in PQ('ol')('li'):
                PQ=pq(inf)
                dic={
                    'url':'https://github.com'+PQ('[class="d-block"]')('a').attr('href'),
                    'title':PQ('[class="repo js-repo"]').attr('title'),
                    '.md':PQ('[class="pinned-repo-desc text-gray text-small d-block mt-2 mb-3"]').text()
                }
                lis.append(dic)
        except Exception as e:
            print('repos-list',e.args)
        finally:
            return lis

def main():
    git=github('********','********')
    git.login()
    for i in git.repos_list():
        print(i)
    git.logout()


if __name__ == '__main__':
    main()