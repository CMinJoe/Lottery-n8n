# 使用官方的 n8n Docker 映像作為基礎
FROM n8nio/n8n:latest

# 保持 n8n 的默認入口點
ENTRYPOINT ["n8n"]
