from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

KAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
SHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

logging.basicConfig(level=logging.INFO)

HTML = '''
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>四柱推命</title></head><body>
  <h1>🔮 四柱推命テスト</h1>
  <form method="post">
    名前: <input type="text" name="name"><br>
    年: <input type="number" name="year"><br>
    月: <input type="number" name="month"><br>
    日: <input type="number" name="day"><br>
    時: <input type="number" name="hour"><br>
    <button type="submit">診断実行</button>
  </form>
  {% if error %}<p style="color:red">⚠️ {{ error }}</p>{% endif %}
  {% if result %}<h2>📝 結果</h2><pre>{{ result }}</pre>{% endif %}
</body></html>
'''

app = Flask(__name__)

def resolve_kanshi(value):
    """干支を番号やオブジェクトから文字列に変換"""
    try:
        if isinstance(value, (list, tuple)) and len(value) == 2:
            return f"{KAN[value[0]]}{SHI[value[1]]}"
        elif hasattr(value, 'tenkan') and hasattr(value, 'chishi'):
            return f"{KAN[value.tenkan]}{SHI[value.chishi]}"
        elif isinstance(value, dict) and "tenkan" in value and "chishi" in value:
            return f"{KAN[value['tenkan']]}{SHI[value['chishi']]}"
    except Exception:
        pass
    return "不明"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            year = int(request.form.get("year", ""))
            month = int(request.form.get("month", ""))
            day = int(request.form.get("day", ""))
            hour = int(request.form.get("hour", ""))

            m = Meishiki(year, month, day, hour)
            app.logger.info("属性確認: %s", dir(m))

            result = f"""🌸 名前: {name}
📅 年柱: {resolve_kanshi(m.nenchu)}
📅 月柱: {resolve_kanshi(m.getchu)}
📅 日柱: {resolve_kanshi(m.nitchu)}
📅 時柱: {resolve_kanshi(m.jichu)}
🔢 十干番号(日): {m.nikkan}
🧬 性別コード: {m.sex}
"""
        except Exception as e:
            error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
