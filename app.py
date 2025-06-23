from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

HTML = '''
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>四柱推命</title></head><body>
  <h1>🔮 四柱推命 診断</h1>
  <form method="post">
    名前: <input type="text" name="name"><br>
    年: <input type="number" name="year"><br>
    月: <input type="number" name="month"><br>
    日: <input type="number" name="day"><br>
    時: <input type="number" name="hour"><br>
    <button type="submit">診断</button>
  </form>
  {% if error %}<p style="color:red">⚠️ {{ error }}</p>{% endif %}
  {% if result %}<h2>📝 結果</h2><pre>{{ result }}</pre>{% endif %}
</body></html>
'''

def resolve_kanshi(field):
    if isinstance(field, (list, tuple)) and len(field) >= 2:
        return f"{field[0]}{field[1]}"
    elif hasattr(field, '__getitem__') and len(field) >= 2:
        return f"{field[0]}{field[1]}"
    elif hasattr(field, 'kanshi'):
        return str(field.kanshi)
    return "不明"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            year = int(request.form.get("year", 0))
            month = int(request.form.get("month", 0))
            day = int(request.form.get("day", 0))
            hour = int(request.form.get("hour", 0))

            m = Meishiki(year, month, day, hour)
            app.logger.info("属性確認: %s", dir(m))

            nenchu = resolve_kanshi(m.nenchu)
            getchu = resolve_kanshi(m.getchu)
            nitchu = resolve_kanshi(m.nitchu)
            jikkan = m.nikkan if hasattr(m, 'nikkan') else "不明"

            result = f'''🌸 名前: {name}
📅 年柱: {nenchu}
📅 月柱: {getchu}
📅 日柱: {nitchu}
📅 時柱: {resolve_kanshi(m.jichu)}
🔢 十干番号(日): {jikkan}
🧬 性別コード: {m.sex}'''

        except Exception as e:
            error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
