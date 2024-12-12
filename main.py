from flask import Flask, jsonify
from datetime import datetime, timedelta
from database import SessionLocal, Article
import os

app = Flask(__name__)

@app.route('/api/scores', methods=['GET'])
def get_scores():
    db = SessionLocal()
    try:
        five_hours_ago = datetime.utcnow() - timedelta(hours=5)
        results = db.query(Article.ticker, sqlalchemy.func.avg(Article.score).label('avg_score'))\
                   .filter(Article.timestamp >= five_hours_ago)\
                   .group_by(Article.ticker)\
                   .all()

        return jsonify([{ "ticker": r[0], "avg_score": r[1] } for r in results])
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ(PORT)))
