# -*- coding: utf-8 -*-
"""Каталог ASIC-майнеров: раздел, бренды, карточки моделей.

Характеристики — только из подтверждённых источников: 17 моделей Bitmain взяты с текущих
карточек miningshop.ru, модели старого сайта — из описаний на самом старом сайте (архив).
Цен нет намеренно: они меняются ежедневно, на временном сайте их показывать нельзя.
"""
import json, os, re
from core import (add, u, esc, h2, h3, p, ul, ol, note, ptable, faq_html, faq_ld, cards, section, cta_box, toc, a, C)

HERE = os.path.dirname(__file__)
LEG = json.load(open(os.path.join(HERE, 'legacy.json'), encoding='utf-8'))

ALGO = {
    'SHA-256': {'coins': 'Bitcoin (BTC), а также Bitcoin Cash (BCH) и другие монеты на SHA-256', 'eff_unit': 'Дж/TH', 'div': 1},
    'Scrypt': {'coins': 'Litecoin (LTC) и Dogecoin (DOGE) — в пулах их добывают одновременно (merged mining)', 'eff_unit': 'Дж/MH', 'div': 1},
    'kHeavyHash': {'coins': 'Kaspa (KAS)', 'eff_unit': 'Дж/TH', 'div': 1},
    'Eaglesong': {'coins': 'Nervos Network (CKB)', 'eff_unit': 'Дж/TH', 'div': 1},
    'Etchash': {'coins': 'Ethereum Classic (ETC) и другие монеты на Etchash', 'eff_unit': 'Дж/MH', 'div': 1},
}

# name, brand, algo, hashrate, unit, watts, cooling, path, legacy_key, noise
M = []


def model(name, brand, algo, h, unit, w, cooling, path, leg=None, noise=None, live=False, extra=''):
    M.append(dict(name=name, brand=brand, algo=algo, h=h, unit=unit, w=w, cooling=cooling, path=path,
                  leg=leg, noise=noise, live=live, extra=extra))


