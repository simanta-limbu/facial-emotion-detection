# facial-emotion-detection
App Development Final Project

This repository contains a facial emotion detection application that uses machine learning to identify emotions in images. The application is built using Flask, a Python web framework, and leverages a pre-trained model for emotion recognition.

The project is inspired by and makes use of the resources from the facial-emotion-detection-webapp repository.
Getting Started

Follow these instructions to set up the project on your local machine for development and testing purposes.
Prerequisites

    Python 3.6 or higher
    Git

Installing Dependencies

    Clone the repository:

    bash

git clone https://github.com/simanta-limbu/facial-emotion-detection.git
cd facial-emotion-detection

Create a virtual environment and activate it:

bash

python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
.\venv\Scripts\activate   # For Windows

Install the required Python packages:

    pip install -r requirements.txt

Running the Application

    Run the Flask application:

    bash

    export FLASK_APP=app.py   # For Linux/macOS
    set FLASK_APP=app.py      # For Windows
    flask run

    Open your web browser and visit http://127.0.0.1:5000/ to access the application.

Usage

    Register a new user or log in with an existing account.
    Upload an image containing a face for emotion detection.
    The application will process the image and display the detected emotion.
    You can save the result to your dashboard, view saved results, or delete saved images.

Contributing

Please feel free to submit issues, fork the repository, and send pull requests.
License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements

    Pawandeep-prog/facial-emotion-detection-webapp for the inspiration and resources.
