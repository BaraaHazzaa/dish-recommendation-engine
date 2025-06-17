from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from app.services import initialize_models
import logging

app = create_app()

def retrain_recommendation_models():
    logging.info("Retraining recommendation models...")
    initialize_models()

if __name__ == '__main__':
    # Set up the scheduler to run the retraining function every 10 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(retrain_recommendation_models, 'interval', minutes=10)
    scheduler.start()

    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except (KeyboardInterrupt, SystemExit):
        pass  # Handle the exit gracefully
    finally:
        scheduler.shutdown()  # Shut down scheduler when the app stops
