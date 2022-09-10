import re

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

    '플랫/로퍼': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '힐/펌프스': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '웨지힐': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '샌들/슬리퍼/쪼리': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
                  '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '스니커즈/운동화': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
                 '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '워커/부츠': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
              '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '수제화': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[15]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[7]'],

    '가죽': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '숄더백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '토트백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '크로스백': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
             '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '클러치/지갑': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
               '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '백팩': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '세일': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[16]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[7]'],

    '쥬얼리': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
            '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[1]'],
    '벨트': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[2]'],
    '헤어핀/밴드': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
               '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[3]'],
    '모자': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[4]'],
    '선그라스/안경': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
                '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[5]'],
    '시계': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[6]'],
    '기타': ['//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[17]',
           '//*[@id="eCategoryTbody"]/tr/td[2]/div/ul/li[7]'],
}

fakes = ['디옷','디올','디오르','디욜','샤x','샤널','에르','에르메스','샤','구구','GC','구c','CHA','루이','베네','타이틀','PXG','탐브',
         '프라','MI','몽끌','에트로','베르체','coco','COCO','CD','cd','헤지','TB']

color_ = {'베':'베이지','검':'검은색'}

image_check = ['이미지 사용 불가','이미지 공유가 불가','이미지 사용이 금지']

def name_change(subject):
    subject = subject.lower().replace("ops"," 원피스")
    subject = subject.lower().replace("ope", " 원피스")
    subject = subject.lower().replace("jk", " 자켓")
    subject = subject.lower().replace("set", " 세트")
    subject = subject.lower().replace("tee", " 티셔츠")
    if re.search("bl$|BL$", subject):
        subject = subject.lower().replace("bl", " 블라우스")
    return subject