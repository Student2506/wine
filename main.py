import datetime as dt
from collections import defaultdict
from contextlib import suppress
from http.server import HTTPServer, SimpleHTTPRequestHandler

import configargparse
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

FOUNDATION_YEAR = 1920


def main():
    parser = configargparse.ArgParser()
    parser.add(
        'filename', nargs='?', default='wine3.xlsx', help='File to import'
    )
    options = parser.parse_args()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    grouped_wines = pd.read_excel(
        options.filename, sheet_name='Лист1', keep_default_na=False
    ).astype({'Цена': 'int32'}).sort_values(
        by=['Категория']
    ).to_dict(orient='index')
    wines = defaultdict(list)
    for wine in grouped_wines.values():
        wines[wine['Категория']].append(wine)
    rendered_page = template.render(
        age=dt.datetime.today().year-FOUNDATION_YEAR,
        wines=wines,
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main()
