from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "OPENAI_API_KEY"

PRICE_TABLE = {
    "전통된장1kg": 20000,
    "전통된장3kg": 53000,
    "전통된장5kg": 85000,
    "3년묵은된장1kg": 28000,
    "3년묵은된장3kg": 75000,
    "찹쌀고추장1kg": 30000,
    "찹쌀고추장3kg": 88000,
    "찹쌀고추장5kg": 140000,
    "고추장만들기3.5kg(용기미포함)": 50000,
    "고추장만들기7kg(용기미포함)": 83000,
    "고추장만들기용기: 5000,
    "현미보리고추장만들기7kg": 88000,
    "된장만들기3.5kg": 45000,
    "된장만들기7kg": 70000,
    "전통간장900ml": 12000,
    "전통간장1.8L": 23000,
    "청국장130g4개": 15000,
    "청국장130g12개": 39000,
    "청국장2kg": 36000,
    "청국장가루210g": 13200,
    "청국장가루1.2kg": 64000,
    "청국장가루1.5kg": 69000,
    "청국장환300g": 24000,
}

@app.route("/chat", methods=["POST"])
def chatbot():
    user_input = request.json.get("userRequest", {}).get("utterance", "")
    
    prompt = f"""다음 문장에서 제품명과 수량을 추출해 제품별 가격을 계산한 뒤 총액을 알려주세요. 
    가격표는 다음과 같습니다. 만약 합계가 30000 이하인 경우 배송비 3000을 추가해서 계산하여 총액을 알려주세요: {PRICE_TABLE}
    문장: "{user_input}" """

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    result = completion['choices'][0]['message']['content']

    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {"text": result + "\n\n입금계좌: 농협 351-0194-2025-33 (예금주: 안동제비원전통식품)"}
            }]
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run()
