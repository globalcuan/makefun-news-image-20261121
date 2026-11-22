from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = '#f6f1e5'
INK = '#14181f'
RED = '#b3202c'
NAVY = '#1d3557'
TEAL = '#14666b'
GREEN = '#2e6b34'
SAND = '#c9a86a'
ORANGE = '#e07b24'
im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)

FONT_SERIF = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
FONT_SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FALLBACK = {
    FONT_SERIF: '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    FONT_SANS_B: '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    FONT_SANS: '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
}
def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(FALLBACK[path], size)

def wrap(text, f, maxw):
    words = text.split()
    lines, line = [], ''
    for word in words:
        trial = word if not line else line + ' ' + word
        if d.textlength(trial, font=f) <= maxw:
            line = trial
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def draw_wrapped(text, xy, f, fill, maxw, leading=None, max_lines=None):
    x, y = xy
    lines = wrap(text, f, maxw)
    if max_lines: lines = lines[:max_lines]
    leading = leading or int(f.size * 1.15)
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y

def centered(text, y, f, fill):
    d.text(((W-d.textlength(text, font=f))/2, y), text, font=f, fill=fill)

def rule(y, x1=28, x2=996, fill=INK, width=2):
    d.line((x1,y,x2,y), fill=fill, width=width)

# Masthead
rule(10, 22, 1002, RED, 4)
centered('THE WORLD IN ONE DAY', 16, font(FONT_SERIF, 62), INK)
d.rectangle((0, 91, W, 133), fill=RED)
centered('SATURDAY, 21 NOVEMBER 2026', 96, font(FONT_SANS_B, 29), PAPER)
rule(141, 22, 1002, INK, 2)
rule(146, 22, 1002, INK, 1)

# Lead illustration
px, py, pw, ph = 28, 160, 300, 300
d.rectangle((px,py,px+pw,py+ph), fill=NAVY)
# stylized dusk glow
for cx,cy,r in [(82,208,2),(220,182,2),(270,229,2),(160,192,2),(49,263,2)]:
    d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=PAPER)
# Three arcing incoming trails and starbursts
trails = [((46,174),(95,190),(136,229)), ((129,164),(164,186),(197,218)), ((218,169),(235,188),(254,211))]
for a,b,c in trails:
    d.arc((min(a[0],c[0])-8, min(a[1],c[1])-8, max(a[0],c[0])+8, max(a[1],c[1])+24), 5, 135, fill='#ffd18a', width=4)
    d.line((a,b,c), fill='#ffd18a', width=3)
    hx,hy=a
    d.ellipse((hx-3,hy-3,hx+3,hy+3), fill='#ffe0a8')
    ex,ey=c
    d.line((ex-7,ey,ex+7,ey), fill=ORANGE, width=3)
    d.line((ex,ey-7,ex,ey+7), fill=ORANGE, width=3)
    d.line((ex-5,ey-5,ex+5,ey+5), fill=ORANGE, width=2)
    d.line((ex-5,ey+5,ex+5,ey-5), fill=ORANGE, width=2)
# smoke puffs
for x,y,r in [(72,329,12),(88,316,14),(101,329,11),(217,319,13),(231,305,11),(244,320,12)]:
    d.ellipse((x-r,y-r,x+r,y+r), fill='#858b90')
# industrial shoreline
shore = [(px,346),(px+22,340),(px+50,344),(px+77,337),(px+105,343),(px+139,338),(px+170,344),(px+199,339),(px+232,345),(px+270,338),(px+300,343),(px+300,430),(px,430)]
d.polygon(shore, fill='#10151a')
# Two additional impact bursts on shoreline targets
for cx,cy in [(111,348),(181,349)]:
    for ang in range(0,360,45):
        ex=cx+int(math.cos(math.radians(ang))*7); ey=cy+int(math.sin(math.radians(ang))*7)
        d.line((cx,cy,ex,ey),fill=ORANGE,width=2)
    d.ellipse((cx-2,cy-2,cx+2,cy+2),fill='#ffd18a')
