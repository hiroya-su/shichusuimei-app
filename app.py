from flask import Flask, request, render_template_string
from meishiki import Meishiki

app = Flask(__name__)

HTML = '''
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>四柱推命</title></head><body>
<h1>🔮 四柱推命 診断フォーム</h1>
<form method="post">
名前: <input name="name"><br>
年: <input name="year" type="number"><br>
月: <input name="month" type="number"><br>
日: <input name="day" type="number"><br>
時: <input name="hour" type="number"><br>
<button type="submit">診断</button>
</form>
{% if result %}<h2>結果</h2><pre>{{ result }}</pre>{% endif %}
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
</body></html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            name = request.form["name"]
            year = int(request.form["year"])
            month = int(request.form["month"])
            day = int(request.form["day"])
            hour = int(request.form["hour"])

            m = Meishiki(year, month, day, hour)

            # 各干支を正しく取得
            nenchu = str(m.nenchu.kanshi()) if hasattr(m.nenchu, "kanshi") else "不明"
            getchu = str(m.getchu.kanshi()) if hasattr(m.getchu, "kanshi") else "不明"
            nitchu = str(m.nitchu.kanshi()) if hasattr(m.nitchu, "kanshi") else "不明"
            jichu = str(m.jichu.kanshi()) if hasattr(m.jichu, "kanshi") else "不明"

            result = f"""🌸 名前: {name}
📅 年柱: {nenchu}
📅 月柱: {getchu}
📅 日柱: {nitchu}
📅 時柱: {jichu}
🔢 十干番号(日): {m.nikkan}
🧬 性別コード: {m.sex}"""
        except Exception as e:
            error = f"⚠️ エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
