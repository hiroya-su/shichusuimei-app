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
    if request.method == "POST":
        name = request.form["name"]
        year = int(request.form["year"])
        month = int(request.form["month"])
        day = int(request.form["day"])
        hour = int(request.form["hour"])
        m = Meishiki(year, month, day, hour)
        result = m.show_as_dict()
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
