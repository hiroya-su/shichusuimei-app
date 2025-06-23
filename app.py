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
    error_msg = None  # ← ここが“冒頭”です

    if request.method == "POST":
        # 入力の取得
        name = request.form.get("name", "").strip()
        year = request.form.get("year", "").strip()
       ...

        # バリデーション
        if not name or not year or not month or not day or not hour:
            error_msg = "全ての項目を入力してください"
        else:
            try:
                year = int(year); month = int(month); day = int(day); hour = int(hour)
            except ValueError:
                error_msg = "年/月/日/時 には数字を入力してください"
        
        if error_msg is None:
            m = Meishiki(year, month, day, hour)
            result = m.show_as_dict()
        else:
            result = None

    else:
        result = None

    return render_template_string(HTML, result=result, error=error_msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
