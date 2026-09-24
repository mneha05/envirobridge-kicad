from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("docs")
OUT.mkdir(exist_ok=True)
W, H = 900, 560

BG = (7, 12, 24, 255)
BOARD = (21, 88, 61, 255)
EDGE = (125, 211, 252, 255)
TEXT = (248, 250, 252, 255)
MUTED = (148, 163, 184, 255)
GREEN = (167, 243, 208, 255)
SDA = (253, 230, 138, 255)
SCL = (147, 197, 253, 255)

def font(size, bold=False):
    choices = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in choices:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def board_base():
    im = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((95, 80, 805, 450), radius=28, fill=BOARD, outline=EDGE, width=4)

    for x, y in [(135, 120), (765, 120), (135, 410), (765, 410)]:
        d.ellipse((x-16, y-16, x+16, y+16), fill=BG, outline=(209,213,219,255), width=5)

    for x, label, addr in [(200, "U1", "0x76"), (700, "U2", "0x77")]:
        d.rounded_rectangle((x-43, 210, x+43, 296), radius=10, fill=(31,41,55,255), outline=TEXT, width=3)
        d.text((x, 242), label, font=font(19, True), anchor="mm", fill=TEXT)
        d.text((x, 271), addr, font=font(14, True), anchor="mm", fill=GREEN)

    d.rounded_rectangle((365, 350, 535, 405), radius=10, fill=(31,41,55,255), outline=TEXT, width=3)
    d.text((450, 378), "J1 / J2 HOST", font=font(17, True), anchor="mm", fill=TEXT)

    d.line((243, 245, 657, 245), fill=SDA, width=6)
    d.line((243, 268, 657, 268), fill=SCL, width=6)
    d.line((450, 268, 450, 350), fill=SCL, width=6)
    d.line((470, 245, 470, 350), fill=SDA, width=6)

    d.text((450, 38), "ENVIROBRIDGE", font=font(34, True), anchor="mm", fill=TEXT)
    d.text((450, 493), "dual BME280  •  I²C  •  testable  •  configurable", font=font(16), anchor="mm", fill=MUTED)
    d.text((112, 260), "AIRFLOW", font=font(15, True), anchor="mm", fill=(103,232,249,255))
    d.text((788, 260), "AIRFLOW", font=font(15, True), anchor="mm", fill=(103,232,249,255))
    return im

def board_tour():
    steps = [
        ("DUAL SENSOR TOPOLOGY", (450, 255), "Two BME280s share one 3.3 V I²C bus", 260),
        ("ADDRESS SELECTION", (200, 254), "Independent 0x76 / 0x77 configuration", 84),
        ("HOST CONNECTIVITY", (450, 378), "JST-SH + 2.54 mm debug header", 115),
        ("TEST ACCESS", (450, 145), "3V3 · GND · SDA · SCL probe points", 135),
        ("AIRFLOW-AWARE PLACEMENT", (700, 254), "Sensors sit near opposite board edges", 92),
    ]
    frames = []
    for index, (title, (cx, cy), subtitle, radius) in enumerate(steps):
        for tick in range(5):
            im = board_base()
            d = ImageDraw.Draw(im, "RGBA")
            pulse = 1 + 0.08 * math.sin(tick / 5 * math.tau)
            r = int(radius * pulse)
            for pad, alpha in [(16, 45), (9, 80), (3, 200)]:
                d.ellipse((cx-r-pad, cy-r-pad, cx+r+pad, cy+r+pad), outline=(103,232,249,alpha), width=max(2,pad//4))
            d.rounded_rectangle((135, 505, 765, 552), radius=16, fill=(4,10,20,235), outline=(125,211,252,160), width=2)
            d.text((450, 520), f"{index+1}/5  {title}", font=font(15, True), anchor="mm", fill=TEXT)
            d.text((450, 541), subtitle, font=font(12), anchor="mm", fill=GREEN)
            frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=96))
    frames[0].save(OUT/"board-tour.gif", save_all=True, append_images=frames[1:], duration=120, loop=0, optimize=True, disposal=2)

def interpolate(points, s):
    lengths = []
    total = 0.0
    for a, b in zip(points, points[1:]):
        length = math.hypot(b[0]-a[0], b[1]-a[1])
        lengths.append(length)
        total += length
    distance = s * total
    for (a,b), length in zip(zip(points,points[1:]), lengths):
        if distance <= length:
            q = distance / length if length else 0
            return a[0] + (b[0]-a[0])*q, a[1] + (b[1]-a[1])*q
        distance -= length
    return points[-1]

def i2c_flow():
    left = [(450,378),(450,300),(450,268),(350,268),(250,268),(200,268)]
    right = [(450,378),(470,300),(470,245),(560,245),(650,245),(700,245)]
    frames=[]
    for tick in range(24):
        im = board_base()
        d = ImageDraw.Draw(im, "RGBA")
        target_left = tick < 12
        local = (tick % 12) / 11
        x,y = interpolate(left if target_left else right, local)
        for radius, alpha in [(17,40),(11,90),(6,230)]:
            d.ellipse((x-radius,y-radius,x+radius,y+radius), fill=(253,230,138,alpha))
        d.rounded_rectangle((x-21,y-11,x+21,y+11), radius=7, fill=(15,23,42,245), outline=SDA, width=2)
        d.text((x,y), "I²C", font=font(10, True), anchor="mm", fill=TEXT)
        addr = "U1 · 0x76" if target_left else "U2 · 0x77"
        d.rounded_rectangle((185, 505, 715, 552), radius=16, fill=(4,10,20,235))
        d.text((450, 521), f"HOST → {addr}", font=font(16, True), anchor="mm", fill=GREEN)
        d.text((450, 542), "shared SDA/SCL bus · independently addressed devices", font=font(12), anchor="mm", fill=MUTED)
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=96))
    frames[0].save(OUT/"i2c-flow.gif", save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True, disposal=2)

if __name__ == "__main__":
    board_tour()
    i2c_flow()
    print("generated docs/board-tour.gif and docs/i2c-flow.gif")