BM = '/catalog/asic_maynery/bitmain/'
# ---- 17 моделей Bitmain с текущего сайта (адреса сохраняем) ----
model('Antminer S23 Hydro 580 TH/s', 'Bitmain', 'SHA-256', 580, 'TH/s', 5510, 'hydro', BM + 'antminer-s23-hydro-580th/', live=True)
model('Antminer S21 XP Hydro 473 TH/s', 'Bitmain', 'SHA-256', 473, 'TH/s', 5976, 'hydro', BM + 'antminer-s21-xp-hydro-473th/', live=True)
model('Antminer S21 Hydro 335 TH/s', 'Bitmain', 'SHA-256', 335, 'TH/s', 5360, 'hydro', BM + 'antminer-s21-hydro-335th/', live=True)
model('Antminer S21 XP 270 TH/s', 'Bitmain', 'SHA-256', 270, 'TH/s', 3645, 'air', BM + 'antminer-s21-xp-270th/', noise=75, live=True)
model('Antminer S21 Pro 234 TH/s', 'Bitmain', 'SHA-256', 234, 'TH/s', 3510, 'air', BM + 'antminer-s21-pro-234th/', noise=75, live=True)
model('Antminer S21+ 225 TH/s', 'Bitmain', 'SHA-256', 225, 'TH/s', 3150, 'air', BM + 'antminer-s21-plus-225th/', noise=75, live=True)
model('Antminer S21+ 216 TH/s', 'Bitmain', 'SHA-256', 216, 'TH/s', 3564, 'air', BM + 'antminer-s21-plus-216th/', live=True)
model('Antminer S21 200 TH/s', 'Bitmain', 'SHA-256', 200, 'TH/s', 3500, 'air', BM + 'antminer-s21-200th/', noise=75, live=True)
model('Antminer T21 190 TH/s', 'Bitmain', 'SHA-256', 190, 'TH/s', 3610, 'air', BM + 'antminer-t21-190th/', live=True)
model('Antminer S19 XP 141 TH/s', 'Bitmain', 'SHA-256', 141, 'TH/s', 3031, 'air', BM + 'antminer-s19-xp-141th/', leg=('live', 'antminer-s19-xp-141th'), live=True)
model('Antminer S19 Pro 110 TH/s', 'Bitmain', 'SHA-256', 110, 'TH/s', 3250, 'air', BM + 'antminer-s19-pro-110th/', leg=('live', 'antminer-s19-pro-110th'), live=True)
model('Antminer S19j Pro 104 TH/s', 'Bitmain', 'SHA-256', 104, 'TH/s', 3068, 'air', BM + 'antminer-s19j-pro-104th/', leg=('live', 'antminer-s19j-pro-104th'), live=True)
model('Antminer L9 17 GH/s', 'Bitmain', 'Scrypt', 17000, 'MH/s', 3360, 'air', BM + 'antminer-l9-17gh/', noise=75, live=True)
model('Antminer L9 16 GH/s', 'Bitmain', 'Scrypt', 16000, 'MH/s', 3360, 'air', BM + 'antminer-l9-16gh/', live=True)
model('Antminer L7 9500 MH/s', 'Bitmain', 'Scrypt', 9500, 'MH/s', 3425, 'air', BM + 'antminer-l7-9500mh/', leg=('live', 'antminer-l7-9500mh'), live=True)
model('Antminer KS3 9.4 TH/s', 'Bitmain', 'kHeavyHash', 9.4, 'TH/s', 3500, 'air', BM + 'antminer-ks3-9-4th/', live=True)
model('Antminer K7 63.5 TH/s', 'Bitmain', 'Eaglesong', 63.5, 'TH/s', 3080, 'air', BM + 'antminer-k7-63-5th/', live=True)
# ---- модели старого сайта: возвращаем по прежним адресам ----
model('Antminer S19k Pro 120 TH/s', 'Bitmain', 'SHA-256', 120, 'TH/s', 2760, 'air', '/catalog/asic_maynery/bitmain/bitmain_antminer_s19k_pro/', leg=('legacy', 'antminer-s19k-pro'))
model('Antminer S19 Pro+ Hyd 198 TH/s', 'Bitmain', 'SHA-256', 198, 'TH/s', 5445, 'hydro', '/catalog/asic_maynery/bitmain/bitmain_antminer_s19_pro_hyd/', leg=('legacy', 'antminer-s19-pro-hyd'))
model('Antminer E9 Pro 3680 MH/s', 'Bitmain', 'Etchash', 3680, 'MH/s', 2200, 'air', '/catalog/asic_maynery/bitmain/bitmain_antminer_e9/', leg=('legacy', 'antminer-e9-pro'))
model('Whatsminer M30S++ 112 TH/s', 'Whatsminer', 'SHA-256', 112, 'TH/s', 3472, 'air', '/catalog/asic_maynery/whatsminer/whatsminer_m30s_plus_plus/', leg=('legacy', 'whatsminer-m30s-plus-plus'))
model('Whatsminer M30S+ 102 TH/s', 'Whatsminer', 'SHA-256', 102, 'TH/s', 3400, 'air', '/catalog/asic_maynery/whatsminer/whatsminer_m30s_plus/', leg=('legacy', 'whatsminer-m30s-plus'))
model('Whatsminer M21S 56 TH/s', 'Whatsminer', 'SHA-256', 56, 'TH/s', 3360, 'air', '/catalog/asic_maynery/whatsminer/whatsminer_m21s/', leg=('legacy', 'whatsminer-m21s'))
model('Whatsminer M56', 'Whatsminer', 'SHA-256', None, 'TH/s', None, None, '/catalog/asic_maynery/whatsminer/whatsminer_m56/', leg=('legacy', 'whatsminer-m56'))
model('iPollo V1 Mini Classic Plus 280 MH/s', 'iPollo', 'Etchash', 280, 'MH/s', 270, 'air', '/catalog/asic_maynery/ipollo/ipollo_v1_mini_classic_plus_6g/', leg=('legacy', 'ipollo-v1-mini-classic-plus'))
model('Jasminer X16-Q 1950 MH/s', 'Jasminer', 'Etchash', 1950, 'MH/s', 620, 'air', '/catalog/asic_maynery/jasminer/jasminer_x16_q_1950mh/', leg=('legacy', 'jasminer-x16-q'))

