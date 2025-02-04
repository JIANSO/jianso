from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoTokenizer
import torch

# 모델과 토크나이저 로드
#tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#model = GPT2LMHeadModel.from_pretrained("gpt2")

# KoGPT2 모델과 토크나이저 로드
# 응답이 너무 이상하게 나와서 이 부분 조정 - 소
tokenizer = AutoTokenizer.from_pretrained("skt/kogpt2-base-v2")
model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2")

# 사용자로부터 실시간 입력 받기
user_input = input("사용자 입력:: ")

# 사용자 입력에 따라 다른 프롬프트 설정
if user_input.strip() == "도와줘":
    ai_response = "테스트 중입니다."
    
    input_text = f"사용자: {user_input}\nAI: {ai_response}\n"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
else:
    # 입력 텍스트를 모델이 처리할 수 있도록 인코딩
    input_ids = tokenizer.encode(f"{user_input}", return_tensors='pt')

# attention_mask 생성
attention_mask = torch.ones(input_ids.shape)  # 모든 입력 토큰에 주목하도록 설정

# 모델로부터 응답 생성
# 응답이 너무 이상하게 나와서 이 부분 조정 - 소
outputs = model.generate(
    input_ids
)

# 생성된 출력 디코딩 및 출력
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("response ::", response)
