from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

KAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
SHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

logging.basicConfig(level=logging.INFO)

HTML = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>四柱推命診断</title>
</head>
<body style="font-family:sans-serif;padding:20px;">
  <h1>🔮 四柱推命フォーム</h1>
  <form method="post">
    名前: <input type="text" name="name"><br>
    年: <input type="number" name="year"><br>
    月: <input type="number" name="month"><br>
    日: <input type="number" name="day"><br>
    時: <input type="number" name="hour"><br>
    <button type="submit">診断実行</button>
  </form>
  {% if error %}
    <p style="color:red;">⚠️ {{ error }}</p>
  {% endif %}
  {% if result %}
    <h2>📝 診断結果</h2>
    <div style="background:#f0f0f0;padding:15px;border-radius:8px;">
      {{ result | safe }}
    </div>
  {% endif %}
</body>
</html>
'''

app = Flask(__name__)

def eto(tenkan, chishi):
    try:
        return f"{KAN[int(tenkan) % 10]}{SHI[int(chishi) % 12]}"
    except Exception:
        return "不明"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            year = int(request.form.get("year", "0"))
            month = int(request.form.get("month", "0"))
            day = int(request.form.get("day", "0"))
            hour = int(request.form.get("hour", "0"))

            if not all([name, year, month, day, hour]):
                error = "全ての項目を入力してください"
            else:
                m = Meishiki(year, month, day, hour)

                # 年柱・月柱・日柱・時柱
                nenchu = eto(*m.nenchu) if isinstance(m.nenchu, (list, tuple)) and len(m.nenchu) == 2 else "不明"
                getchu = eto(*m.getchu) if isinstance(m.getchu, (list, tuple)) and len(m.getchu) == 2 else "不明"
                nitchu = eto(m.nikkan, m.chishi)
                jichu = eto(*m.jichu) if isinstance(m.jichu, (list, tuple)) and len(m.jichu) == 2 else "不明"

                result = f"""
                🌸 <strong>名前:</strong> {name}<br>
                <hr>
                📅 <strong>年柱:</strong> {nenchu}<br>
                📅 <strong>月柱:</strong> {getchu}<br>
                📅 <strong>日柱:</strong> {nitchu}<br>
                📅 <strong>時柱:</strong> {jichu}<br>
                <hr>
                🔢 <strong>十干番号(日):</strong> {m.nikkan}<br>
                🧬 <strong>性別コード:</strong> {m.sex}
                """

        except Exception as e:
            logging.error("内部エラー: %s", e)
            error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
