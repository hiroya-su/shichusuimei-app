from flask import Flask, request, render_template_string
from meishiki import Meishiki

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>四柱推命 診断</title>
</head>
<body>
  <h1>🔮 四柱推命 診断フォーム</h1>
  <form method="post">
    名前: <input type="text" name="name"><br>
    年:   <input type="number" name="year"><br>
    月:   <input type="number" name="month"><br>
    日:   <input type="number" name="day"><br>
    時:   <input type="number" name="hour"><br>
    <button type="submit">命式を表示</button>
  </form>

  {% if error %}
    <p style="color:red">⚠️ {{ error }}</p>
  {% endif %}

  {% if result %}
    <h2>📝 命式結果</h2>
    <pre>{{ result | tojson(indent=2, ensure_ascii=False) }}</pre>
  {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None  # エラーメッセージ用

    if request.method == "POST":
        # 入力取得とトリム
        name   = request.form.get("name", "").strip()
        year_s = request.form.get("year", "").strip()
        month_s= request.form.get("month", "").strip()
        day_s  = request.form.get("day", "").strip()
        hour_s = request.form.get("hour", "").strip()

        # 空欄チェック
        if not (name and year_s and month_s and day_s and hour_s):
            error = "全ての項目（名前・年・月・日・時）を入力してください"
        else:
            try:
                year  = int(year_s)
                month = int(month_s)
                day   = int(day_s)
                hour  = int(hour_s)

                m = Meishiki(year, month, day, hour)
                result = vars(m)  # 一旦辞書化して結果表示
            except ValueError:
                error = "年/月/日/時 には数字を入力してください"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
