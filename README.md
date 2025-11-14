# Rasa Chatbot

## Deployment trên Render.com

1. Tạo tài khoản tại https://render.com
2. Kết nối với GitHub repository này
3. Chọn Web Service
4. Build Command: `pip install -r requirements.txt && rasa train`
5. Start Command: `rasa run --enable-api --cors "*" --port $PORT`

## Local Development

```bash
rasa train
rasa run --enable-api --cors "*"
```
