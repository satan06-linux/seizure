# 🚀 Deployment Guide

## Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app"
5. Select repository and branch
6. Set main file: `app.py`
7. Click "Deploy"

## Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create seizureguard-ai
git push heroku main
```

## Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t seizureguard-ai .
docker run -p 8501:8501 seizureguard-ai
```

## Option 4: AWS EC2

1. Launch EC2 instance (Ubuntu)
2. SSH into instance
3. Install dependencies
4. Clone repository
5. Run with screen/tmux
6. Configure security groups (port 8501)

## Environment Variables

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```
