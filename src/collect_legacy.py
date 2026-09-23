# -*- coding: utf-8 -*-
"""Собирает из архива старого сайта данные для карточек: описания, фото, характеристики.

Для моделей, которые уже есть на живом сайте (17 Bitmain), подтягиваем фото и описание
по названию. Для моделей, которые приносили трафик в 2024–2025 годах и которых на новом
сайте нет, берём и сам старый адрес страницы — у него остались внешние ссылки и история
в поиске, выгоднее вернуть страницу туда же, чем заводить новую.
"""
import json, os, re, shutil

ARCH = r'D:\Projects\miningshop-archive'
SITE = r'D:\Projects\miningshop-site'

P = json.load(open(os.path.join(ARCH, 'data', 'products.json'), encoding='utf-8'))


def photos(p):
    return [x for x in (p.get('images_local') or []) + (p.get('images_preview_local') or []) if x]


def best(rx):
    hits = [p for p in P if re.search(rx, (p.get('name') or '').lower())]
    hits.sort(key=lambda p: (len(photos(p)), len(p.get('description_md') or ''), p['archived_at']), reverse=True)
    return hits[0] if hits else None


def clean_desc(md):
    if not md:
        return ''
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', md)            # картинки из тела описания
    md = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', md)          # ссылки -> текст
    md = re.sub(r'(?im)^.*(цена товара может|наложенн|звоните|88002003264|8 ?800 ?200).*$', '', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


def copy_photos(p, slug):
    out = []
    for i, rel in enumerate(photos(p)[:6]):
        src = os.path.join(ARCH, rel.replace('/', os.sep))
        if not os.path.exists(src):
            continue
        ext = os.path.splitext(src)[1].lower() or '.jpg'
        dst_rel = 'assets/img/products/%s-%d%s' % (slug, i + 1, ext)
        shutil.copyfile(src, os.path.join(SITE, dst_rel.replace('/', os.sep)))
        out.append(dst_rel)
    return out


# модели живого сайта: slug -> регулярка по названию в архиве
LIVE = {
    'antminer-s19-pro-110th': r'^bitmain antminer s19 pro$',
    'antminer-s19j-pro-104th': r'^bitmain antminer s19j pro$',
    'antminer-l7-9500mh': r'^bitmain antminer l7$',
    'antminer-s19-xp-141th': r'^bitmain antminer s19xp$',
}
# модели старого сайта, которые возвращаем по старому адресу
LEGACY = {
    'whatsminer-m30s-plus-plus': r'^whatsminer m30s\+\+$',
    'whatsminer-m30s-plus': r'^whatsminer m30s\+$',
    'whatsminer-m21s': r'^whatsminer m21s$',
    'whatsminer-m56': r'^whatsminer m56$',
    'ipollo-v1-mini-classic-plus': r'^ipollo v1 mini classic plus$',
    'antminer-e9-pro': r'e9 pro 3680m',
    'antminer-s19k-pro': r'^bitmain antminer s19k pro$',
    'antminer-s19-pro-hyd': r's19 pro hyd',
    'jasminer-x16-q': r'jasminer x16-q',
}

res = {'live': {}, 'legacy': {}}
for group, table in (('live', LIVE), ('legacy', LEGACY)):
    for slug, rx in table.items():
        p = best(rx)
        if not p:
            print('нет в архиве:', slug)
            continue
        res[group][slug] = {
            'archive_name': p['name'],
            'old_url': p['url'],
            'old_path': re.sub(r'^https://miningshop\.ru', '', p['url']).split('?')[0],
            'archived_at': p['archived_at'],
            'specs': p['specs'],
            'description': clean_desc(p.get('description_md')),
            'photos': copy_photos(p, slug),
        }
        r = res[group][slug]
        print('%-6s %-30s фото %d | описание %5d | %s' % (group, slug, len(r['photos']), len(r['description']), r['old_path']))

json.dump(res, open(os.path.join(SITE, 'src', 'legacy.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
