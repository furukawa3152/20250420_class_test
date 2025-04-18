from openai import OpenAI
import os

class get_openai_response:
    def __init__(self, model: str):
        self.client = OpenAI(api_key=os.environ["API_KEY"])
        self.model = model
    def get_response(self, question: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model= self.model,
                messages=[
                    {"role": "system", "content": "日本語で簡潔に回答してください。"},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"エラーが発生しました: {e}"


class DetailedOpenAIResponse(get_openai_response):  # 基本クラスを継承
    # __init__は書かなくてよい。上のクラスを継承するので。
    def get_response(self, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "日本語で詳細に回答してください。"},
                {"role": "user", "content": question}
            ],
        )
        return response.choices[0].message.content


# 共通ベースクラス：OpenAIクライアントを外から注入
class OpenAIResponder:
    def __init__(self, client,model):
        self.client = client
        self.model = model
    def get_response(self, user_prompt: str, system_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"エラーが発生しました: {e}"


class SimpleResponder(OpenAIResponder):
    def get_response(self, user_prompt: str) -> str:
        return super().get_response(
            user_prompt,
            system_prompt="日本語で簡潔に回答してください。"
        )


# 詳細に答える用
class DetailedResponder(OpenAIResponder):
    def get_response(self, user_prompt: str) -> str:
        return super().get_response(
            user_prompt,
            system_prompt="日本語で詳細に回答してください。"
        )


# 使用例
if __name__ == "__main__":
    question = "pythonとは"

    # 継承
    # model = "gpt-4o-mini"
    # response_basic = get_openai_response(model)
    # print(response_basic.get_response(question))
    #
    # response_detailed = DetailedOpenAIResponse(model)
    # print(response_detailed.get_response(question))

    client = OpenAI(api_key=os.environ["API_KEY"])
    simple = SimpleResponder(client,model="gpt-4o-mini")
    print(simple.get_response(question))

    detailed = DetailedResponder(client,model="gpt-4o-mini")
    print(detailed.get_response(question))
