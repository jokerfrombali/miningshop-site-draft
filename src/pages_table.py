# -*- coding: utf-8 -*-
"""/table/ — доходность асиков. Старый адрес с 33 тыс. входов в 2021–2022 и спросом
«доходность асиков» 1,6 тыс. и «калькулятор асиков» 1,2 тыс. в месяц.

Доход асика = хешрейт × хешпрайс (доход на единицу хешрейта в сутки). Хешпрайс меняется
каждый день вместе с курсом и сложностью сети, поэтому в статике его не зашиваем:
пользователь вводит актуальное значение, а таблица и калькулятор считают остальное.
Потребление и эффективность — фиксированные характеристики, их считаем заранее.
"""
from core import (add, u, h2, h3, p, ul, note, ptable, faq_html, faq_ld, section, a)
from pages_asic import M, hr, fmt_eff, eff

sha = [m for m in M if m['algo'] == 'SHA-256' and m['h'] and m['w']]
sha.sort(key=lambda m: eff(m))

rows = []
for m in sha:
    kwh = m['w'] * 24 / 1000
    rows.append('<tr data-h="%g" data-w="%d"><td><a href="%s">%s %s</a></td><td>%s</td><td>%d Вт</td><td>%s</td>'
                '<td>%s</td><td class="inc">—</td><td class="en">—</td><td class="pr">—</td><td class="be">—</td></tr>'
                % (m['h'], m['w'], u(m['path']), m['brand'], m['name'], hr(m), m['w'], fmt_eff(m),
                   ('%.1f' % kwh).replace('.', ',')))

options = ''.join('<option value="%s" data-h="%g" data-p="%d" data-u="%s">%s %s</option>'
                  % (m['path'], m['h'], m['w'], 'TH/s', m['brand'], m['name']) for m in sha)

calc = ('<form class="calc" data-calc onsubmit="return false">'
        '<div class="card"><h3>Исходные данные</h3>'
        '<label class="field"><span>Модель (подставит хешрейт и потребление)</span><select name="model">'
        '<option value="">— своя конфигурация —</option>%s</select></label>'
        '<label class="field"><span>Хешрейт, <b data-o="unit">TH/s</b></span><input name="hash" type="number" step="any" value="200"><input name="unit" type="hidden" value="TH/s"></label>'
        '<label class="field"><span>Потребление, Вт</span><input name="power" type="number" step="any" value="3500"></label>'
        '<label class="field"><span>Тариф на электроэнергию, ₽/кВт·ч</span><input name="tariff" type="number" step="any" value="5"></label>'
        '<label class="field"><span>Хешпрайс, ₽ за 1 TH/s в сутки</span><input name="hashprice" type="number" step="any" value="4"></label>'
        '<label class="field"><span>Комиссия пула, %%</span><input name="pool" type="number" step="any" value="2"></label>'
        '<label class="field"><span>Цена асика, ₽ (для окупаемости)</span><input name="price" type="number" step="any" value="0"></label>'
        '</div><div class="calc-out"><h3 style="font:700 20px var(--font-head);text-transform:uppercase;margin:0 0 18px">Результат</h3><dl>'
        '<dt>Доход в сутки</dt><dd data-o="income">—</dd>'
        '<dt>Электричество в сутки</dt><dd data-o="energy">—</dd>'
        '<dt>Прибыль в сутки</dt><dd data-o="profit" class="big">—</dd>'
        '<dt>Прибыль за 30 дней</dt><dd data-o="month">—</dd>'
        '<dt>Окупаемость</dt><dd data-o="payback">—</dd>'
        '<dt>Тариф безубыточности</dt><dd data-o="breakeven">—</dd></dl>'
        '<p style="color:#b6c0c8;font-size:14px;margin:18px 0 0">Хешпрайс по умолчанию — пример, а не текущее значение. '
        'Подставьте актуальный: его публикуют пулы и сервисы аналитики майнинга (в долларах за TH/s в сутки — умножьте на курс).</p>'
        '</div></form>' % options)

table = ('<div class="tbl-wrap" style="margin-top:28px"><table class="tbl" data-table>'
         '<thead><tr><th>Модель</th><th>Хешрейт</th><th>Потребление</th><th>Эффективность</th><th>кВт·ч/сутки</th>'
         '<th>Доход/сутки</th><th>Свет/сутки</th><th>Прибыль/сутки</th><th>Безубыточный тариф</th></tr></thead>'
         '<tbody>%s</tbody></table></div>' % ''.join(rows))

