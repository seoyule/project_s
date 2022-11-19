import re
import time
#url info -- listfile 파일 참고

block_seller = ["동평화 2층","동평화 3층","동평화 4층", # 픽업시간 안맞음
                "신발상가 A동 2층 67호 조원",
                '신발상가 A동 3층 24호 패션시티',
                '신발상가 A동 3층 20호 SEXING섹싱',
                'HANAHANA(하나하나)', # 자기 상품 올라가는거 싫어함
                '누죤 지하1층 726호 Joa 좋아',
                '동평화 1층 신관108호 JIHOO (지후)', # 반품율 높음. 보꾸 계열
                '청평화 1층 라15호 보꾸 Boggu', # 반품율 높음. 보꾸 계열
                '남평화 3층 136호 예삐박스', # 반품율 높음.
                '디오트 2층 i-09 Byme바이미', # 반품율 높음.
                '테크노 지하1층 B42호 colorandchoice(컬러앤초이스)',
                ]

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

category_convert = {
    '아우터': '아우터',
    '티&탑': '티&탑',
    '원피스': '원피스',
    '블라우스': '블라우스',
    '니트': '니트',
    '청바지': '청바지',
    '팬츠': '팬츠',
    '스커트': '스커트',
    '세일상품': '세일상품',
    '시즌상품': '시즌상품',
    '세트 아이템': '세트 아이템',
    '셔츠/남방': '셔츠/남방',
    '빅사이즈': '빅사이즈',
    '임부복': '빅사이즈',

    '플랫/로퍼': '여성 신발',
    '힐/펌프스': '여성 신발',
    '웨지힐': '여성 신발',
    '샌들/슬리퍼/쪼리': '여성 신발',
    '스니커즈/운동화': '여성 신발',
    '워커/부츠': '여성 신발',
    '수제화': '여성 신발',

    '가죽': '여성 가방',
    '숄더백': '여성 가방',
    '토트백': '여성 가방',
    '크로스백': '여성 가방',
    '클러치/지갑': '여성 가방',
    '백팩': '여성 가방',
    '세일': '여성 가방',

    '쥬얼리': '악세사리',
    '벨트': '악세사리',
    '헤어핀/밴드': '악세사리',
    '모자': '악세사리',
    '선그라스/안경': '악세사리',
    '시계': '악세사리',
    '기타': '악세사리',
}


fakes = ['디옷','디올','디오르','디욜','샤x','샤널','샤넬','CHA','에르메스','구구','구c','구찌','베네','타이틀','PXG','탐브','TB',
         '프라','몽끌','에트로','베르체','coco','COCO','셀린','발망']

image_check = []
#image_check = ['이미지 사용 불가','이미지 공유가 불가','이미지 사용이 금지']

block_subject = [
    '원피스 레트로 프릴 롱원피스',
    '원피스 뽀글원피스',
    '아우터 모모 울 방모자켓',
    '아우터 신상)꽈배기니트가죽 자켓',
    '아우터 신상)닥스숄 가디건',
    '아우터 날개무스탕조끼',
    '세트 아이템 후드p트레이닝세트',
    '원피스 맥시트위드원피스',
    '아우터 페이즐오버가디건',
    '아우터 니트패딩가디건',
    '아우터 가죽배색 트위드자켓 가을신상',
    '원피스 로마트위드투피스',
    '티-탑 플루토 맨투맨',
    '원피스 메리유 주름 롱원피스',
    '아우터 아리니트자켓',
    '니트 꽈배기 롱 니트 폴라',
    '티-탑 new) 비숑 쭉 티 긴팔 남여공용 빅사이즈',
]

def name_change(subject):
    subject = subject.lower().replace("[", "(")
    subject = subject.lower().replace("]", ")")
    subject = subject.lower().replace(",", ".")
    subject = subject.lower().replace("?", "")
    subject = subject.lower().replace("_", "-")
    subject = subject.lower().replace("현금", "")
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
    if re.search("y[.]$|Y[.]$", subject):
        subject = subject.lower().replace("y.", " 가디건")
    for i in fakes:
        if i in subject:
            subject = subject.replace(i, i[0])
    return subject