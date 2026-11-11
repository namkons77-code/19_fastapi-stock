from datetime import datetime, timedelta

import FinanceDataReader as fdr
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Data API")

# React 개발 서버 연동을 위한 CORS 미들웨어 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_home():
    return {"message": "Stock Data API is running. Go to /samsung or /docs"}


@app.get("/samsung")
def read_samsung(days: int = 30):
    """삼성전자(005930) 주식 데이터를 가져와 JSON 형태로 반환합니다.

    - days: 조회할 일수 (기본값: 최근 30일)
    """
    # 시작 날짜 계산
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # FinanceDataReader를 통해 삼성전자(종목코드: 005930) 데이터 조회
    df = fdr.DataReader("005930", start=start_date)

    # 인덱스(Date)를 일반 컬럼으로 변환하고 문자열 포맷팅
    df = df.reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    # 결측치(NaN)가 있을 경우 JSON 호환을 위해 None으로 변환
    df = df.where(pd.notnull(df), None)

    return {
        "code": "005930",
        "name": "삼성전자",
        "days": days,
        "count": len(df),
        "data": df.to_dict(orient="records"),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
