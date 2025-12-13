import asyncio
from fastapi import FastAPI
from sqlmodel import Session
from app.database import get_session
from app.services.recommender import RecommenderService

recommender = RecommenderService()


async def periodic_training(app: FastAPI, interval: int = 86400):  # 24h default
    """Run recommender training every `interval` seconds."""
    while True:
        print("🔄 Auto-training recommender...")
        with next(get_session()) as session:  # open DB session
            ok = recommender.train(session)
            print("✅ Training complete" if ok else "⚠️ No data to train yet")
        await asyncio.sleep(interval)
