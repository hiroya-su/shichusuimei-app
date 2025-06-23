from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

KAN = "甲乙丙丁戊己庚辛壬癸"
SHI = "子丑寅卯辰巳午未申酉戌亥"

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

def kanshi_str(lst):
    if isinstance(lst, list) and len(lst) >= 2:
        kan = KAN[lst[0]] if 0 <= lst[0] < len(KAN) else "不明"
        shi = SHI[lst[1]] if 0 <= lst[1] < len(SHI) else "不明"
        return f"{kan}{shi}"
    return "不明"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            y = int(request.form.get("year", ""))
            m = int(request.form.get("month", ""))
            d = int(request.form.get("day", ""))
            h = int(request.form.get("hour", ""))

            m_obj = Meishiki(y, m, d, h)

            nenchu = kanshi_str(getattr(m_obj, "nenchu", []))
            getchu = kanshi_str(getattr(m_obj, "getchu", []))
            nitchu = kanshi_str(getattr(m_obj, "nitchu", []))
            jichu  = kanshi_str(getattr(m_obj, "jichu", []))
            nikkan = getattr(m_obj, "nikkan", "不明")
            sex    = getattr(m_obj, "sex", "不明")

            result = f"""🌸 名前: {name}
📅 年柱: {nenchu}
📅 月柱: {getchu}
📅 日柱: {nitchu}
📅 時柱: {jichu}
🔢 十干番号(日): {nikkan}
🧬 性別コード: {sex}
"""

        except Exception as e:
            logging.exception("内部エラー:")
            error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