BRANDS = [
    ('bitmain', 'Bitmain Antminer', 'Bitmain'),
    ('whatsminer', 'Whatsminer (MicroBT)', 'Whatsminer'),
    ('ipollo', 'iPollo', 'iPollo'),
    ('jasminer', 'Jasminer', 'Jasminer'),
]


def eff(m):
    if not (m['h'] and m['w']):
        return None
    if m['unit'] == 'TH/s':
        return m['w'] / m['h']
    return m['w'] / m['h']  # Дж/MH для MH/s


def hr(m):
    if m['h'] is None:
        return '—'
    v = m['h']
    if m['unit'] == 'MH/s' and v >= 1000:
        return ('%g GH/s' % (v / 1000)).replace('.', ',')
    return ('%g %s' % (v, m['unit'])).replace('.', ',')


def fmt_eff(m):
    e = eff(m)
    if e is None:
        return '—'
    return ('%.2f' % e if e < 5 else '%.1f' % e).replace('.', ',') + ' ' + ALGO[m['algo']]['eff_unit']


def photo(m):
    if m['leg']:
        g, k = m['leg']
        ph = LEG[g].get(k, {}).get('photos') or []
        if ph:
            return ph
    return []


def placeholder_svg(m):
    return ('assets/img/ui/asic-%s.svg' % ('hydro' if m['cooling'] == 'hydro' else 'air'))


def card(m):
    ph = photo(m)
    img = ph[0] if ph else placeholder_svg(m)
    tags = [m['algo'], 'Гидро' if m['cooling'] == 'hydro' else ('Воздух' if m['cooling'] == 'air' else '')]
    return ('<article class="prod" data-tags="%s %s %s"><a class="prod-img" href="%s"><img src="%s" alt="%s" loading="lazy"></a>'
            '<div class="prod-body"><div class="tags"><span class="tag tag-accent">%s</span>%s</div>'
            '<h3><a href="%s">%s %s</a></h3>'
            '<div class="specs-mini"><span>Хешрейт</span><b>%s</b><span>Потребление</span><b>%s</b><span>Эффективность</span><b>%s</b></div>'
            '<a class="btn btn-line" href="%s">Подробнее и расчёт</a></div></article>'
            % (m['brand'].lower(), m['algo'], m['cooling'] or '', u(m['path']), u('/' + img), esc(m['brand'] + ' ' + m['name']),
               m['algo'], ''.join('<span class="tag">%s</span>' % t for t in tags[1:] if t),
               u(m['path']), m['brand'], m['name'], hr(m), ('%d Вт' % m['w']) if m['w'] else '—', fmt_eff(m), u(m['path'])))


def grid(models):
    return '<div class="grid g4" id="asic-grid">%s</div>' % ''.join(card(m) for m in models)


def chips(models):
    algos = sorted({m['algo'] for m in models}, key=lambda x: ['SHA-256', 'Scrypt', 'kHeavyHash', 'Etchash', 'Eaglesong'].index(x))
    ch = ['<button class="chip" data-value="all" aria-pressed="true">Все</button>']
    ch += ['<button class="chip" data-value="%s" aria-pressed="false">%s</button>' % (x, x) for x in algos]
    ch += ['<button class="chip" data-value="hydro" aria-pressed="false">Гидроохлаждение</button>']
    return '<div class="chips" data-filter-group="#asic-grid">%s</div>' % ''.join(ch)


