import datetime as dt
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

FOUNDATION_YEAR = 1920


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    products = pd.read_excel(
        'wine3.xlsx', sheet_name='Лист1', index_col=[0]
    ).astype({'Цена': 'int32'}).replace(np.nan, None).sort_index()
    products.reset_index(level=0, inplace=True)
    grouped_wines = products.sort_values(
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
    main()
