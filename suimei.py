from meishiki import build_meishiki
from unsei import build_unsei
from output import output_html, output_stdio
from datetime import datetime as dt
import sys

if __name__ == '__main__':

    birthday = dt.strptime(sys.argv[1] + ' ' + sys.argv[2], '%Y-%m-%d %H:%M')
    sex = int(sys.argv[3])
    
    # 命式を組成する
    meishiki = build_meishiki(birthday, sex)

    # 運勢を組成する
    unsei = build_unsei(meishiki)
    
    # 命式・運勢を出力する
    f1 = output_html(meishiki, unsei)
    f2 = output_stdio(meishiki, unsei)
    
