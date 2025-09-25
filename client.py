import asyncio
import argparse
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

import os
from dotenv import load_dotenv

load_dotenv()

def create_transport():
    # サーバースクリプトのパス
    server_script = os.getenv("SERVER_PATH")
    # PythonStdioTransportを使用してサーバを起動
    return PythonStdioTransport(script_path=server_script)

async def process_with_client(client: Client, word: str, letter: str):
    """既存のクライアントを使って処理を実行"""
    # 利用可能なツールを取得
    tools = await client.list_tools()
    print("ツール:", tools)

    # ツールの呼び出し
    result = await client.call_tool("letter_counter", {"word": word, "letter": letter})
    print("ツール呼び出し結果:", result)
    return result

async def count_letters_async(word: str, letter: str):
    """メイン処理"""
    transport = create_transport()

    async with Client(transport) as client:
        return await process_with_client(client, word, letter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FastMCP Letter Counter Client')
    parser.add_argument('word', nargs='?', help='カウント対象の単語')
    parser.add_argument('letter', nargs='?', help='カウントする文字')
    
    args = parser.parse_args()
    
    if not args.word or not args.letter:
        print("❌ エラー: wordとletterの両方を指定してください")
        
    else:
        asyncio.run(count_letters_async(args.word, args.letter))

