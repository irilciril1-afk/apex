from PIL import Image, ImageFilter, ImageChops
import os
U = "/mnt/user-data/uploads/"
src = {
 "audi-q8": ("47076758602269128.jpg", .52),
 "bmw-m4": ("CARS___BMW_M4.jpg", .5),
 "lexus-rx": ("Лексус_RX.jpg", .5),
 "lexus-is": ("89931323804876638.jpg", .72),
 "volvo-s80": ("Volvo_S80_V8.jpg", .88),
 "mercedes-e300": ("132574782777390151.jpg", .45),
 "porsche-macan": ("2018_Porsche_Macan_Review.jpg", .5),
 "audi-a6": ("Audi_A_series.jpg", .55),
 "bmw-x5": ("Der_brandneue_BMW_X5_MotorTrend_der_4__Generation_2019_auf_Instagram___Der_xDrive40i___._Ch___", .4),
 "lexus-nx": ("Lexus_NX_350h.jpg", .5),
}
def crop(im, ratio, focus):
    w, h = im.size
    if w / h > ratio:
        nw = h * ratio; l = (w - nw) / 2
        return im.crop((int(l), 0, int(l + nw), h))
    nh = w / ratio; t = (h - nh) * focus
    return im.crop((0, int(t), w, int(t + nh)))
for key, (f, focus) in src.items():
    im = Image.open(U + f).convert("RGB")
    if key == "audi-a6":
        # blur another dealer's name on the front plate
        box = (95, 410, 220, 470)
        reg = im.crop(box).filter(ImageFilter.GaussianBlur(7))
        im.paste(reg, box)
    out = crop(im, 4/3, focus).resize((960, 720), Image.LANCZOS)
    if key in ("bmw-m4", "porsche-macan", "lexus-nx"):
        out = ImageChops.multiply(out, Image.new("RGB", out.size, (214, 222, 215)))
    out.save(f"img/{key}.jpg", "JPEG", quality=74, optimize=True, progressive=True)
hero = Image.open(U + "47076758602269128.jpg").convert("RGB")
crop(hero, 4/5, .55).resize((720, 900), Image.LANCZOS).save("img/hero.jpg", "JPEG", quality=78, optimize=True, progressive=True)
for f in sorted(os.listdir("img")): print(f, os.path.getsize("img/"+f))
