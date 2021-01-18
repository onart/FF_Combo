# 자모 그려 둔 후, 위치에 맞춤
import fontforge, psMat

STD_C=(120,90,820,620)
STD_VV=(320,-86,715,820)
STD_HV=(54,136,962,642)

LEFT_HV=(85,190,750,370)
RIGHT_VV=(645,-90,830,820)
COMPL=(84.0, -113, 989.0, 849.0)

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

for umso in 'ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ':
    hr=font[umso].boundingBox()
    font[umso].transform(transC(hr,STD_C))
for umso in 'ㅏㅐㅑㅒㅓㅔㅕㅖ':
    mr=font[umso].boundingBox()
    font[umso].transform(transC(mr,STD_VV))
for umso in 'ㅗㅛㅜㅠ':
    mr=font[umso].boundingBox()
    font[umso].transform(transC(mr,STD_HV))
eu=font['ㅡ']
ee=font['ㅣ']
eu.transform(transV(eu.boundingBox(),STD_HV))
ee.transform(transV(ee.boundingBox(),STD_VV))
for umso in 'ㅘㅙㅚㅝㅞㅟㅢ':
    font[umso].addReference('ㅡ',transV(eu.boundingBox(),LEFT_HV))
    font[umso].addReference('ㅣ',transV(ee.boundingBox(),RIGHT_VV))

# 여기 이후로 ㅘㅙㅚㅝㅞㅟ를 그림(등고선 방향 동일하게), 그 후 1_3
