---
title: 申请阿里百炼 api key
date: 2025-06-16
---

阿里百炼

https://bailian.console.aliyun.com/?tab=model#/api-key

遇到的问题和经验总结：
1、示例中的 openai 不是一般人能用的，首先得学术上网，然后还得申请一个 openai 的 api key，还需要充值。
2、.env 文件需要自己创建一个，Google 的那个 api key 不需要。如果你访问不了 openai，就用阿里云百炼。官网：https://bailian.console.aliyun.com/?tab=model#/api-key
3、示例代码的文件名和目录名和文章中的不一样，需要自己调整下，比如 client 和 server 目录，特别注意 client 中的有个 mcp server 的路径，是一个绝对路径，我用的 MacOS，路径前面一段必须是 “/Users/wukong/”，不能是“～”，否则会报找不到路径。
4、我用的 deepseek 作为推理大模型， 直接用这个命令跑就行，uv run client-v3-deepseek.py ../rag-server/server.py
5、索引的文档只有几种病症，都放在 medical_docs 变量里面在，如果你输入一个 感冒，就会检索不到。不要以为是程序问题，自己再一个文档丢进去就行。
6、另外我做了一个好玩的事情，我加了一个感冒的文档，但是对感冒的描述是错的，最后的现象是 能检索到这个文档，但是将问题+文档检索到的内容丢给大模型时，大模型会告诉我文档有明显的问题。AI 回答：“根据提供的文档内容，关于感冒的描述存在明显错误或不准确的信息。文档中提到的感冒特征为"血糖水平持续降低"[5]，这与医学上对感冒（上呼吸道病毒感染）的认知完全不符。”
7、将 openai 替换为 阿里云百炼的代码如下。官网文档有示例代码，需要注意的是维度需要改成一样的，1536。
client = OpenAI(
api_key=os.getenv("DASHSCOPE_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" # 百炼服务的base_url
)

async def embed_text(texts: List[str]) -> np.ndarray:
resp = client.embeddings.create(
model="text-embedding-v4",
input=texts,
dimensions=1536,# 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
encoding_format="float"
)
return np.array([d.embedding for d in resp.data], dtype='float32')
