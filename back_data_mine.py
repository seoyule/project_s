import re

urls = [("https://sinsangmarket.kr/store/8984?isPublic=1","누죤 지하1층 615호 오블리","no"),("https://sinsangmarket.kr/store/25759?isPublic=1","동평화 2층 나16호 노아","no"),("https://sinsangmarket.kr/store/5244?isPublic=1","디오트 1층 H16 진스타","no"),("https://sinsangmarket.kr/store/306?isPublic=1","디오트 2층 E08 에펠(eiffel)","no"),("https://sinsangmarket.kr/store/24164?isPublic=1","팀204 6층 630호 Silhouette실루엣","no"),("https://sinsangmarket.kr/store/15628?isPublic=1","APM 4층 4 Authentic 어센틱서울","no"),("https://sinsangmarket.kr/store/22211?isPublic=1","APM PLACE 지하2층 39 yellowband","no"),("https://sinsangmarket.kr/store/9765?isPublic=1","남평화 3층 127호 초이스(Choice)","no"),("https://sinsangmarket.kr/store/21952?isPublic=1","남평화 3층 136호 예삐박스","no"),("https://sinsangmarket.kr/store/16895?isPublic=1","누죤 4층 206호 제이프랑","no"),("https://sinsangmarket.kr/store/21781?isPublic=1","누죤 지하2층 213호 CC하니","no"),("https://sinsangmarket.kr/store/11711?isPublic=1","누죤 지하2층 706호 쵸콜릿","no"),("https://sinsangmarket.kr/store/5246?isPublic=1","디오트 1층 E13 DOUBLEM(더블엠)","no"),("https://sinsangmarket.kr/store/16892?isPublic=1","디오트 2층 C01 1STAR 원스타","no"),("https://sinsangmarket.kr/store/21015?isPublic=1","디오트 2층 i-09 Byme바이미","no"),("https://sinsangmarket.kr/store/2729?isPublic=1","디오트 2층 J06 헤르츠","no"),("https://sinsangmarket.kr/store/10446?isPublic=1","디오트 지하1층 D09 도어","no"),("https://sinsangmarket.kr/store/16361?isPublic=1","디오트 지하2층 A05-1 Raon 라온","no"),("https://sinsangmarket.kr/store/20888?isPublic=1","맥스타일 2층 2-03 끌리어","no"),("https://sinsangmarket.kr/store/1892?isPublic=1","맥스타일 3층 3-16 누보","no"),("https://sinsangmarket.kr/store/7181?isPublic=1","스튜디오W 3층 35호 스타제이 (StarJ)","no"),("https://sinsangmarket.kr/store/15864?isPublic=1","신발상가 A동 2층 67호 조원","no"),("https://sinsangmarket.kr/store/15040?isPublic=1","제일평화 2층 137호 miho","no"),("https://sinsangmarket.kr/store/10426?isPublic=1","청평화 1층 라15호 보꾸 Boggu","no"),("https://sinsangmarket.kr/store/1042?isPublic=1","APM 6층 32 SB(스타일봉)에스비","no"),("https://sinsangmarket.kr/store/375?isPublic=1","DDP패션몰 (유어스) 2층 42 ACEPT n MARYBLACK 에이셉트앤메리블랙","no"),("https://sinsangmarket.kr/store/26052?isPublic=1","DDP패션몰 (유어스) 3층 118-5(신상드림센터) 아우어 프로젝트","no"),("https://sinsangmarket.kr/store/26320?isPublic=1","DDP패션몰 (유어스) 3층 118-7(신상드림센터) 어닝","no"),("https://sinsangmarket.kr/store/5202?isPublic=1","DWP (동원프라자) 2층 18호 바이율","no"),("https://sinsangmarket.kr/store/12031?isPublic=1","DWP (동원프라자) 3층 25 일진(1jean)","no"),("https://sinsangmarket.kr/store/10442?isPublic=1","남평화 1층 나125호 도진 옴니아","no"),("https://sinsangmarket.kr/store/23799?isPublic=1","남평화 1층 다62호 데일리","no"),("https://sinsangmarket.kr/store/10500?isPublic=1","누죤 1층 204호 화이트 White","no"),("https://sinsangmarket.kr/store/10759?isPublic=1","누죤 1층 701호 야무지게 (YAMUJIGE)","no"),("https://sinsangmarket.kr/store/367?isPublic=1","누죤 3층 413호 noticeboard (노티스보드)","no"),("https://sinsangmarket.kr/store/5567?isPublic=1","누죤 5층 101호 Helmut (헬뮤트)","no"),("https://sinsangmarket.kr/store/16912?isPublic=1","누죤 5층 227호 샤인","no"),("https://sinsangmarket.kr/store/1772?isPublic=1","누죤 6층 524호 B747(비칠사칠)","no"),("https://sinsangmarket.kr/store/9240?isPublic=1","동평화 1층 신관102호 써니","no"),("https://sinsangmarket.kr/store/19835?isPublic=1","디오트 1층 J11 콜라컴퍼니","no"),("https://sinsangmarket.kr/store/7585?isPublic=1","디오트 2층 B16 에스앤에스(SNS)","no"),("https://sinsangmarket.kr/store/26517?isPublic=1","디오트 3층 G08 마키","no"),("https://sinsangmarket.kr/store/25189?isPublic=1","디오트 3층 i-23 mayflower 메이플라워","no"),("https://sinsangmarket.kr/store/11740?isPublic=1","디오트 지하1층 A12 뮤즈팜므","no"),("https://sinsangmarket.kr/store/23271?isPublic=1","디오트 지하1층 E12-1 민잇 mean it","no"),("https://sinsangmarket.kr/store/4232?isPublic=1","디오트 지하2층 A01 빅싸이즈","no"),("https://sinsangmarket.kr/store/16485?isPublic=1","디오트 지하2층 N77 Vixen빅센","no"),("https://sinsangmarket.kr/store/17288?isPublic=1","디오트 지하2층 다6 느낌표","no"),("https://sinsangmarket.kr/store/24987?isPublic=1","맥스타일 지하1층 171 요이요이 YOIYOI","no"),("https://sinsangmarket.kr/store/18219?isPublic=1","벨포스트 2층 56호 화이트","no"),("https://sinsangmarket.kr/store/25291?isPublic=1","벨포스트 2층 87호 PetitNana피어트나나","no"),("https://sinsangmarket.kr/store/24989?isPublic=1","스튜디오W 3층 8호 ROAR로어","no"),("https://sinsangmarket.kr/store/25069?isPublic=1","시즌상가 (구 JABA11) 2층 H-20 캐롯 carrot","no"),("https://sinsangmarket.kr/store/11578?isPublic=1","신발상가 C동 1층 102호 SMSHOES(에스엠슈즈)","no"),("https://sinsangmarket.kr/store/12954?isPublic=1","신발상가 C동 2층 46호 미노","no"),("https://sinsangmarket.kr/store/18614?isPublic=1","신발상가 C동 3층 가-17호 제이밍","no"),("https://sinsangmarket.kr/store/23248?isPublic=1","신발상가 D동 2층 10호 바이앤바이(buyandbuy)","no"),("https://sinsangmarket.kr/store/15489?isPublic=1","신발상가 D동 2층 1호 토브","no"),("https://sinsangmarket.kr/store/168?isPublic=1","신발상가 D동 2층 4호 에이유(au)","no"),("https://sinsangmarket.kr/store/5182?isPublic=1","신평화 A동 지하1층 가23호 Jini 지니","no"),("https://sinsangmarket.kr/store/9860?isPublic=1","청평화 1층 가8호 아뜨리오","no"),("https://sinsangmarket.kr/store/5449?isPublic=1","청평화 1층 나23호 ara 아라","no"),("https://sinsangmarket.kr/store/5894?isPublic=1","청평화 1층 라25호 프로섬 (prorsum)","no"),("https://sinsangmarket.kr/store/14111?isPublic=1","청평화 2층 나42호 보타이","no"),("https://sinsangmarket.kr/store/23848?isPublic=1","청평화 3층 나34호 씨메르Cimer","no"),("https://sinsangmarket.kr/store/1425?isPublic=1","청평화 3층 다36호 오레오레","no"),("https://sinsangmarket.kr/store/17285?isPublic=1","청평화 4층 C39호 아미","no"),("https://sinsangmarket.kr/store/821?isPublic=1","청평화 4층 C40호 Sonamoo 소나무","no"),("https://sinsangmarket.kr/store/26499?isPublic=1","청평화 4층 D34호 도아","no"),("https://sinsangmarket.kr/store/25838?isPublic=1","청평화 5층 가60호 Romantic_Booth(로맨틱부스)","no"),("https://sinsangmarket.kr/store/1657?isPublic=1","청평화 5층 나43호 MOON","no"),("https://sinsangmarket.kr/store/21948?isPublic=1","테크노 4층 426호 도비","no")]

