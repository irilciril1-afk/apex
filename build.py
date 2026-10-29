import base64, json, re
nb = " "
def fmt(n): return f"{n:,}".replace(",", nb) + nb + "₽"
BODY = {"suv": "внедорожник", "sedan": "седан", "coupe": "купе"}
CARS = [
 dict(id="lexus-rx", name="Lexus RX 350", body="suv", cond="used", km=12000, price=6990000, engine="3.5 л, бензин", power=249, drive="полный", gear="автомат",
  alt="Белый Lexus RX на лесной дороге",
  blurb="Спокойный семейный внедорожник с небольшим пробегом.",
  about="RX мягко едет по плохому асфальту, в салоне тихо, багажник вместительный. Пробег 12 000 км, обслуживалась по регламенту. Из тех машин, которые просто работают годами.",
  note="Белый цвет в жизни ещё лучше. Приезжайте днём, пока светло."),
 dict(id="audi-q8", name="Audi Q8 55 TFSI", body="suv", cond="new", km=0, price=9480000, engine="3.0 л, бензин", power=340, drive="полный", gear="автомат",
  alt="Белый Audi Q8 у современного дома",
  blurb="Большой кроссовер с тихим салоном. Для семьи, которая много ездит по трассе.",
  about="Спокойный и просторный Q8 одинаково уверенно чувствует себя в городе и на длинной дороге. Мягкая подвеска, хорошая шумоизоляция, много места сзади. Перед продажей прошёл проверку по 87 пунктам.",
  note="Сзади действительно просторно. Возьмите с собой всю семью и проверьте."),
 dict(id="bmw-m4", name="BMW M4 Competition", body="coupe", cond="new", km=0, price=11250000, engine="3.0 л, бензин", power=510, drive="задний", gear="автомат",
  alt="Серый BMW M4 на белом фоне",
  blurb="Купе для тех, кто любит водить. 510 сил и задний привод.",
  about="Машина для дороги с поворотами. Руль отзывчивый, мотор тянет с самых низов, тормоза не устают. В городе M4 остаётся удобной: подвеска достаточно мягкая для ежедневных поездок.",
  note="Попробуйте её на трассе, а не только вокруг салона."),
 dict(id="mercedes-e300", name="Mercedes-Benz E300", body="sedan", cond="new", km=0, price=8120000, engine="2.0 л, бензин", power=258, drive="задний", gear="автомат",
  alt="Чёрный Mercedes-Benz E-класса у светлой ограды",
  blurb="Бизнес-седан: тихий, мягкий, без лишней демонстративности.",
  about="Е-класс остаётся эталоном комфорта среди седанов. Ровный ход, тихий салон, удобные кресла на длинной дороге. Подходит и для работы, и для семьи.",
  note="Чёрный глянец любит чистоту. Мы моем машины перед каждым показом."),
 dict(id="porsche-macan", name="Porsche Macan S", body="suv", cond="used", km=8400, price=9950000, engine="2.9 л, бензин", power=380, drive="полный", gear="автомат",
  alt="Серый Porsche Macan на белом фоне",
  blurb="Компактный кроссовер с настоящим характером Porsche.",
  about="Macan едет как спортивная машина и помещается в обычный гараж. Быстрый разгон, точный руль, при этом хватает места для багажа и пассажиров. Пробег всего 8 400 км.",
  note="Меньше всего пробег среди машин с пробегом в нашем каталоге."),
 dict(id="audi-a6", name="Audi A6 45 TFSI", body="sedan", cond="used", km=18000, price=6340000, engine="2.0 л, бензин", power=245, drive="полный", gear="автомат",
  alt="Тёмно-серый Audi A6 с чёрными дисками у гаража",
  blurb="Строгий седан для города и трассы, полный привод.",
  about="A6 подходит для каждого дня. Полный привод уверенно держит дорогу зимой, шумоизоляция хорошая, багажник большой. Тёмно-серый цвет с чёрными дисками выглядит строго.",
  note="Посмотрите на неё при дневном свете: серый здесь глубже, чем на фото."),
 dict(id="bmw-x5", name="BMW X5 xDrive40i", body="suv", cond="new", km=0, price=10890000, engine="3.0 л, бензин", power=340, drive="полный", gear="автомат",
  alt="Белый BMW X5 на горной дороге",
  blurb="Большой внедорожник, уверенный и в городе, и на длинной дороге.",
  about="X5 соединяет размеры и динамику. Рядная шестёрка разгоняет её бодро, подвеска справляется и с плохими дорогами. Салон просторный, багажник вместительный.",
  note="Можно взять на тест-драйв на выходные, договоримся заранее."),
 dict(id="lexus-is", name="Lexus IS 300", body="sedan", cond="used", km=31000, price=4750000, engine="2.0 л, бензин", power=241, drive="задний", gear="автомат",
  alt="Чёрный Lexus IS на горной дороге",
  blurb="Компактный седан с задним приводом и характером.",
  about="Небольшой седан, в котором приятно ездить каждый день. Руль точный, посадка низкая, салон собран плотно. Подойдёт тому, кому важна управляемость и не нужен огромный кузов.",
  note="Если сдаёте свою машину в trade-in, цена может быть ниже."),
 dict(id="lexus-nx", name="Lexus NX 350", body="suv", cond="new", km=0, price=5480000, engine="2.4 л, бензин", power=279, drive="полный", gear="автомат",
  alt="Серый Lexus NX на белом фоне",
  blurb="Городской кроссовер: компактный, тихий, удобный каждый день.",
  about="NX легко паркуется и при этом достаточно просторный для семьи. Салон собран аккуратно, ход мягкий. Хороший вариант, если вы впервые берёте машину такого класса.",
  note="Первый Lexus? Начните с NX, он простой и понятный."),
 dict(id="volvo-s80", name="Volvo S80 V8", body="sedan", cond="used", km=61000, price=3450000, engine="4.4 л V8, бензин", power=315, drive="полный", gear="автомат",
  alt="Чёрный Volvo S80 на брусчатке вечером",
  blurb="Редкий седан с V8 и шведской основательностью.",
  about="S80 с восьмицилиндровым мотором встречается нечасто. Едет плавно и уверенно, а салон остался удобным и спустя годы. Хороший выбор, если нужен большой седан за разумные деньги.",
  note="Звук мотора лучше услышать самому. Приезжайте послушать."),
]
STUDIO = {"bmw-m4", "porsche-macan", "lexus-nx"}
def b64(path): return "data:image/jpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()
cards = []
for i, c in enumerate(CARS):
    c["bodyName"] = BODY[c["body"]]
    cond = "Новый" if c["cond"] == "new" else f"С пробегом {c['km']:,}".replace(",", nb) + nb + "км"
    meta = f"{cond}, {c['engine']}, {c['power']} л.с., {c['drive']} привод, {c['gear']}"
    cards.append(f'''<li class="row" data-id="{c['id']}" data-body="{c['body']}" data-cond="{c['cond']}" data-price="{c['price']}">
<a class="row-link" href="#{c['id']}"><figure class="row-photo"><img alt="" width="960" height="720"><span class="tag"><b>{fmt(c['price'])}</b></span></figure><span class="row-name">{c['name']}</span><span class="row-price">{fmt(c['price'])}</span><span class="row-meta">{meta}</span></a>
</li>''')
imgs = json.dumps({c["id"]: b64("img/" + c["id"] + ".jpg") for c in CARS})
opts = "".join(f'<option value="{c["id"]}">{c["name"]}</option>' for c in CARS)
data = json.dumps(CARS, ensure_ascii=False)
q8 = next(c for c in CARS if c["id"] == "audi-q8")
src = open("src.html", encoding="utf-8").read()
out = (src.replace("{{ROWS}}", "\n".join(cards)).replace("{{IMGS}}", imgs).replace("{{CAR_OPTIONS}}", opts).replace("{{DATA}}", data)
          .replace("{{HERO_PRICE}}", fmt(q8["price"])))
assert "{{" not in out, re.findall(r"\{\{[^}]+\}\}", out)
open("dist/fragment.html", "w", encoding="utf-8").write(out)
wrapper = '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + out + '</body></html>'
open("test.html", "w", encoding="utf-8").write(wrapper)
print(len(out) // 1024, "KB")
