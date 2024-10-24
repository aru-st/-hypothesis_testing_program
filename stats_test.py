import streamlit as st
import random
import itertools
import numpy as np
import pandas as pd
from scipy import stats

#/***********/
#/* 処理実装 */
#/***********/

def process(al, freedom, ave, st_er):
    rejection = stats.t.interval(1 - al, df = freedom, loc = ave, scale = st_er)  #棄却域
    st.write("棄却域：" + str(rejection))

    if st.session_state.mu < rejection[0] or st.session_state.mu > rejection[1]:
        st.write("帰無仮説は棄却される")
    else:
        st.write("帰無仮説は棄却されない")

#/*******************/
#/* Streamlitの実装 */
#/*  UI, 入力部分   */
#/*******************/

st.session_state.flag = False #検定を行うかどうかのフラグ

#マークダウン記法での記述

def main():
    # タイトルを設定
    st.title('検定できるプログラム')

    # ファイルアップロード機能
    uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "xls"])

    # ファイルがアップロードされた場合の処理
    if uploaded_file is not None:
        # pandasでExcelファイルを読み込む
        df = pd.read_excel(uploaded_file)

        # アップロードしたファイルの内容を表示
        st.write("アップロードされたファイルの内容:")
        st.dataframe(df)

        # カラムの選択
        columns = df.columns.tolist()
        selected_columns = st.multiselect("検定したいカラムを選択してください", columns)

        # ユーザーがカラムを選択した場合の処理
        if selected_columns and len(selected_columns) < 2:

            st.session_state.flag = True

            #st.write(type(selected_columns)) #Debug

            selected_data = df[selected_columns]
            st.write("選択されたカラムの内容:")
            st.dataframe(selected_data)

            #各種統計量の計算
            st.session_state.ave = selected_data.mean().iloc[0]
            st.session_state.u = selected_data.std().iloc[0]
            st.session_state.n = len(selected_data)
            st.session_state.se = st.session_state.u / np.sqrt(st.session_state.n)

            st.write("各種統計量を表示します")
            st.write(f"標本平均: {st.session_state.ave}")
            st.write(f"不偏分散: {st.session_state.u}")
            st.write(f"データ数: {st.session_state.n}")
            st.write(f"標準誤差: {st.session_state.se}")
        else:
            st.write("選択するカラムは１つまでにしてください")


    # 実行する世代数を設定
    st.session_state.alpha = st.number_input("有意水準α")
    st.session_state.mu = st.number_input("帰無仮説の平均値")

    #if st.button("Weight, Value List Validation!"):
    #    st.write(st.session_state.W)
    #    st.write(st.session_state.V)

    if st.button("仮説検定をする") and st.session_state.flag and (st.session_state.alpha > 0 and st.session_state.alpha < 1):
        rejection = stats.t.interval(1 - st.session_state.alpha, df = st.session_state.n - 1, loc = st.session_state.mu, scale = st.session_state.se)  #棄却域
        st.write(f"棄却域は{rejection[0]}以上{rejection[1]}以下です。")
        st.write("標本平均がこの棄却域の中に入っていなければ棄却されます")

        if st.session_state.ave < rejection[0] or st.session_state.ave > rejection[1]:
            st.write("帰無仮説は棄却される")
        else:
            st.write("帰無仮説は棄却されない")
    else:
        print("検定に使う列を選択してください")

if __name__ == "__main__":
    main()