# таблица пересчитывается тем же хешпрайсом и тарифом, что введены в калькуляторе
table_js = ('<script>(function(){var f=document.querySelector("[data-calc]");var t=document.querySelector("[data-table]");'
            'if(!f||!t)return;function r(){var hp=+f.hashprice.value,tr=+f.tariff.value,pl=+f.pool.value/100;'
            't.querySelectorAll("tbody tr").forEach(function(row){var h=+row.dataset.h,w=+row.dataset.w;'
            'var inc=h*hp*(1-pl),en=w/1000*24*tr,pr=inc-en,be=inc/(w/1000*24);'
            'var n=function(v,d){return v.toLocaleString("ru-RU",{maximumFractionDigits:d||0})};'
            'row.querySelector(".inc").textContent=n(inc)+" ₽";row.querySelector(".en").textContent=n(en)+" ₽";'
            'var c=row.querySelector(".pr");c.textContent=n(pr)+" ₽";c.className="pr "+(pr>=0?"pos":"neg");'
            'row.querySelector(".be").textContent=n(be,2)+" ₽";});}'
            'f.addEventListener("input",r);r();})();</script>')

faq = [
    ('Как посчитать доходность асика?',
     'Доход в сутки = хешрейт × хешпрайс (доход на 1 TH/s в сутки) за вычетом комиссии пула. Расход = потребление в кВт × '
     '24 часа × тариф. Прибыль — разница между ними. Калькулятор выше делает это автоматически.'),
    ('Что такое хешпрайс и где его взять?',
     'Хешпрайс — сколько приносит 1 TH/s за сутки при текущем курсе биткоина и сложности сети. Его ежедневно публикуют пулы '
     'и сервисы аналитики майнинга, обычно в долларах. Умножьте на курс рубля и подставьте в калькулятор.'),
    ('Почему реальный доход отличается от расчёта?',
     'Расчёт — моментальный снимок. Курс и сложность сети меняются ежедневно, сложность в долгую растёт. Плюс простои, '
     'температура и прошивка влияют на фактический хешрейт. Для решения о покупке смотрите на тариф безубыточности: '
     'чем больше запас между ним и вашим тарифом, тем устойчивее проект.'),
    ('Какой асик самый выгодный?',
     'При дорогом электричестве выигрывает не самый мощный, а самый эффективный — с наименьшим числом джоулей на терахеш. '
     'В таблице модели отсортированы именно по эффективности.'),
]

body = (section(calc + table + table_js, cls='sec-soft', title='Калькулятор доходности',
                sub='Введите тариф и текущий хешпрайс — калькулятор и таблица пересчитают доход, прибыль и тариф безубыточности '
                    'для всех асиков на SHA-256. Модели отсортированы по энергоэффективности.')
        + section('<div class="prose">'
                  + h2('Как читать таблицу', 'kak')
                  + p('<b>Эффективность</b> — сколько джоулей асик тратит на терахеш. Это ключевой параметр: при одинаковом '
                      'хешпрайсе прибыль определяет именно он. <b>Тариф безубыточности</b> — цена киловатт-часа, при которой '
                      'доход асика равен расходу на электричество. Если ваш тариф ниже — асик приносит прибыль; чем больше '
                      'разница, тем больше запас прочности на случай падения курса или роста сложности.')
                  + note('Это не обещание дохода', 'Калькулятор считает по введённым данным и не прогнозирует курс и сложность сети. '
                         'Для решения о покупке закладывайте рост сложности и обслуживание — поможем с полным расчётом в '
                         + a('/services/business-plan/', 'бизнес-плане') + '.')
                  + h2('Что ещё влияет на прибыль', 'faktory')
                  + ul(['<b>Простои</b> — перезагрузки, обслуживание, аварии питания: каждый процент простоя — минус процент дохода.',
                        '<b>Температура</b> — в жару асики сбрасывают частоты, в пыли — перегреваются.',
                        '<b>Место размещения</b> — промышленный тариф в ' + a('/services/hosting/', 'дата-центре') +
                        ' часто меняет экономику сильнее, чем выбор модели.',
                        '<b>Комиссия пула</b> — обычно 1–4 %, учитывайте её в расчёте.'])
                  + h2('Частые вопросы', 'faq') + faq_html(faq) + '</div>'))

add(path='/table/', kind='tool',
    title='Доходность асиков 2026: калькулятор и таблица окупаемости ASIC-майнеров — MiningShop',
    description='Калькулятор доходности асиков: доход, прибыль, окупаемость и тариф безубыточности для Antminer S21, S21 XP, '
                'S19, Whatsminer M30S++ и других. Подставьте свой тариф и текущий хешпрайс.',
    h1='Доходность асиков', lead='Калькулятор и таблица окупаемости ASIC-майнеров на SHA-256: подставьте свой тариф на '
                                 'электроэнергию и текущий хешпрайс — получите прибыль и тариф безубыточности по каждой модели.',
    crumbs=[('Доходность асиков', '/table/')], body=body, ld=[faq_ld(faq)])
