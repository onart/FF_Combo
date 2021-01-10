import fontforge, psMat

# 가로/세로 사이즈 840 가량으로 맞춤. 좌측하단이 (0,0)지점

# 미리 지정한 백분율 상수 좌표(백분율: 좌측하단 꼭짓점, 가로, 세로)
# 테스트 결과에 따라 수정 가능

CONS=(
    (13,35,45,35),  # ㅏㅐㅑㅒㅓㅔㅕㅖㅣ와 자음
    (25,45,50,35),  # ㅗㅛㅜㅠㅡ와 자음
    (25,50,35,30),  # ㅘㅙㅚㅝㅞㅟㅢ와 자음
    )
VOW=(
    (64,10,25,80),  # ㅏㅐㅑㅒㅓㅔㅕㅖㅣ와 자음
    (10,20,80,25),  # ㅗㅛㅜㅠㅡ와 자음
    (15,10,70,80),  # ㅘㅙㅚㅝㅞㅟㅢ
)

# 모든 받침의 공통 위치, 테스트 결과에 따라 수정 가능
CONSB=(
    ()
)



RATIO=8.4
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

def trans(rect1, rect2):
    # rect1을 rect2에 맞게 조정. rect1의 비율을 유지(긴 방향의 중심선 일치)
    rect2=list(rect2)
    for i in range(4):
        rect2[i]*=RATIO
    mat=None
    if rect1[2]-rect1[0]>rect1[3]-rect1[1]:
        mat=psMat.scale(rect2[2]/(rect1[2]-rect1[0]))
        tr1=psMat.translate(0,(rect2[2]+rect1[2]-rect2[0])/2)
        mat=psMat.compose(mat,tr1)
    else:
        mat=psMat.scale(rect2[3]/(rect1[3]-rect1[1]))
        tr1=psMat.translate((rect2[3]+rect1[3]-rect2[1])/2,0)
        mat=psMat.compose(mat,tr1)
    tr2=psMat.translate(rect2[0]-rect1[0],rect2[1]-rect1[1])
    mat=psMat.compose(mat,tr2)
    return mat

font=fontforge.fonts()[0]

for h in HD:
    headRect=font[h].boundingBox()
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
        font[base].addReference(h,trans(headRect,CONS[ix]))
        font[base].addReference(m,trans(midRect,VOW[ix]))
        for e in ED:
            pass