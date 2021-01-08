import fontforge

font=fontforge.fonts()[0]
# Create 한글 glyph
i=ord('ㄱ')
while i<=ord('ㅣ'):
    font.createChar(i,chr(i))
    i+=1
i=ord('가')
while i<=ord('힣'):
    font.createChar(i,chr(i))
    i+=1
del i

