---
title: A2A 协议学习
date: 2025-06-19
---

### 启动专门负责汇率计算的 Agent

该 Agent 能够实时的访问各种国家的货币汇率信息。

![image-20250619091923344](http://cdn.jayh.club/uPic/image-20250619091923344AUsygn.png)

```sh
 uv run .
INFO:__main__:Starting server on localhost:10000
INFO:     Started server process [42799]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:10000 (Press CTRL+C to quit)
INFO:     127.0.0.1:59793 - "GET / HTTP/1.1" 405 Method Not Allowed
INFO:     127.0.0.1:59793 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60325 - "GET /.well-known/agent.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:63998 - "GET /.well-known/agent.json HTTP/1.1" 200 OK
INFO:common.server.task_manager:Upserting task b0b996b7-252f-44f7-8674-6c190d1ad105



WARNING:langchain_google_genai.chat_models:Retrying langchain_google_genai.chat_models._chat_with_retry.<locals>._chat_with_retry in 2.0 seconds as it raised RetryError: Timeout of 600.0s exceeded, last exception: 503 failed to connect to all addresses; last error: UNAVAILABLE: ipv4:172.253.117.95:443: Failed to connect to remote host: Timeout occurred: FD shutdown.
```

![image-20250619091822483](http://cdn.jayh.club/uPic/image-202506190918224830RoB9H.png)

![](http://cdn.jayh.club/uPic/image-2025061909203948657kaxj.png)

![](http://cdn.jayh.club/uPic/image-20250619092545627xTdvcr.png)

汇率换算

![](http://cdn.jayh.club/uPic/image-2025061914190239655Q48Z.png)

![image-20250619142235065](http://cdn.jayh.club/uPic/image-20250619142235065d8E2OC.png)
