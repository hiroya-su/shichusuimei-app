from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

# ——————————————————————————
# ログの初期設定（app.logger を INFO レベルで有効に）
logging.basicConfig(level=logging.INFO)

# HTML テンプレート（ファイル上部）
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
  {% if result %}<h2>📝 結果</h2><pre>{{ result|tojson(indent=2, ensure_ascii=False) }}</pre>{% endif %}
</body></html>
'''

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        year = request.form.get("year", "").strip()
        month = request.form.get("month", "").strip()
        day = request.form.get("day", "").strip()
        hour = request.form.get("hour", "").strip()

        if not all([name, year, month, day, hour]):
            error = "全ての項目を入力してください"
        else:
            try:
                y, m, d, h = map(int, (year, month, day, hour))
                m_obj = Meishiki(y, m, d, h)
                app.logger.info("Meishiki生成 OK: %s", dir(m_obj))
                if hasattr(m_obj, "to_dict"):
                    result = m_obj.to_dict()
                elif hasattr(m_obj, "to_json"):
                    result = m_obj.to_json()
                else:
                    error = "to_dict/to_json メソッドがありません"
            except Exception as e:
                error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
