#!/bin/python3
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from colorama import init
from pyfiglet import Figlet
init(autoreset=True)


uaList = UserAgent()
proxies = []
uaPayload = {'user-agent': uaList.random}
proxyUrlHTTPS = 'https://www.sslproxies.org/'


def initial(url):
    print("\n\033[1;32m [+] Scraping IPs")
    proxiesReq = Request(url, headers=uaPayload)
    proxiesCont = urlopen(proxiesReq).read().decode('utf8')
    soup = BeautifulSoup(proxiesCont, 'html.parser')
    proxyTable = soup.find(id='proxylisttable')

    for row in proxyTable.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })


def randomProxy(theList):
    return random.randrange(len(theList))


def writeProxy(text):
    f = open('proxy-list.txt','a')
    f.append(text)
    f.close()


def isAlive(proxyList):
    proxiesCopy = proxyList
    print("\n\033[1;32m [+] Checking proxy is alive or dead.")
    proxyIn = randomProxy(proxiesCopy)
    proxy = proxiesCopy[proxyIn]
    checked = 0

    while checked < len(proxyList):
        for n in range(0, 100):
            req = Request('http://checkip.amazonaws.com/')
            req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'https')

            if n % 10 == 0:
                checked += 1
                try:
                    my_ip = urlopen(req).read().decode('utf8')
                    aliveProxy = '\033[1;32m [+] ' + str(n) + ': ' + my_ip + ' ' + proxy['port']
                    print(aliveProxy)
                    writeProxy(aliveProxy)
                except:
                    del proxiesCopy[proxyIn]
                    print('\033[1;33m [-] Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
                

def main():
    banner = Figlet(font='banner3-D')
    print(banner.renderText('\n    | FPF |    '))
    print(Figlet(font='slant').renderText('Free - Proxy           Finder'))
    try:
        print('''\033[1;32m 
        This Program Checks for 100 Proxies And Print The Alive Proxies To a File, proxy-list.txt, And Deletes The Dead Proxy\n. 
        1 --> for https
        2 --> for http
        3 --> for socks-4
        4 --> for socks-5
        ''')
        while True:
            proxyType = input("\n\033[1;32m Which proxy: ")
            if proxyType == '1':
                try:
                    initial(proxyUrlHTTPS)
                except:
                    print("\033[1;31m [!] An Error Accured!")
                    break
                if len(proxies) > 1:
                    isAlive(proxies)
                else:
                    print("\033[1;31m [!] Check Your Internet Connection")
                    break
            else:
                print("\033[1;33m [-] Currently Unavailable!")
    except KeyboardInterrupt:
        print("\n\n\033[1;32m Bye!")

if __name__ == "__main__":
    main()