# ================================================================ раздел ASIC
asic_faq = [
    ('Какой асик выбрать в 2026 году?',
     'Решает не хешрейт, а энергоэффективность и ваш тариф на электричество. При тарифе выше 5 ₽/кВт·ч имеет смысл '
     'смотреть на модели с эффективностью 15 Дж/TH и лучше — S21 XP, S21 Pro, S21+ 225T, гидроверсии. При дешёвом '
     'электричестве окупаются и более старые S19-й серии. Точный ответ даёт расчёт на вашем тарифе — '
     'его можно сделать в <a href="%s">калькуляторе доходности</a>.' % u('/table/')),
    ('Чем гидроасики отличаются от обычных?',
     'Модели Hydro охлаждаются жидкостью через теплообменник, а не вентиляторами. Они тише, выдерживают большую '
     'плотность размещения и позволяют использовать тепло, но требуют контура с насосом и драйкулером. '
     'Дома без инженерной подготовки их не запустить.'),
    ('Можно ли держать асик дома?',
     'Воздушный асик потребляет 3–3,6 кВт и шумит на уровне 75 дБ. Дома нужна отдельная линия питания, '
     'отвод горячего воздуха и шумоизоляция — обычно шумобокс. Разбор всех вариантов — в статье '
     '<a href="%s">про шумобоксы</a>.' % u('/knowledge/maintenance/shumoboks-dlya-asika/')),
    ('Почему на сайте нет цен?',
     'Цены на асики меняются вслед за курсом биткоина и наличием у поставщиков буквально ежедневно. '
     'Мы называем цену в момент запроса и фиксируем её в счёте — так честнее, чем устаревшая цифра на сайте.'),
    ('Какую монету можно добывать на асике?',
     'Каждый асик работает только на одном алгоритме. SHA-256 — биткоин, Scrypt — Litecoin и Dogecoin, '
     'kHeavyHash — Kaspa, Etchash — Ethereum Classic. Эфир (ETH) асиками больше не добывается: в 2022 году сеть '
     'перешла на Proof-of-Stake.'),
]

asic_body = (
    section(chips(M) + grid(M), cls='sec-soft', title='Модели в каталоге',
            sub='Характеристики — паспортные значения производителя. Реальный хешрейт зависит от прошивки, температуры '
                'воздуха и качества питания. Цену и наличие сообщаем в момент запроса.')
    + section('<div class="layout"><div class="prose">'
              + h2('Как выбрать ASIC-майнер', 'kak-vybrat')
              + p('Асик — специализированный вычислитель под один алгоритм. Выбор начинается не с модели, а с трёх '
                  'цифр: сколько киловатт вы можете подвести, по какому тарифу и куда уйдёт тепло. Эти ограничения '
                  'отсекают большую часть вариантов ещё до разговора о хешрейте.')
              + h3('1. Энергоэффективность важнее хешрейта')
              + p('Эффективность в джоулях на терахеш показывает, сколько электричества уходит на единицу работы. '
                  'Два асика с одинаковым хешрейтом могут отличаться по счёту за свет в полтора раза. '
                  'При тарифе 5–7 ₽/кВт·ч разница в 5 Дж/TH — это разница между окупаемым и убыточным устройством.')
              + ptable(['Поколение', 'Эффективность', 'Когда оправдано'],
                       [['S23 Hydro, S21 XP Hydro', '9,5–12,6 Дж/TH', 'промышленные площадки с жидкостным охлаждением'],
                        ['S21 XP, S21 Pro, S21+ 225T', '13,5–15 Дж/TH', 'любой тариф, лучший выбор для воздуха'],
                        ['S21, T21, S21+ 216T', '16,5–19 Дж/TH', 'тариф до 5–6 ₽/кВт·ч'],
                        ['S19 XP, S19k Pro', '21,5–23 Дж/TH', 'дешёвое электричество, до 4 ₽/кВт·ч'],
                        ['S19 Pro, S19j Pro, M30S+', '29,5–33 Дж/TH', 'только очень дешёвая энергия']])
              + h3('2. Охлаждение: воздух или жидкость')
              + p('Воздушные модели ставятся где угодно, где можно организовать приток холодного и отвод горячего '
                  'воздуха. Гидромодели (Hydro, Hyd) плотнее и тише, но требуют контура охлаждения. '
                  'Если такого контура нет — выбирайте воздух.')
              + h3('3. Алгоритм и монета')
              + p('Большая часть рынка — SHA-256 и биткоин: это самая ликвидная монета и самая предсказуемая экономика. '
                  'Scrypt (L7, L9) даёт диверсификацию за счёт Litecoin и Dogecoin. Kaspa и Etchash — более волатильные '
                  'сети, где сложность меняется быстрее.')
              + h3('4. Где будет стоять асик')
              + p('Дома — только одиночные устройства со шумоизоляцией и отдельной линией. Для двух и более '
                  'устройств обычно выгоднее ' + a('/services/hosting/', 'хостинг в дата-центре') + ': промышленный '
                  'тариф, охлаждение и обслуживание включены.')
              + note('Проверьте расчёт до покупки',
                     'Посчитайте доходность на своём тарифе в ' + a('/table/', 'калькуляторе') + ' — он показывает '
                     'окупаемость и тариф, при котором устройство выходит в ноль.')
              + h2('Частые вопросы', 'faq') + '</div>'
              + '<aside class="aside">' + cta_box('Подберём асик под ваш тариф',
                                                  'Скажите мощность, тариф и бюджет — предложим 2–3 модели с расчётом окупаемости.',
                                                  '/#podbor', 'Подобрать') + '</aside></div>'
              + faq_html(asic_faq))
)

