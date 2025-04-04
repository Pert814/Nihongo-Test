from google import genai
import json
import os
import csv
from dotenv import load_dotenv

def generate_JLPT_questions(N:int, number_of_questions:int = 10):
    if not isinstance(N, int) or N not in range(1, 6):
        raise ValueError("N 必須是 1 到 5 之間的整數！")
    else:
        # 使用 Google GenAI API 生成問題
        # 請確保您已經設置好 GOOGLE_APPLICATION_CREDENTIALS 環境變數，並且有正確的 API 金鑰
        # 這裡的 API_KEY 是示範用的，請替換為您的實際 API 金鑰
        load_dotenv()  # 自動載入 .env 檔案中的環境變數
        API_KEY = os.getenv("MY_GOOGLE_API_KEY")
        prompt = f"給我多樣化.不重複的{number_of_questions}題JLPT N{N}難度的單字填空4選1選擇題，包括：詞彙填空（文脈判斷）.類義詞選擇.反義詞選擇.熟語・慣用語填空.外來語應用.動詞活用填空.漢字讀音測驗.日文同音異義詞測驗，並輸出成json，欄位包含ID,Category,Question,Option A,Option B,Option C,Option D,Answer，Answer只要A.B.C.D其中之一就好，回傳json格式"

        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            )

        # 嘗試解析 JSON
        start = response.text.find("[")  # 找到 "[" 的位置
        end = response.text.find("]")    # 找到 "]" 的位置

        if start != -1 and end != -1:  # 確保找到標記
            result = response.text[start:end+1]  # 包含 "]"
        else:
            print("未找到json格式的資料")

        # 將結果轉換為 JSON 格式
        try:
            json_data = json.loads(result)
        except json.JSONDecodeError as e:
            print("JSON 解析錯誤:", e)
            json_data = None

        # 確保json_data長度符合number_of_questions
        if json_data and len(json_data) != number_of_questions:
            print(f"生成的問題數量不正確，預期 {number_of_questions} 題，但實際生成了 {len(json_data)} 題。")
            return

        # 將 json_data 寫成dict 並匯出成csv檔案存入data資料夾
        if json_data:

            # 確保資料夾存在
            data_folder = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_folder, exist_ok=True)

            # 定義 CSV 檔案名稱
            csv_file_name = os.path.join(data_folder, f"N{N}_{number_of_questions}_questions.csv")  # 更新 CSV 檔案路徑

            # 確保檔案不存在，否則刪除
            if os.path.exists(csv_file_name):
                os.remove(csv_file_name)

            # 寫入 CSV 檔案
            with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # 寫入標題行
                writer.writerow(["ID", "Category", "Question", "Option A", "Option B", "Option C", "Option D", "Answer"])
                # 寫入資料行
                for item in json_data:
                    writer.writerow([item["ID"], item["Category"], item["Question"], item["Option A"], item["Option B"], item["Option C"], item["Option D"], item["Answer"]])
            print(f"CSV 檔案 '{csv_file_name}' 已成功生成。")


generate_JLPT_questions(N=3, number_of_questions=10)