# plant blocks, chimneys
for box in [(58,310,111,362),(107,322,153,364),(202,315,256,362)]: d.rectangle(box, fill='#20262b')
d.rectangle((68,277,79,342), fill='#20262b'); d.rectangle((132,288,143,347), fill='#20262b')
# flames
for x,y in [(77,328),(123,340),(226,337)]:
    d.polygon([(x-12,y+20),(x-7,y+1),(x-2,y+10),(x+5,y-7),(x+9,y+6),(x+14,y+20)], fill=ORANGE)
    d.polygon([(x-6,y+19),(x-2,y+8),(x+2,y+13),(x+6,y+3),(x+9,y+19)], fill='#ffd17c')
# sea strip and tanker
d.rectangle((px,421,px+pw,py+ph), fill=TEAL)
d.polygon([(42,438),(101,438),(113,431),(157,431),(157,438),(176,438),(165,449),(58,449)], fill='#10151a')
d.rectangle((80,426,103,438), fill='#10151a')
d.line((145,431,151,410), fill='#10151a', width=2); d.line((151,410,160,418), fill='#10151a', width=2)
d.line((28,455,328,455), fill=SAND, width=2)

# Lead text
lx=350
kicker=font(FONT_SANS_B, 21)
serif=font(FONT_SERIF, 43)
body=font(FONT_SANS, 21)
d.text((lx,164),'MIDDLE EAST ESCALATION',font=kicker,fill=RED)
lead_head='IRAN STRIKES US BASES IN BAHRAIN'
y=draw_wrapped(lead_head,(lx,194),serif,INK,646,leading=47,max_lines=3)
lead_sub="Revolutionary Guards hit two American positions as Bahrain reports a fire at a civilian industrial site; tankers are struck near the Strait of Hormuz"
draw_wrapped(lead_sub,(lx,y+6),body,INK,646,leading=25,max_lines=4)
rule(477,28,996,INK,2)

# Grid story panels
stories = [
 (28,493,474,175,'a'), (522,493,474,175,'b'),
 (28,680,474,175,'c'), (522,680,474,175,'d')]
for x,y,w,h,key in stories:
    d.rectangle((x,y,x+w,y+h), outline=INK, width=1)
    ix,iy=x+10,y+12
    iw,ih=92,92
    if key=='a':
        d.rectangle((ix,iy,ix+iw,iy+ih),fill=NAVY)
        # Centered Polish flag: white above red, outlined in ink
        flag=(ix+15,iy+25,ix+77,iy+67)
        d.rectangle(flag,fill=PAPER)
        d.rectangle((flag[0],iy+46,flag[2],flag[3]),fill=RED)
        d.rectangle(flag,outline=INK,width=1)
        # small starburst
        cx,cy=ix+79,iy+22
        for ang in range(0,360,45):
            rad=11
            ex=cx+int(math.cos(math.radians(ang))*rad); ey=cy+int(math.sin(math.radians(ang))*rad)
            d.line((cx,cy,ex,ey),fill=ORANGE,width=2)
        d.ellipse((cx-3,cy-3,cx+3,cy+3),fill=ORANGE)
        kicker_text='NATO FRONTIER'; head='RUSSIAN MISSILES LAND IN POLAND'
        sub="Warsaw calls it a deliberate provocation during NATO drills; a ballistic missile kills two in Kryvyi Rih, Zelensky's hometown"
    elif key=='b':
        d.rectangle((ix,iy,ix+iw,iy+ih),fill=INK)
        for gx in range(ix+15,ix+iw,20): d.line((gx,iy+8,gx,iy+ih-8),fill='#41454a',width=1)
        for gy in range(iy+12,iy+ih,20): d.line((ix+8,gy,ix+iw-8,gy),fill='#41454a',width=1)
        pts=[(ix+12,iy+20),(ix+32,iy+27),(ix+48,iy+38),(ix+64,iy+53),(ix+80,iy+76)]
        d.line(pts,fill=RED,width=5)
        for a,bp in zip(pts,pts[1:]):
            d.line((a[0],a[1],bp[0],bp[1]),fill=RED,width=5)
        kicker_text='MARKETS'; head='AI SELLOFF TIPS STOCKS INTO CORRECTION'
        sub="The Nasdaq erases its 2026 gains in tech's worst week since 2020, even as Anthropic's record $2 trillion IPO stuns Wall Street"
    elif key=='c':
        d.rectangle((ix,iy,ix+iw,iy+ih),fill=NAVY)
        # three small flags
        fy=iy+24
        for fx,fw in [(ix+7,22),(ix+35,22),(ix+63,22)]:
            d.line((fx-2,fy-7,fx-2,fy+53),fill=INK,width=1)
        fx=ix+7
        d.rectangle((fx,fy,fx+22,fy+42),fill=RED)
        d.ellipse((fx+4,fy+5,fx+8,fy+9),fill='#f5d547')
        fx2=ix+35
        d.rectangle((fx2,fy,fx2+22,fy+42),fill=PAPER)
        for sy in range(fy,fy+42,8): d.rectangle((fx2,sy,fx2+22,sy+4),fill=RED)
        d.rectangle((fx2,fy,fx2+10,fy+19),fill=NAVY)
        fx3=ix+63
        d.rectangle((fx3,fy,fx3+22,fy+42),fill=PAPER)
        d.rectangle((fx3,fy+14,fx3+22,fy+28),fill=NAVY)
        d.rectangle((fx3,fy+28,fx3+22,fy+42),fill=RED)
        kicker_text='APEC SUMMIT'; head='TRUMP, XI, PUTIN MEET IN SHENZHEN'
        sub='The three leaders hold their first trilateral summit and sign a peace declaration that says nothing about Ukraine'
    else:
        d.rectangle((ix,iy,ix+iw,iy+ih),fill=TEAL)
        cx,cy=ix+46,iy+46
        d.ellipse((cx-29,cy-29,cx+29,cy+29),outline=PAPER,width=3)
        star=[]
        for j in range(10):
            ang=-math.pi/2+j*math.pi/5
            rad=20 if j%2==0 else 9
            star.append((cx+math.cos(ang)*rad,cy+math.sin(ang)*rad))
        d.polygon(star,fill=PAPER)
        kicker_text='MEXICO'; head="CARTEL BOSS 'CHAPO ISIDRO' CAPTURED"
        sub='Special forces seize the FBI most-wanted trafficker in Sinaloa; the gunfights and road blockades that follow leave at least 11 dead'
    tx=x+116; tw=w-126
    d.text((tx,y+8),kicker_text,font=font(FONT_SANS_B,17),fill=RED)
    hy=draw_wrapped(head,(tx,y+31),font(FONT_SERIF,25),INK,tw,leading=28,max_lines=2)
    draw_wrapped(sub,(tx,hy+2),font(FONT_SANS,17),INK,tw,leading=19,max_lines=4)