category_list = {
    '아우터': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[1]'],
    '티&탑': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[2]'],
    '원피스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]'],
    '블라우스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[4]'],
    '니트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[5]'],
    '청바지': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[6]'],
    '팬츠': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]'],
    '스커트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]'],
    '세일상품': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]'],
    '시즌상품': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[10]'],
    '세트 아이템': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[11]'],
    '셔츠/남방': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[12]'],
    '빅사이즈': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[13]'],
    '임부복': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[14]'],

    '플랫/로퍼': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],
    '힐/펌프스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],
    '웨지힐': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],
    '샌들/슬리퍼/쪼리': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],
    '스니커즈/운동화': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],
    '워커/부츠': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],
    '수제화': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]'],

    '가죽': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],
    '숄더백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],
    '토트백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],
    '크로스백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],
    '클러치/지갑': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],
    '백팩': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],
    '세일': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]'],

    '쥬얼리': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
    '벨트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
    '헤어핀/밴드': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
    '모자': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
    '선그라스/안경': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
    '시계': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
    '기타': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]'],
}

fakes = ['디옷','디올','디오르','디욜','샤x','샤널','에르','에르메스','샤','구구','GC','구c','CHA','루이','베네','타이틀','PXG','탐브',
         '프라','MI','몽끌','에트로','베르체','coco','COCO','CD','cd','헤지','TB']

color_ = {'베':'베이지','검':'검은색'}

image_check = ['이미지 사용 불가','이미지 공유가 불가','이미지 사용이 금지']

def name_change(subject):
    subject = subject.lower().replace("ops"," 원피스")
    subject = subject.lower().replace("ope", " 원피스")
    subject = subject.lower().replace("jk", " 자켓")
    subject = subject.lower().replace("sk", " 스커트")
    subject = subject.lower().replace("set", " 세트")
    subject = subject.lower().replace("tee", " 티셔츠")
    subject = subject.lower().replace("판매1위", "")
    subject = subject.lower().replace("  ", " ")
    if re.search("bl$|BL$", subject):
        subject = subject.lower().replace("bl", " 블라우스")
    if re.search("t$|T$", subject):
        subject = subject.lower().replace("t", " 티셔츠")
    return subject