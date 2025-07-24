from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import aiomysql

# 使用通义千问通义千问
DASHSCOPE_API_KEY = "sk-c268f16163084457ad1b8218e6c7a91b"

client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

app = FastAPI()

# 解决前后端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库连接池
db_pool = None

@app.on_event("startup")
async def startup_event():
    global db_pool
    db_pool = await aiomysql.create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        db="aiproject",
        autocommit=True
    )

@app.on_event("shutdown")
async def shutdown_event():
    db_pool.close()
    await db_pool.wait_closed()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    user_id = data.get("userId", "anonymous")  # 如果前端没传就匿名

    try:
        #调用大模型
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个聪明的中文助手"},
                {"role": "user", "content": user_message},
            ]
        )
        reply = response.choices[0].message.content.strip()

        #存入数据库
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO chat_history (user_id, message, reply) VALUES (%s, %s, %s)",
                    (user_id, user_message, reply)
                )

        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
