







html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


urls = [("https://sinsangmarket.kr/store/1319?isPublic=1","더클리닝",'(.*모델정보[^\n]*)'),
        ]

r = soup.find("div", attrs={"class": "row__content"}).get_text()
try:
    p = re.compile(urls[0][2], re.DOTALL)
    m = p.search(r)
    comment = m.group(1)
    comment = comment.lower().replace("\n", "<br>")

except:
    r = ""
    comment = ""
