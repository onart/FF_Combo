import fontforge, psMat

# 가로/세로 사이즈 840 가량으로 맞춤. 좌측하단이 (0,0)지점

# 미리 지정한 상수 좌표(백분율: 좌측하단 꼭짓점, 가로, 세로)
# 테스트 결과에 따라 수정 가능

CONS=(
    (54.0, 181.0, 555.0, 623.0),  # ㅏㅐㅑㅒㅓㅔㅕㅖㅣ와 자음
    (166.0, 360.0, 806.0, 723.0),  # ㅗㅛㅜㅠㅡ와 자음
    (131.0, 330.0, 636.0, 697.0),  # ㅘㅙㅚㅝㅞㅟㅢ와 자음
)
VOW=(
    (587.0, -107.0, 986.0, 847.0),  # ㅏㅐㅑㅒㅓㅔㅕㅖㅣ와 자음
    (48.0, 34.0, 981.0, 321.0),  # ㅗㅛㅜㅠㅡ와 자음
    (81.0, -110.0, 830.0, 850.0),  # ㅘㅙㅚㅝㅞㅟㅢ
)

# 모든 받침의 공통 위치, 테스트 결과에 따라 수정 가능
CONSB=(
    (300,-63,800,250),
)

BASEB=(
    (140,240,980,870),
)

STD_C=(120,90,820,620)
STD_VV=(320,-86,715,820)
STD_HV=(54,136,962,642)

LEFT_HV=(85,190,750,370)
RIGHT_VV=(645,-90,830,820)
COMPL=(84.0, -113, 989.0, 849.0)

BASEORDER=ord('가')

HD=( 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
       'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ' )
MD=('ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
     'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ' )
ED=( '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
      'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ',
      'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

def plusHan(h,m,e=''):
    return chr(BASEORDER+588*HD.index(h)+28*MD.index(m)+ED.index(e))

def transC(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지하지 않고 rect2의 비율을 따라감
    dst=(rect2[2]-rect2[0],rect2[3]-rect2[1])
    mat=psMat.scale(dst[0]/(rect1[2]-rect1[0]),dst[1]/(rect1[3]-rect1[1]))
    tr2=psMat.translate(rect2[0]-rect1[0],rect2[1]-rect1[1])
    mat=psMat.compose(mat,tr2)
    return mat

def transV(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지(긴 방향의 중심선 일치)
    dst=(rect2[2]-rect2[0],rect2[3]-rect2[1])
    mat=None
    if rect1[2]-rect1[0]>rect1[3]-rect1[1]:
        mat=psMat.scale(dst[0]/(rect1[2]-rect1[0]))
        #tr1=psMat.translate(0,(dst[1]+(rect1[3]-rect1[1])*dst[0]/(rect1[2]-rect1[0]))/2)
        #mat=psMat.compose(mat,tr1)
    else:
        mat=psMat.scale(dst[1]/(rect1[3]-rect1[1]))
        #tr1=psMat.translate((dst[0]+(rect1[2]-rect1[0])*dst[1]/(rect1[3]-rect1[1]))/2,0)
        #mat=psMat.compose(mat,tr1)
    tr2=psMat.translate(rect2[0]-rect1[0],rect2[1]-rect1[1])
    mat=psMat.compose(mat,tr2)
    return mat

font=fontforge.fonts()[0]

for h in HD:
    for m in MD:
        midRect=font[m].boundingBox()
        base=plusHan(h,m)
        ix=0
        if m in 'ㅏㅐㅑㅒㅓㅔㅕㅖㅣ':
            ix=0
        elif m in 'ㅗㅛㅜㅠㅡ':
            ix=1
        else:
            ix=2
        font[base].addReference(h,transC(STD_C,CONS[ix]))
        if m in 'ㅡㅣ':
            font[base].addReference(m,transV(midRect,VOW[ix]))
        else:
            font[base].addReference(m,transC(midRect,VOW[ix]))
        font[base].transform(transC(font[base].boundingBox(),COMPL))
        for e in ED[1:]:
            term=plusHan(h,m,e)
            font[term].addReference(base, transC(COMPL,BASEB[0]))
            font[term].addReference(e,transC(STD_C,CONSB[0]))
            font[term].transform(transC(font[term].boundingBox(),COMPL))

# 확인된 문제: addReference에서 transC의 효과가 약간 다름