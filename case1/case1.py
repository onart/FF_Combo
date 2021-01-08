import fontforge, psMat
import os

#psMat 튜플 구조: 2x2행렬 기준 좌상/좌하/우상/우하/x병진/y병진
#글리프 생성: fontforge.fonts()[0].createChar(유니코드, 글리프이름)
BASEDIR='C:\\FFC\\'
BASEORDER=ord('가')
HANGUL_SVG_HEAD=
'''
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="-10 0 1034 1024">
'''
HANGUL_SVG_TAIL='</svg>'

HD=( 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
       'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ' )
MD=('ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
     'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ' )
ED=( '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
      'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ',
      'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

if not os.path.exists(BASEDIR):
    os.makedirs(BASEDIR)

def han2GL(c):
    return 'uni'+str(hex(ord(c)))[2:].upper()

def plusHan(h,m,e=''):
    return chr(BASEORDER+588*HD.index(h)+28*MD.index(m)+ED.index(e))

def getPath(c):
    f=open(BASEDIR+c+'.svg')
    v=f.read()
    f.close()
    v=v[v.find('<path'):v.find('</svg>')]
    return v

def mergeVec(v1, v2, name):
    f=open(BASEDIR+name+'.svg','w')
    f.write(HANGUL_SVG_HEAD)
    f.write(v1)
    f.write(v2)
    f.write(HANGUL_SVG_TAIL)
    f.close()

font=fontforge.fonts()[0]

for h in HD:
    for m in MD:
        top=plusHan(h,m)
        # 모음에 따른 초성 변환
        if m in 'ㅏㅐㅑㅒㅓㅔㅕㅖㅣ':
            pass
        elif m in 'ㅗㅛㅜㅠㅡ':
            pass
        elif m in 'ㅘㅙㅚㅝㅞㅟㅢ':
            pass
        # (추후 수정 가능)
        font[han2GL(h)].export(BASEDIR+h+'.svg')
        hp=getPath(h)
        font[han2GL(m)].export(BASEDIR+m+'.svg')
        mp=getPath(m)
        mergeVec(hp,mp,top)
        tp=getPath(top)
        font[top].importOutlines(BASEDIR+top+'.svg')
        for e in ED[1:]:
            # 초성+중성본 변환(상하 압축)
            full=plusHan(h,m,e)
            
            mergeVec(tp,ep,full)
            pass
