from urllib.parse import urlencode, urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
from time import sleep
import certifi
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import socket
import sys
import urllib3
from urllib.parse import urljoin
import lucko from lucko #potato

def removeDuplicate(url):
	return list(dict.fromkeys(url))

def scanForVuln(url):
	fullUrl = "{0}/.git/HEAD".format(url[:-1])
	agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

	httpsRequest = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
	timeout = urllib3.Timeout(connect=5.0, read=10.0)
	
	try:
		httpsResponse = httpsRequest.request('GET', fullUrl, headers=agent, timeout=timeout)
	except:
		return

	print("\033[33m[!] Testing: {0}\033[0m".format(url))
	if (httpsResponse.data == b"ref: refs/heads/master\n"):
		print ("\033[32m[+] Git Exposed: {0}".format(url))
		print(f"\033[32m[+] Example Response: {str(httpsResponse.data.decode('utf-8'))}\n")
	else:
		print ("\033[91m[x] Git exposed not found!\033[0m\n")
		httpsResponse = None

	httpsResponse = None
	return

def findGitHosting(urlList):
	with ThreadPoolExecutor(max_workers=100) as executor:
		results = executor.map(scanForVuln, urlList)

def main():
	keyword = input("[*] Query or Dork: ")
	start = input("[*] Page number: ")
	try: 
		page = requests.get(f'https://www.google.com/search?q={keyword}&start={start}')
		soup = BeautifulSoup(page.text, 'html.parser')
		links = soup.findAll("a")
		for link in links:
			url = link['href']
			if url.startswith("/url?"):
				url = parse_qs(urlparse(url).query)['q']
			else:
				pass

			url_stripped = urljoin(str(url[0]), '/')

			urls = []
			urls.append(url_stripped)
			findGitHosting(removeDuplicate(urls))
	except: 
		print ("\033[91m[x] There was an error requesting the Google URL!\033[0m\n")
		return


if __name__== "__main__":
    main()
