from flask import Flask, jsonify
from datetime import datetime, timedelta
from database import SessionLocal, Article
from flask_cors import CORS
import sqlalchemy
import os

app = Flask(__name__)
CORS(app)
@app.route('/api/scores', methods=['GET'])
def get_scores():
    db = SessionLocal()
    try:
        # Get current UTC time
        utc_now = datetime.utcnow()
        # EST is UTC-5 (standard time), so subtract 5 hours
        est_offset = timedelta(hours=-5)
        est_now = utc_now + est_offset
        five_hours_ago = est_now - timedelta(hours=12)
        results = db.query(Article.ticker, sqlalchemy.func.avg(Article.score).label('avg_score'))\
                   .filter(Article.timestamp >= five_hours_ago)\
                   .group_by(Article.ticker)\
                   .all()

        return jsonify([{ "ticker": r[0], "avg_score": r[1] } for r in results])
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ(PORT)))
