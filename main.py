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
from flask import Flask, jsonify, request
from database import SessionLocal, Article, Tweet
from flask_cors import CORS
import sqlalchemy
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/api/scores', methods=['GET'])
def get_scores():
    db = SessionLocal()
    try:
        # Parse query parameters for start and end timestamps
        start_time = request.args.get('start', default=None, type=str)
        end_time = request.args.get('end', default=None, type=str)

        if not start_time or not end_time:
            return jsonify({"error": "Please provide both start and end timestamps."}), 400

        # Convert strings to datetime
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 format (e.g., '2024-12-19T08:00:00')."}), 400

        # Calculate scores for each hour in the range
        results = []
        current_time = start_time
        while current_time <= end_time:
            # Calculate the 5-hour range
            range_start = current_time - timedelta(hours=5)
            range_end = current_time

            # Query scores within the 5-hour range
            scores = db.query(
                Article.ticker,
                sqlalchemy.func.avg(Article.score).label('avg_score'),
                sqlalchemy.func.max(Article.score).label('max_score'),
                sqlalchemy.func.min(Article.score).label('min_score'),
                sqlalchemy.func.stddev(Article.score).label('std_dev')
            ).filter(
                Article.timestamp >= range_start,
                Article.timestamp < range_end
            ).group_by(Article.ticker).all()

            # Append results
            for r in scores:
                results.append({
                    "ticker": r[0],
                    "hour": current_time.isoformat(),
                    "avg_score": r[1],
                    "max_score": r[2],
                    "min_score": r[3],
                    "std_dev": r[4],
                })

            # Move to the next hour
            current_time += timedelta(hours=1)

        return jsonify(results)

    finally:
        db.close()

@app.route('/api/tweet_scores', methods=['GET'])
def get_tweet_scores():
    """
    Endpoint to get sentiment scores for tweets within a specific time range.
    The `date` column is stored as a proper `timestamp`.
    Accepts input in ISO 8601 format (e.g., '2024-12-19T08:00:00').
    """
    db = SessionLocal()
    try:
        # Parse query parameters for start and end timestamps
        start_time = request.args.get('start', default=None, type=str)
        end_time = request.args.get('end', default=None, type=str)

        if not start_time or not end_time:
            return jsonify({"error": "Please provide both start and end timestamps."}), 400

        # Convert ISO 8601 strings to datetime objects
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 format (e.g., '2024-12-19T08:00:00')."}), 400

        # Calculate scores for each hour in the range
        results = []
        current_time = start_time
        while current_time <= end_time:
            # Calculate the 5-hour range
            range_start = current_time - timedelta(hours=5)
            range_end = current_time

            # Query scores within the 5-hour range
            scores = db.query(
                Tweet.ticker,
                sqlalchemy.func.avg(Tweet.score).label('avg_score'),
                sqlalchemy.func.max(Tweet.score).label('max_score'),
                sqlalchemy.func.min(Tweet.score).label('min_score'),
                sqlalchemy.func.stddev(Tweet.score).label('std_dev')
            ).filter(
                Tweet.timestamp >= range_start,
                Tweet.timestamp < range_end
            ).group_by(Tweet.ticker).all()

            # Append results
            for r in scores:
                results.append({
                    "ticker": r[0],
                    "hour": current_time.isoformat(),  # Keep ISO 8601 format in the response
                    "avg_score": r[1],
                    "max_score": r[2],
                    "min_score": r[3],
                    "std_dev": r[4],
                })

            # Move to the next hour
            current_time += timedelta(hours=1)

        return jsonify(results)

    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))


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

