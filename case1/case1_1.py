# 한글 글리프를 생성
import fontforge

font=fontforge.fonts()[0]

i=ord('ㄱ')
while i<=ord('ㅣ'):
    font.createChar(i,chr(i))
    i+=1
i=ord('가')
while i<=ord('힣'):
    font.createChar(i,chr(i))
    i+=1
del i

#완성 글리프 비우기 코드
i=ord('가')
while i<=ord('힣'):
    font[chr(i)].clear()
    i+=1
del i