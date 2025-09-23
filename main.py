import asyncio
import streamlit as st
from client import count_letters_async

def main():
    st.title("文字カウンター")
    st.write("単語の中に特定の文字が何回現れるかを数えます")

    word = st.text_input("単語またはフレーズを入力してください:", value="Strawberry")
    letter = st.text_input("カウントする文字を入力してください:", value="r")

    if st.button("カウント実行"):
        if word and letter:
            try:
                result = asyncio.run(count_letters_async(word, letter))
                letter_count = result.content[0].text if result.content else 0
                st.success(f"'{word}' の中に '{letter}' は **{letter_count}** 回現れます")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("単語と文字の両方を入力してください")

if __name__ == "__main__":
    main()
