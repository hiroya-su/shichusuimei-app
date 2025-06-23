import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

from flask import Flask, request, render_template_string
from meishiki import Meishiki
app = Flask(__name__)


# HTML は省略（そのままでOK）

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        name_s   = request.form.get("name", "").strip()
        year_s   = request.form.get("year", "").strip()
        month_s  = request.form.get("month", "").strip()
        day_s    = request.form.get("day", "").strip()
        hour_s   = request.form.get("hour", "").strip()

        if not (name_s and year_s and month_s and day_s and hour_s):
            error = "全ての項目を入力してください"
        else:
            try:
                year  = int(year_s)
                month = int(month_s)
                day   = int(day_s)
                hour  = int(hour_s)

                m = Meishiki(year, month, day, hour)
                logging.info("Meishiki dir: %s", dir(m))

                if hasattr(m, "to_dict"):
                    result = m.to_dict()
                elif hasattr(m, "to_json"):
                    result = m.to_json()
                else:
                    error = "to_dict/to_json メソッドがありません"
            except ValueError:
                error = "年/月/日/時 には数字を入力してください"
            except Exception as e:
                error = f"実行時エラー: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
