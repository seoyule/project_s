import re

category_list = {
    '신상품': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[1]'],
    '원피스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[2]'],
    '셔츠/남방': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '블라우스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]',
             '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '니트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '티&탑': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '빅사이즈': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]',
             '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '임부복': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[3]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '스커트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[4]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '청바지': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[4]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '팬츠': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[4]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '아우터': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[5]'],
    '세트 아이템': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[6]'],
    '샌들/슬리퍼/쪼리': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
                  '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '플랫/로퍼': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '힐/펌프스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '웨지힐': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '스니커즈/운동화': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
                 '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '워커/부츠': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '수제화': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[7]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[7]'],
    '쥬얼리': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '벨트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '헤어핀/밴드': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
               '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '모자': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '선그라스/안경': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
                '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '시계': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '기타': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[8]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[7]'],
    '가죽': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '숄더백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '토트백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '크로스백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]',
             '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '클러치/지갑': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]',
               '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '백팩': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[9]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '남성의류': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[10]']}

urls = [("https://sinsangmarket.kr/store/16892?isPublic=1","디오트 2층 C01 1STAR 원스타","no","no"),("https://sinsangmarket.kr/store/9466?isPublic=1","디오트 1층 C23 andante 안단테","no","no"),("https://sinsangmarket.kr/store/17944?isPublic=1","테크노 별관 9호 Bough 보우","no","no"),("https://sinsangmarket.kr/store/1429?isPublic=1","디오트 5층 E-05호 BUSTLING 버슬링","no","no"),("https://sinsangmarket.kr/store/21015?isPublic=1","디오트 2층 i-09 Byme바이미","no","no"),("https://sinsangmarket.kr/store/21781?isPublic=1","누죤 지하2층 213호 CC하니","no","no"),("https://sinsangmarket.kr/store/12007?isPublic=1","디오트 2층 C13 COMMASHOP(콤마샵)","no","no")]

fakes = ['디옷','디올','디오르','디욜','샤x','샤널','에르','에르메스','샤','구구','GC','구c','CHA','루이','베네','타이틀','PXG','탐브',
         '프라','MI','몽끌','에트로','베르체','coco','COCO','CD','cd','헤지']

def name_change(subject):
    subject = subject.lower().replace("ops"," 원피스")
    subject = subject.lower().replace("ope", " 원피스")
    subject = subject.lower().replace("jk", " 자켓")
    subject = subject.lower().replace("set", " 세트")
    subject = subject.lower().replace("tee", " 티셔츠")
    if re.search("bl$|BL$", subject):
        subject = subject.lower().replace("bl", " 블라우스")
    return subject