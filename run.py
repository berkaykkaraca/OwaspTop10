from app import app
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
if __name__ == "__main__":
    app.run(debug=True)
