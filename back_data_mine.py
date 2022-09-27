import re

#url info -- listfile 파일 참고

block_seller = ["동평화 2층","동평화 3층","동평화 4층","신발상가 A동 2층 67호 조원",'신발상가 A동 3층 24호 패션시티','신발상가 A동 3층 20호 SEXING섹싱']

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
         '프라','MI','몽끌','에트로','베르체','coco','COCO','CD','cd','헤지','TB', '셀린', '셀린느','발먼']

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
    if re.search("y$|Y$", subject):
        subject = subject.lower().replace("y", " 가디건")
    return subject