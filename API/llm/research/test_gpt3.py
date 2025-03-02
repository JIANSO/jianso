import os
from openai import OpenAI
#########################################
# 테스트 완료 / 사용하지 않음
# gpt2 보다 훨씬 더 나은 응답 제공
# 문제 :: 유료
#########################################


# 환경 변수에서 API 키 불러오기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI 클라이언트 초기화 (API 키 설정 필요)
client = OpenAI(api_key=OPENAI_API_KEY)

# 사용자로부터 입력 받기
user_input = input("사용자: ")

# few-shot 설정을 위한 시스템 메시지 및 사용자 메시지 구성
if user_input.strip() == "도와줘":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "도와줘"},
        {"role": "assistant", "content": "무엇을 도와드릴까요?"}
    ]
else:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]

# 대화 생성 요청
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

# 응답 출력
response = completion.choices[0].message
print("response ::", response)