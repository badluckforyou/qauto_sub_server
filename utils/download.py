import time
import requests

url = "https://appcenter-filemanagement-distrib4ede6f06e.azureedge.net/5aa286e3-9517-4752-a978-e37cac23dbd0/POS%20Dev.ipa?sv=2019-02-02&sr=c&sig=V7BlgDEmW2MCF6EJZ8t05TindlYn4j3okorRk%2BzOPv0%3D&se=2020-07-01T04%3A17%3A36Z&sp=r&download_origin=appcenter"
url = "https://appcenter-filemanagement-distrib3ede6f06e.azureedge.net/f8b50d22-ae9c-436d-ae79-924bd98e9fe0/pos-dev.ipa?sv=2019-02-02&sr=c&sig=SviVOeY2ZGXE%2B5UJiF%2F%2BPXUyAiNqr0MBl6a4ROV8hOI%3D&se=2020-07-01T04%3A19%3A28Z&sp=r&download_origin=appcenter"
def download(url, savepath):
    pass


url = "https://install.appcenter.ms/orgs/bindo-labs-organization/apps/bindo-pos-dev/distribution_groups/public"
headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
response = requests.get(url, headers=headers)
print(response.text)