import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

# 環境変数を読み込み
load_dotenv()

# Streamlitページの設定
st.set_page_config(
    page_title="専門家AI相談アプリ",
    page_icon="🤖",
    layout="wide"
)

# タイトルと説明
st.title("🤖 専門家AI相談アプリ")
st.write("このアプリでは、選択した専門家の立場からAIが回答します。")

# 操作方法の説明
st.markdown("""
### 📋 操作方法
1. **専門家を選択**: ラジオボタンで相談したい専門家を選んでください
2. **質問を入力**: テキストエリアに相談内容を入力してください  
3. **回答を取得**: 「回答を取得」ボタンを押すと、選択した専門家の立場からAIが回答します
4. **結果確認**: 画面下部に専門家からの回答が表示されます
""")

st.divider()

# 専門家選択のラジオボタン
expert_type = st.radio(
    "相談したい専門家を選択してください：",
    ["医師", "弁護士", "栄養士"]
)

# 入力フォーム
user_input = st.text_area(
    "相談内容を入力してください：",
    height=150,
    placeholder="ここに相談したい内容を詳しく入力してください..."
)

# LLMに問い合わせる関数を定義
def get_expert_response(input_text, expert_choice):
    """
    入力テキストと専門家選択を受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーの入力テキスト
        expert_choice (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    try:
        # OpenAI APIキーの設定
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 専門家に応じたシステムメッセージを設定
        if expert_choice == "医師":
            system_content = "あなたは経験豊富な医師です。患者からの相談に対して、医学的知識に基づいた適切なアドバイスを提供してください。ただし、最終的には医療機関での診察を勧めることも忘れずに。"
        elif expert_choice == "弁護士":
            system_content = "あなたは経験豊富な弁護士です。法的な相談に対して、関連する法律や判例に基づいた適切なアドバイスを提供してください。ただし、具体的な法的判断については専門の法律相談を勧めることも重要です。"
        elif expert_choice == "栄養士":
            system_content = "あなたは経験豊富な栄養士です。食事や栄養に関する相談に対して、栄養学の知識に基づいた適切なアドバイスを提供してください。個人の体質や健康状態に配慮したアドバイスを心がけてください。"
        
        # メッセージリストを作成
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=input_text)
        ]
        
        # LLMを実行して回答を取得
        result = llm(messages)
        
        return result.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# 回答取得ボタン
if st.button("🤖 回答を取得", type="primary"):
    if user_input.strip():
        with st.spinner(f"{expert_type}が回答を準備中..."):
            # 関数を使用してLLMから回答を取得
            response = get_expert_response(user_input, expert_type)
            
            # 回答を表示
            st.success("回答が完了しました！")
            
            st.subheader(f"👨‍⚕️ {expert_type}からの回答")
            st.write(response)
            
    else:
        st.warning("相談内容を入力してください。")

# フッター
st.divider()
st.markdown("※ このアプリはAIによる参考回答です。重要な決定には専門家への直接相談をお勧めします。")