# from flask import Flask, jsonify
# from datetime import datetime, timedelta
# from database import SessionLocal, Article
# from flask_cors import CORS
# import sqlalchemy
# import os

# app = Flask(__name__)
# CORS(app)
# @app.route('/api/scores', methods=['GET'])
# def get_scores():
#     db = SessionLocal()
#     try:
#         # Get current UTC time
#         utc_now = datetime.utcnow()
#         # EST is UTC-5 (standard time), so subtract 5 hours
#         est_offset = timedelta(hours=-5)
#         est_now = utc_now + est_offset
#         five_hours_ago = est_now - timedelta(hours=12)
#         results = db.query(Article.ticker, sqlalchemy.func.avg(Article.score).label('avg_score'))\
#                    .filter(Article.timestamp >= five_hours_ago)\
#                    .group_by(Article.ticker)\
#                    .all()

#         return jsonify([{ "ticker": r[0], "avg_score": r[1] } for r in results])
#     finally:
#         db.close()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ(PORT)))
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
        
        results = db.query(
            Article.ticker,
            sqlalchemy.func.avg(Article.score).label('avg_score'),
            sqlalchemy.func.max(Article.score).label('max_score')
        ).filter(
            Article.timestamp >= five_hours_ago
        ).group_by(Article.ticker).all()

        return jsonify([
            { "ticker": r[0], "avg_score": r[1], "max_score": r[2] } for r in results
        ])
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


# from flask import Flask, jsonify, request
# from datetime import datetime, timedelta
# from database import SessionLocal, Article
# from flask_cors import CORS
# import sqlalchemy
# import os

# app = Flask(__name__)
# CORS(app)

# @app.route('/api/scores', methods=['GET'])
# def get_scores():
#     db = SessionLocal()
#     try:
#         # Get input timestamps from query parameters
#         start_time_str = request.args.get('start')
#         end_time_str = request.args.get('end')

#         if not start_time_str or not end_time_str:
#             return jsonify({"error": "Missing 'start' or 'end' query parameter."}), 400

#         # Parse input timestamps
#         try:
#             start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
#             end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
#         except ValueError:
#             return jsonify({"error": "Invalid timestamp format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

#         if start_time > end_time:
#             return jsonify({"error": "Start time must be earlier than end time."}), 400

#         # Align input timestamps (EST) to UTC for querying the database
#         utc_start_time = start_time + timedelta(hours=5)  # Convert EST to UTC
#         utc_end_time = end_time + timedelta(hours=5)  # Convert EST to UTC

#         # Calculate results for each hour in the range
#         hourly_results = []
#         current_time = utc_start_time

#         while current_time <= utc_end_time:
#             next_time = current_time + timedelta(hours=1)
#             five_hours_ago = current_time - timedelta(hours=5)

#             results = db.query(
#                 Article.ticker,
#                 sqlalchemy.func.avg(Article.score).label('avg_score'),
#                 sqlalchemy.func.max(Article.score).label('max_score')
#             ).filter(
#                 Article.timestamp >= five_hours_ago,
#                 Article.timestamp < current_time
#             ).group_by(Article.ticker).all()

#             hourly_results.append({
#                 "hour": (current_time - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),  # Convert back to EST
#                 "scores": [
#                     {"ticker": r[0], "avg_score": r[1], "max_score": r[2]} for r in results
#                 ]
#             })

#             current_time = next_time

#         return jsonify(hourly_results)
#     finally:
#         db.close()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

