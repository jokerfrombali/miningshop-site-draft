# -*- coding: utf-8 -*-
"""Однократная выгрузка уже написанных текстов (статьи базы знаний и страницы услуг,
опубликованные на miningshop.ru 22.09.2026) в JSON, чтобы сборка сайта не зависела
от рабочей папки, где они создавались."""
import json, os, sys

WS = r'C:\Users\anich\AppData\Local\Temp\claude\wsdata'
sys.path.insert(0, WS)
import articles_batch1, articles_batch2, pages_services  # noqa: E402

KEEP = ('section', 'slug', 'title', 'h1', 'description', 'lead', 'published', 'updated', 'read_min', 'toc', 'related', 'body',
        'url', 'crumbs', 'faq')
out = {'articles': [], 'services': []}
for a in articles_batch1.ARTICLES + articles_batch2.ARTICLES:
    out['articles'].append({k: a[k] for k in KEEP if k in a})
for pg in pages_services.PAGES:
    out['services'].append({k: pg[k] for k in KEEP if k in pg})
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'reused_content.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('статей: %d, услуг: %d' % (len(out['articles']), len(out['services'])))
