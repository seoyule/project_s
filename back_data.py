"""작업한 내용을 원격 저장소에 저장하는 순서 간단 정리
프로그램 변경 작업하기
git add <파일명> 또는 git add * 명령 수행하기
git commit -m "변경사항 요약" 명령 수행하기
git push 명령 수행하기"""

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