add(path='/catalog/asic_maynery/', kind='catalog',
    title='ASIC-майнеры купить в Москве: Antminer S21, Whatsminer — каталог MiningShop',
    description='Каталог ASIC-майнеров: Bitmain Antminer S21, S21 XP, S21 Hydro, S19, L9, Whatsminer M30S++. '
                'Характеристики, энергоэффективность, расчёт доходности, доставка по России.',
    h1='ASIC-майнеры', lead='Асики для биткоина, Litecoin/Dogecoin, Kaspa и Ethereum Classic. Подберём модель под ваш тариф, '
                              'посчитаем окупаемость, доставим и настроим.',
    crumbs=[('Каталог', '/catalog/'), ('ASIC-майнеры', '/catalog/asic_maynery/')],
    body=asic_body, ld=[faq_ld(asic_faq), {"@type": "CollectionPage", "name": "ASIC-майнеры", "url": "https://miningshop.ru/catalog/asic_maynery/"}])

# ================================================================ бренды
BRAND_TEXT = {
    'bitmain': ('Bitmain — крупнейший производитель асиков. Линейка Antminer S21 — текущее поколение для биткоина: от S21 '
                '200 TH/s до гидроверсий S21 XP Hydro и S23 Hydro. Для Litecoin и Dogecoin — Antminer L7 и L9, для Kaspa — KS3.',
                'Асики Bitmain Antminer купить: S21, S21 XP, S21 Hydro, L9 — MiningShop'),
    'whatsminer': ('Whatsminer — бренд китайской компании MicroBT, второго по величине производителя асиков для биткоина. '
                   'Устройства славятся стабильностью блоков питания и ремонтопригодностью. На сайте — модели, которые '
                   'продавались у нас и до сих пор работают в парках клиентов.',
                   'Асики Whatsminer купить: M30S++, M30S+, M21S — MiningShop'),
    'ipollo': ('iPollo делает компактные тихие асики серии Mini — единственный класс майнеров, который реально можно '
               'поставить в квартире без шумобокса.', 'Асики iPollo V1 Mini — MiningShop'),
    'jasminer': ('Jasminer выпускает энергоэффективные асики для Etchash (Ethereum Classic) с низким потреблением.',
                 'Асики Jasminer X16-Q — MiningShop'),
}
for key, label, brand in BRANDS:
    models = [m for m in M if m['brand'] == brand]
    txt, title = BRAND_TEXT[key]
    add(path='/catalog/asic_maynery/%s/' % key, kind='catalog', title=title,
        description=('%s: модели, характеристики, энергоэффективность и расчёт доходности. Доставка по России, '
                     'настройка и гарантия.' % label),
        h1='Асики %s' % label, lead=txt,
        crumbs=[('Каталог', '/catalog/'), ('ASIC-майнеры', '/catalog/asic_maynery/'), (label, '/catalog/asic_maynery/%s/' % key)],
        body=section(grid(models), cls='sec-soft', title='Модели %s' % label,
                     sub='Паспортные характеристики. Цена и наличие — по запросу.')
        + section(cards([
            ('calc', 'Расчёт окупаемости', 'Посчитайте доход и срок окупаемости на своём тарифе.', '/table/'),
            ('server', 'Размещение в дата-центре', 'Промышленный тариф и обслуживание вместо шума дома.', '/services/hosting/'),
            ('wrench', 'Ремонт и диагностика', 'Хешплаты, блоки питания, вентиляторы, прошивки.', '/services/remont-oborudovaniya/')], 3)))


