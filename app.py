from flask import Flask, request, render_template_string
from meishiki import Meishiki
import logging

KAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
SHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

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
  {% if result %}<h2>📝 結果</h2><pre>{{ result }}</pre>{% endif %}
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
                app.logger.info("chishi の値: %s", m_obj.chishi)
                app.logger.info("Meishiki生成 OK: %s", dir(m_obj))

                # 干支の配列
                KAN = "甲乙丙丁戊己庚辛壬癸"
                SHI = "子丑寅卯辰巳午未申酉戌亥"

                # 干支の文字列を取得（インデックス範囲をチェック）
                try:
                    nikkan = KAN[m_obj.nikkan] if 0 <= m_obj.nikkan < len(KAN) else "不明"
                except Exception:
                    nikkan = "不明"

                try:
                    chishi = SHI[m_obj.chishi] if 0 <= m_obj.chishi < len(SHI) else "不明"
                except Exception:
                    chishi = "不明"

                result = f"""
                🌸 名前: {name}
                🌞 日干支: {nikkan}{chishi}
                🔢 十干番号: {m_obj.nikkan}
                🧬 性別コード: {m_obj.sex}
                """

            except Exception as e:
                error = f"内部エラー: {e}"

    return render_template_string(HTML, result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
