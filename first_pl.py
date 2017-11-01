import sys, requests, re

domain="http://www.mosigra.ru"
links = set()
links.add(domain)

mail_pattern = r'[a-zA-Z0-9]+(?:[._+%-]+[a-zA-Z0-9]+)*@(?:[a-zA-Z0-9]?)+[.][a-zA-Z]{2,}'
link_pattern = r'href="(?:<siteURL>)?(?:\.\.)*(?:\/?[a-zA-Z0-9%-])+\??(?:[a-zA-Z0-9]+\=[a-zA-Z0-9_%-]+[;&]?)*(?:\.html|\.htm|\/)?"'

temp_url = domain.replace("/", "\/")
temp_url = temp_url.replace(".", "\.")
temp_url = temp_url.replace("-", "\-")
link_pattern = link_pattern.replace("<siteURL>", temp_url)
regular_mail = re.compile(mail_pattern)
regular_url = re.compile(link_pattern)

checked_links = set()
mails = set()

while (len(checked_links) < 30):
    link = links.pop()
    if(link in checked_links):
    	continue
    checked_links.add(link)
    site = requests.get(link)
    match_url = regular_url.findall(site.text)
    match_mail = regular_mail.findall(site.text)
    for url in match_url:
            current_url = url[:-1]
            current_url = current_url.replace('href=\"', "")
            if (current_url[0] == "."):
                current_url = re.sub(r'\.\.\/', "", current_url)
                processed_url = link + current_url
            elif (current_url[0] == "/"):
                processed_url = domain + current_url
            elif (current_url.startswith("http://") == False):
                processed_url = domain + "/" + current_url
            else:
                processed_url = current_url
            if (processed_url not in checked_links):
                links.add(processed_url)
    for mail in match_mail:
            if (mail not in mails):
                mails.add(mail)


for mail in mails:
    print(mail + '\n')
