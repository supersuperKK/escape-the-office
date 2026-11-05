# 用法: pip install pillow && python3 tools/build_icons.py
# 逃离办公室 道具图标 16x16，sweetie16 调色板。build.py 是唯一源头，别手改 PNG。
from PIL import Image, ImageDraw, ImageFont
import os
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
PAL = {'K':'#1a1c2c','W':'#f4f4f4','G':'#94b0c2','S':'#566c86','D':'#333c57','R':'#b13e53',
       'O':'#ef7d57','Y':'#ffcd75','L':'#a7f070','N':'#38b764','T':'#257179','B':'#29366f',
       'U':'#3b5dc9','C':'#41a6f6','A':'#73eff7','P':'#5d275d'}

ICONS = {}
def icon(key, name, rows, top=0):
    g = [''] * 16
    for i, r in enumerate(rows):
        assert len(r) <= 16, (key, i, r, len(r))
        g[top + i] = r
    ICONS[key] = (name, [r.ljust(16, '.') for r in g])

icon('badge', '工牌', [
"...U........U...",
"...U........U...",
"....U......U....",
".....U....U.....",
"......UKKU......",
"...KKKKSSKKKK...",
"...KWWWWWWWWK...",
"...KWYYWGGGWK...",
"...KWYYWWWWWK...",
"...KWOOWGGWWK...",
"...KWWWWWWWWK...",
"...KUUUUUUUUK...",
"...KUUUUUUUUK...",
"....KKKKKKKK....",
], top=1)

icon('milktea', '半杯冰奶茶', [
"..........R.....",
".........R......",
"........R.......",
"...KKKKKRKKKK...",
"...KAWWWRWWWK...",
"...KWWWWRWWWK...",
"....KWWWRWWK....",
"....KYYYRYYK....",
"....KYYYYYYK....",
"....KDYYYDYK....",
"....KYDYDYYK....",
".....KDYYDK.....",
".....KKKKKK.....",
], top=1)

icon('powerbank', '充电宝', [
"....KKKKKKKK....",
"....KGSSSSSK....",
"....KGSSSYSK....",
"....KGSSYYSK....",
"....KGSYYYSK....",
"....KGSSYSSK....",
"....KGSYSSSK....",
"....KGSSSSSK....",
"....KGLLLLSK....",
"....KGSSSSSK....",
"....KKKKKKKK....",
".......KK.......",
".......SS.......",
"........SSS.....",
], top=1)

icon('folder', '文件夹', [
".KKKKK..........",
"KYYYYYKKKKKKKK..",
"KYYYYYYYYYYYYYK.",
"KYWWWWWWWWWWWYK.",
"KKKKKKKKKKKKKKK.",
"KYYYYYYYYYYYYYK.",
"KOOOOOOOOOOOOOK.",
"KOOOOWWWWWOOOOK.",
"KOOOOOOOOOOOOOK.",
"KOOOOOOOOOOOOOK.",
"KKKKKKKKKKKKKKK.",
], top=3)

icon('roofkey', '天台钥匙', [
"..KKK...........",
".KYYYK..........",
"KYK.KYK.........",
"KYK.KYKKKKKKKK..",
"KYK.KYYYYYYYYYK.",
".KYYYKKKKKYKKYK.",
"..KKK....KYK.KK.",
"..........K.....",
], top=4)

icon('outpass', '盖章外出单', [
"...KKKKKKKKKK...",
"...KWWWWWWWWK...",
"...KWSSSSSSWK...",
"...KWWWWWWWWK...",
"...KWGGGGGWWK...",
"...KWWWWWWWWK...",
"...KWGGGGWWWK...",
"...KWWWWRRRWK...",
"...KWWWRWRWRK...",
"...KWWWWRRRWK...",
"...KWWWWWWWWK...",
"...KKKKKKKKKK...",
], top=2)

icon('chess', '象棋残局谱', [
".....KKKKKK.....",
"...KKYYYYYYKK...",
"..KYYRRRRRRYYK..",
".KYYRYYYYYYRYYK.",
".KYRYYYRRYYYRYK.",
".KYRYYRRRRYYRYK.",
".KYRYYYRRYYYRYK.",
".KYYRYYYYYYRYYK.",
".KOYYRRRRRRYYOK.",
"..KOOYYYYYYOOK..",
"...KKOOOOOOKK...",
".....KKKKKK.....",
], top=2)

icon('carkey', '老板车钥匙', [
"......KKKK......",
".....KDDDDK.....",
"....KDSSSSDK....",
"....KDSCCSDK....",
"....KDSSSSDK....",
"....KDDRRDDK....",
"....KDDDDDDK....",
".....KDDDDK.....",
"......KGGK......",
"......KGGK......",
".....KGGGGK.....",
"......KGGK......",
".......KK.......",
], top=2)

icon('headphones', '降噪耳机', [
".....KKKKKK.....",
"....KSSSSSSK....",
"...KSK....KSK...",
"..KSK......KSK..",
"..KSK......KSK..",
".KKSK......KSKK.",
"KDDDK......KDDDK",
"KDCDK......KDCDK",
"KDCDK......KDCDK",
"KDDDK......KDDDK",
".KKK........KKK.",
], top=2)

icon('tissue', '带薪如厕卷纸', [
"....KKKKKKK.....",
"...KWWWWWWWK....",
"..KWWWGGGWWWK...",
"..KWWGDDDGWWK...",
"..KWWGDDDGWWK...",
"..KWWWGGGWWWK...",
"...KWWWWWWWK....",
"....KKKKKKKWK...",
"..........KWK...",
"..........KWK...",
"..........KKK...",
], top=3)

