from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

KAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
SHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# ログ設定
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
  {% if result %}
    <h2>📝 結果</h2>
    <div style="background:#f9f9f9;border:1px solid #ccc;padding:10px">
      {{ result | safe }}
    </div>
  {% endif %}
</body></html>
'''

app = Flask(__name__)

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
                m_obj = Meishiki(year, month, day, hour)
                app.logger.info("Meishiki生成 OK: %s", dir(m_obj))

                nikkan = KAN[m_obj.nikkan % 10]
                chishi = SHI[m_obj.chishi % 12]

                result = f"""
                🌸 <strong>名前:</strong> {name}<br>
                🌞 <strong>日干支:</strong> {nikkan}{chishi}<br>
                🔢 <strong>十干番号:</strong> {m_obj.nikkan}<br>
                🧬 <strong>性別コード:</strong> {m_obj.sex}
                """
        except Exception as e:
            app.logger.error("内部エラー: %s", e)
            error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