# ================================================================ карточки моделей
def model_page(m):
    ph = photo(m)
    leg = LEG[m['leg'][0]].get(m['leg'][1], {}) if m['leg'] else {}
    old_desc = leg.get('description', '')
    alg = ALGO[m['algo']]
    brand_key = m['brand'].lower()
    brand_label = dict((b[2], b[1]) for b in BRANDS)[m['brand']]
    full = '%s %s' % (m['brand'], m['name'])
    kw_day = m['w'] * 24 / 1000 if m['w'] else None

    rows = [['Производитель', m['brand']], ['Алгоритм', m['algo']], ['Хешрейт', hr(m)],
            ['Потребление', ('%d Вт' % m['w']) if m['w'] else 'уточняйте'], ['Энергоэффективность', fmt_eff(m)],
            ['Охлаждение', {'hydro': 'жидкостное (Hydro)', 'air': 'воздушное'}.get(m['cooling'], 'уточняйте')]]
    if m['noise']:
        rows.append(['Шум', '%d дБ' % m['noise']])
    if kw_day:
        rows.append(['Расход энергии в сутки', ('%.1f кВт·ч' % kw_day).replace('.', ',')])
    kv = '<table class="kv">%s</table>' % ''.join('<tr><td>%s</td><td>%s</td></tr>' % tuple(r) for r in rows)

    imgs = ph or [placeholder_svg(m)]
    gallery = ('<div class="pd-gallery"><div class="main"><img src="%s" alt="%s"></div>%s</div>'
               % (u('/' + imgs[0]), esc(full),
                  '<div class="thumbs">%s</div>' % ''.join('<button type="button" data-src="%s"><img src="%s" alt=""></button>'
                                                          % (u('/' + x), u('/' + x)) for x in imgs) if len(imgs) > 1 else ''))
    info = ('<div class="pd-info"><div class="tags"><span class="tag tag-accent">%s</span><span class="tag">%s</span></div>'
            '<h1>%s</h1>%s<div class="pd-price">Цена по запросу<small>Меняется вместе с курсом и наличием — зафиксируем в счёте</small></div>'
            '<div class="pd-actions"><a class="btn btn-accent" href="%s">Узнать цену и наличие</a>'
            '<a class="btn btn-line" href="%s">Рассчитать доходность</a></div></div>'
            % (m['algo'], brand_label, esc(full), kv, u('/#podbor'), u('/table/')))

    # ---------- текст карточки
    sec = []
    sec.append(h2('Какие монеты добывает', 'monety'))
    sec.append(p('%s работает на алгоритме %s. На нём добываются: %s. Монета выбирается в настройках пула — '
                 'сам асик переключить на другой алгоритм нельзя.' % (full, m['algo'], alg['coins'])))
    if m['w'] and m['h']:
        sec.append(h2('Сколько электричества потребляет', 'potreblenie'))
        costs = [(t, kw_day * t) for t in (3, 5, 7)]
        sec.append(p('Паспортное потребление — %d Вт, то есть %s кВт·ч в сутки и около %s кВт·ч в месяц. '
                     'Это главная статья расходов: при разных тарифах счёт за электричество одного устройства выглядит так:'
                     % (m['w'], ('%.1f' % kw_day).replace('.', ','), '{:,}'.format(round(kw_day * 30)).replace(',', ' '))))
        sec.append(ptable(['Тариф', 'Расход в сутки', 'Расход в месяц'],
                          [['%d ₽/кВт·ч' % t, '{:,} ₽'.format(round(c)).replace(',', ' '), '{:,} ₽'.format(round(c * 30)).replace(',', ' ')]
                           for t, c in costs]))
        sec.append(p('Доход зависит от курса и сложности сети и меняется каждый день, поэтому мы не пишем его в карточке. '
                     'Подставьте текущий хешпрайс в ' + a('/table/', 'калькулятор') + ' — он сразу покажет прибыль, '
                     'окупаемость и тариф, при котором %s выходит в ноль.' % m['name']))
    sec.append(h2('Кому подойдёт', 'komu'))
    if m['cooling'] == 'hydro':
        sec.append(p('Это гидроверсия: платы охлаждаются жидкостью, а не вентиляторами. Модель рассчитана на промышленные '
                     'площадки с контуром охлаждения (насос, теплообменник, драйкулер) и на проекты, где важны плотность '
                     'размещения, низкий шум или утилизация тепла. Для дома без инженерной подготовки не подходит — '
                     'разместить её можно в ' + a('/services/hosting/', 'дата-центре') + '.'))
    elif m['w'] and m['w'] < 1000:
        sec.append(p('Компактная модель с низким потреблением: её можно поставить дома, подключив к обычной розетке. '
                     'Подходит для знакомства с майнингом и небольшого пассивного дохода без инженерной подготовки.'))
    elif m['w']:
        e = eff(m)
        good = m['unit'] == 'TH/s' and m['algo'] == 'SHA-256' and e and e <= 17
        sec.append(p('Воздушная модель мощностью около %s кВт. Нужна отдельная линия питания 220 В (или 380 В для группы '
                     'устройств), приток холодного воздуха и отвод горячего. Уровень шума у воздушных асиков — около '
                     '75 дБ, поэтому дома без ' % ('%.1f' % (m['w'] / 1000)).replace('.', ',')
                     + a('/catalog/komplektuyushchie/shumoboksy/', 'шумобокса') + ' не обойтись. '
                     + ('По эффективности это одна из лучших воздушных моделей — она остаётся прибыльной при большинстве '
                        'российских тарифов.' if good else
                        'Модель предыдущих поколений: выгодна при дешёвом электричестве, при дорогом стоит сравнить '
                        'с более новыми устройствами.')))
    else:
        sec.append(p('Характеристики этой модели зависят от ревизии — уточняйте у менеджера перед заказом.'))

    sec.append(h2('Что проверить перед покупкой', 'proverka'))
    sec.append(ul(['<b>Ревизию и точный хешрейт</b> — у одной модели бывает несколько версий с разными платами и потреблением.',
                   '<b>Тип блока питания и разъём</b> — нужна розетка или клеммы под мощность устройства.',
                   '<b>Гарантию</b> — заводскую или сервисную, и кто её обслуживает в России.',
                   '<b>Сроки поставки</b> — «в наличии» и «под заказ» отличаются на недели.']))
    sec.append(p('Если асик нужен не для дома, а для площадки, посмотрите ' + a('/services/mining-pod-kljuch/', 'запуск под ключ') +
                 ': мы рассчитаем электрику и вентиляцию под количество устройств.'))

    if old_desc:
        sec.append(h2('Описание модели', 'opisanie'))
        sec.append('<div class="legacy">%s</div>' % md_to_html(old_desc))

    faq = [('Сколько стоит %s?' % m['name'],
            'Цена зависит от курса, партии и наличия и меняется ежедневно. Напишите или позвоните — назовём актуальную '
            'цену и сроки и зафиксируем их в счёте.'),
           ('Можно ли разместить %s в дата-центре?' % m['name'],
            'Да. Мы размещаем асики на площадках с промышленным тарифом, охлаждением и мониторингом — подробнее на '
            'странице <a href="%s">хостинга</a>.' % u('/services/hosting/'))]
    if m['w']:
        faq.insert(1, ('Сколько электричества потребляет %s?' % m['name'],
                       'Паспортное потребление — %d Вт, около %s кВт·ч в сутки.' % (m['w'], ('%.1f' % kw_day).replace('.', ','))))

    siblings = [x for x in M if x is not m and (x['algo'] == m['algo'])][:4]
    body = (section('<div class="pd">' + gallery + info + '</div>', cls='sec-soft')
            + section('<div class="layout"><div class="prose">' + ''.join(sec) + h2('Частые вопросы', 'faq')
                      + faq_html(faq) + '</div><aside class="aside">'
                      + cta_box('Нужна консультация?', 'Подскажем, подойдёт ли %s под ваш тариф и площадку, и посчитаем окупаемость.' % m['name'],
                                '/#podbor', 'Получить расчёт') + '</aside></div>')
            + (section(grid(siblings), cls='sec-soft', title='Похожие модели') if siblings else ''))

    prod_ld = {"@type": "Product", "name": full, "brand": {"@type": "Brand", "name": m['brand']},
               "category": "ASIC-майнер", "description": 'ASIC-майнер %s на алгоритме %s.' % (full, m['algo'])}
    add(path=m['path'], kind='product',
        title=('%s — купить, характеристики | MiningShop' % full) if len(full) < 42 else ('%s — характеристики и цена' % full),
        description='%s: %s, %s, эффективность %s. Расчёт потребления и окупаемости, доставка по России, настройка.'
                    % (full, hr(m), ('%d Вт' % m['w']) if m['w'] else 'алгоритм ' + m['algo'], fmt_eff(m)),
        h1=full, crumbs=[('Каталог', '/catalog/'), ('ASIC-майнеры', '/catalog/asic_maynery/'),
                         (brand_label, '/catalog/asic_maynery/%s/' % brand_key), (m['name'], m['path'])],
        hero='', body='<div class="wrap" style="padding-top:18px">' + crumbs_inline(m, brand_label, brand_key) + '</div>' + body,
        ld=[prod_ld, faq_ld(faq)])