icon('thermos', '老板同款保温杯', [
".....KKKKK......",
".....KGGGK......",
"....KKKKKKK.....",
"....KUCUUBK.....",
"....KUCUUBK.....",
"....KYYYYYK.....",
"....KUCUUBK.....",
"....KURURBK.....",
"....KUCRUBK.....",
"....KUCUUBK.....",
"....KUCUUBK.....",
"....KKKKKKK.....",
], top=2)

icon('luosifen', '螺蛳粉', [
".....L...L......",
"....L...L.......",
".....L...L......",
"................",
"..KKKKKKKKKKKK..",
".KOOYOOROOYOOOK.",
".KWWWWWWWWWWWWK.",
"..KWRWWWWWWRWK..",
"...KWWWWWWWWK...",
"....KKKKKKKK....",
".....KGGGGK.....",
".....KKKKKK.....",
], top=2)

icon('hardhat', '安全帽', [
"......KKKK......",
"....KKYYYYKK....",
"...KYWYYYYYOK...",
"..KYWYYYYYYYOK..",
"..KYYYYYYYYYOK..",
"..KYYYYYYYYYOK..",
"KKKKKKKKKKKKKKKK",
"KYYYYYYYYYYYYOOK",
"KKKKKKKKKKKKKKKK",
], top=4)

icon('mint', '薄荷糖', [
"......KKKK......",
".KK..KAWAAK..KK.",
".KAKKAWAAAAKKAK.",
".KAAKAAAAAAKAAK.",
".KAKKAAAATAKKAK.",
".KK..KATTTK..KK.",
"......KKKK......",
], top=5)

icon('umbrella', '雨伞', [
"......KKKK......",
"....KKRRRRKK....",
"...KRRRRRRRRK...",
"..KRWRRRRRRRRK..",
".KRRRRRRRRRRRRK.",
".KKKKKKKKKKKKKK.",
".......G........",
".......G........",
".......G........",
".......G........",
".....G.G........",
"......G.........",
], top=2)

icon('helmet', '外卖头盔', [
".....KKKKK......",
"...KKYYYYYKK....",
"..KYYWYYYYYYK...",
".KYYWYYYYYYYYK..",
".KYYYYYYKKKKKK..",
".KYYYYYKCCCCCK..",
".KYYYYYKCACCCK..",
".KYYYYYYKKKKKK..",
"..KOOOOOOOOOK...",
"...KKKKKKKKK....",
], top=3)

icon('invite', '会议邀请（诅咒）', [
"..P..........P..",
"..KKKKKKKKKKKK..",
"..KWKWWWWWWKWK..",
"..KWWKWWWWKWWK..",
"..KWWWKWWKWWWK..",
"..KWWWWKKWWWWK..",
"..KWWWWWWWWWWK..",
"..KWWWWWWWPPWK..",
"..KKKKKKKKKKKK..",
".P............P.",
], top=3)

icon('notebook', '假装开会笔记本', [
"..KKKKKKKKK.....",
"..KDUUUUUUK.....",
"..KDUWWWWUK.....",
"..KDUUUUUUK...K.",
"..KDUUUUUUK..KYK",
"..KDUUUUUUK.KYK.",
"..KDUUUUUUKKYK..",
"..KDUUUUUUKYK...",
"..KDUUUUUUKK....",
"..KDUUUUUUK.....",
"..KKKKKKKKK.....",
], top=2)

def render(rows):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.':
                im.putpixel((x, y), Image.new('RGB', (1, 1), PAL[c]).getpixel((0, 0)) + (255,))
    return im

os.makedirs(os.path.join(HERE, 'png'), exist_ok=True)  # 输出到 tools/out/
keys = list(ICONS)
COLS, PAD = 6, 2
rows_n = (len(keys) + COLS - 1) // COLS
sheet = Image.new('RGBA', (COLS * (16 + PAD), rows_n * (16 + PAD)), (0, 0, 0, 0))
for i, k in enumerate(keys):
    im = render(ICONS[k][1])
    im.save(os.path.join(HERE, 'png', f'{k}.png'))
    sheet.paste(im, ((i % COLS) * (16 + PAD) + 1, (i // COLS) * (16 + PAD) + 1))
sheet.save(os.path.join(HERE, 'items_sheet_1x.png'))

# 带中文标签的预览卡（给 KK 看）
S = 6
FONT = os.environ.get('ICON_FONT', 'zpix.ttf')  # 中文像素字体 Zpix: github.com/SolidZORO/zpix-pixel-font
try:
    font = ImageFont.truetype(FONT, 12)
except OSError:
    font = ImageFont.load_default()
cw, ch = 16 * S + 40, 16 * S + 40
card = Image.new('RGB', (COLS * cw + 20, rows_n * ch + 20), '#1a1c2c')
d = ImageDraw.Draw(card)
for i, k in enumerate(keys):
    cx, cy = 10 + (i % COLS) * cw, 10 + (i // COLS) * ch
    d.rectangle([cx + 4, cy + 2, cx + cw - 4, cy + ch - 4], fill='#333c57')
    im = render(ICONS[k][1]).resize((16 * S, 16 * S), Image.NEAREST)
    card.paste(im, (cx + (cw - 16 * S) // 2, cy + 6), im)
    name = ICONS[k][0]
    tw = d.textlength(name, font=font)
    d.text((int(cx + (cw - tw) / 2), cy + 16 * S + 12), name, fill='#f4f4f4', font=font)
card.save(os.path.join(HERE, 'items_preview.png'))
print(len(keys), 'icons')
