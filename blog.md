# FastMCPとStreamlitで作る文字カウントアプリケーション

## はじめに

Model Context Protocol (MCP) は、AIアシスタントとさまざまなデータソースやツールとの相互作用を標準化することを目的としたオープンプロトコルです。今回は、FastMCPライブラリを使用してMCPサーバーとクライアントを構築し、さらにStreamlitでWebUIを提供する文字カウントアプリケーションを作成しました。

## プロジェクト構成

```
letter-counter/
├── server.py      # FastMCPサーバー
├── client.py      # FastMCPクライアント
├── main.py        # StreamlitによるWebアプリ
├── .env           # サーバーパス設定
└── pyproject.toml # プロジェクト設定
```

## 技術スタック

- **FastMCP**: MCPプロトコルの実装
- **Streamlit**: WebUIフレームワーク
- **asyncio**: 非同期処理
- **Python 3.12**: 実行環境

## 実装解説

### 1. FastMCPサーバー (`server.py`)

```python
from fastmcp import FastMCP

mcp = FastMCP("Letter Counter")

@mcp.tool()
def letter_counter(word: str, letter: str) -> int:
    """
    単語の中に文字が何回現れるかを数える。

    Args:
        word: 分析する単語またはフレーズ
        letter: 出現回数を数える文字

    Returns:
        単語中にその文字が現れる回数
    """
    return word.lower().count(letter.lower())

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**ポイント:**
- `@mcp.tool()` デコレータでツールを定義
- 大文字小文字を区別しない文字カウント機能
- STDIOトランスポートを使用してクライアントとの通信

### 2. FastMCPクライアント (`client.py`)

```python
import asyncio
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

def create_transport():
    server_script = os.getenv("SERVER_PATH")
    return PythonStdioTransport(script_path=server_script)

async def process_with_client(client: Client, word: str, letter: str):
    """既存のクライアントを使って処理を実行"""
    tools = await client.list_tools()
    print("ツール:", tools)

    result = await client.call_tool("letter_counter", {"word": word, "letter": letter})
    print("ツール呼び出し結果:", result)
    return result

async def count_letters_async(word: str, letter: str):
    """メイン処理"""
    transport = create_transport()

    async with Client(transport) as client:
        return await process_with_client(client, word, letter)
```

**ポイント:**
- `PythonStdioTransport`でサーバーとの通信を確立
- 非同期コンテキストマネージャーでクライアントを管理
- 環境変数からサーバーパスを取得

### 3. StreamlitによるWebアプリ (`main.py`)

```python
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
```

**ポイント:**
- Streamlitの直感的なUIコンポーネント
- `asyncio.run()`でクライアントの非同期処理を実行
- エラーハンドリングとユーザーフィードバック

## 実行方法

### 1. コマンドライン版
```bash
uv run client.py Strawberry r
```

### 2. WebUI版
```bash
uv run streamlit run main.py
```

## アーキテクチャの特徴

### 1. プロトコル標準化
MCPプロトコルにより、AIツールとの統合が標準化されています。これにより、将来的にClaude Desktopなどのクライアントから直接利用することも可能になります。

### 2. 分離されたコンポーネント
- **サーバー**: ビジネスロジックの処理
- **クライアント**: プロトコル通信の管理
- **UI**: ユーザーインターフェースの提供

### 3. 非同期処理
FastMCPの非同期処理により、スケーラブルなアプリケーションを構築できます。

## 学習のポイント

### FastMCPの理解
1. **ツール定義**: `@mcp.tool()`デコレータの使用方法
2. **トランスポート**: STDIOベースの通信メカニズム
3. **クライアント**: 非同期クライアントの使用パターン

### Streamlit統合
1. **非同期処理**: `asyncio.run()`によるブリッジング
2. **状態管理**: セッション状態とエラーハンドリング
3. **UX設計**: 直感的なユーザーインターフェース

## まとめ

このプロジェクトでは、FastMCPを使用してMCPサーバーとクライアントを構築し、Streamlitで使いやすいWebインターフェースを提供するアプリケーションを作成しました。

MCPプロトコルの採用により、将来的にはAIアシスタントから直接ツールを利用することも可能になり、より広範囲なエコシステムでの活用が期待できます。FastMCPとStreamlitの組み合わせは、プロトタイプから本格的なアプリケーションまで、幅広い用途で活用できる強力な技術スタックです。