# Climate strip
rule(851,28,996,INK,2)
d.rectangle((28,858,104,922),fill=GREEN)
d.ellipse((43,867,89,913),fill=PAPER)
# simple globe land blobs
d.ellipse((50,876,68,890),fill=GREEN); d.ellipse((68,887,81,904),fill=GREEN); d.polygon([(57,892),(67,891),(64,904),(56,901)],fill=GREEN)
d.line((45,890,87,890),fill=GREEN,width=1)
d.ellipse((54,868,78,912),outline=GREEN,width=1)
cx=119
climhead='COP31 CLIMATE TALKS DEADLOCKED OVER FOSSIL FUELS'
d.text((cx,856),climhead,font=font(FONT_SERIF,25),fill=INK)
draw_wrapped('The Antalya summit runs into overtime without a deal as negotiators fight over the future of oil and gas',(cx,889),font(FONT_SANS,18),INK,877,leading=22,max_lines=2)
rule(923,28,996,INK,2)

# Ticker and footer
band_y=929
# ensure ticker text is enclosed with two lines inside 102 px band
d.rectangle((0,band_y,1024,1024),fill=INK)
ticker="ALSO ON SATURDAY: World Court finds Myanmar guilty of genocide against the Rohingya • GTA VI earns $3.8 billion on day one, the biggest entertainment launch ever • Earthquake shakes the Peruvian Andes • Harden scores 51 and passes Kobe Bryant"
ticker_font=font(FONT_SANS_B,16)
draw_wrapped(ticker,(28,band_y+6),ticker_font,PAPER,968,leading=19,max_lines=3)
# footer included in lower ticker area; contrasting paper footer plaque
# Reserve bottom 25 px for footer; ticker occupies top 33 px, wraps above.
d.rectangle((0,999,1024,1024),fill=PAPER)
centered('The world\'s news of Saturday 21 November 2026, summed up in one image',1001,font(FONT_SANS,14),INK)

im.save('entry.png',format='PNG',optimize=True)
