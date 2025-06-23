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
    年: <input type="number" name="year"><br>
    月: <input type="number" name="month"><br>
    日: <input type="number" name="day"><br>
    時: <input type="number" name="hour"><br>
    <button type="submit">命式を表示</button>
  </form>

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
    error = None  # エラーメッセージ保持用

    if request.method == "POST":
        # 入力値を文字列として取得
        year_str = request.form.get("year", "").strip()
        month_str = request.form.get("month", "").strip()
        day_str = request.form.get("day", "").strip()
        hour_str = request.form.get("hour", "").strip()

        # 必須チェックとエラー設定
        if not (year_str and month_str and day_str and hour_str):
            error = "年・月・日・時 をすべて入力してください"
        else:
            try:
                year = int(year_str); month = int(month_str)
                day = int(day_str); hour = int(hour_str)

                m = Meishiki(year, month, day, hour)
                print(dir(m))  # ← ここでメソッド一覧を出力！
                result = {}  # 仮で
                # result = m.show_as_dict()
            except ValueError:
                error = "入力値が不正です: 数字で入力してください"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
