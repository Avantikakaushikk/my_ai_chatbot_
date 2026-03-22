#!/bin/bash
cd "$(dirname "$0")"

echo "Starting Chatbot Backend (uvicorn)..."
cd backend
../venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

cd ..
echo "Starting Chatbot Frontend (streamlit)..."
venv/bin/streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!

sleep 3
open http://localhost:8501

echo "Both servers are running! Close this terminal window to stop them."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