def crumbs_inline(m, brand_label, brand_key):
    return ('<div class="crumbs" style="color:#66717c"><a style="color:#66717c" href="%s">Главная</a><span>/</span>'
            '<a style="color:#66717c" href="%s">ASIC-майнеры</a><span>/</span><a style="color:#66717c" href="%s">%s</a>'
            '<span>/</span>%s</div>' % (u('/'), u('/catalog/asic_maynery/'), u('/catalog/asic_maynery/%s/' % brand_key),
                                         brand_label, esc(m['name'])))


def md_to_html(md):
    """Мини-конвертер Markdown из архива: абзацы, списки, жирный."""
    out, lst = [], []
    for block in re.split(r'\n\s*\n', md):
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if not lines:
            continue
        if all(re.match(r'^[-*•]\s+', l) for l in lines):
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(re.sub(r'^[-*•]\s+', '', l)) for l in lines))
        elif lines[0].startswith('#'):
            out.append('<h3>%s</h3>' % inline(lines[0].lstrip('# ')))
            if lines[1:]:
                out.append('<p>%s</p>' % inline(' '.join(lines[1:])))
        else:
            out.append('<p>%s</p>' % inline(' '.join(lines)))
    return ''.join(out)


def inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s


for _m in M:
    model_page(_m)
