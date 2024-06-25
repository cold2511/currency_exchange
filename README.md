# Currency Exchange Web Application

A Flask-based web application for user authentication, location sharing, and chat functionality, integrated with MongoDB for data storage.

## Features

- User Signup and Login
- Location Sharing
- Chat between users
- Find users within a certain distance

## Prerequisites

- Python 3.7+
- MongoDB

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/cold2511/currency_exchange.git
    cd currency_exchange
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up MongoDB:**

    Ensure MongoDB is installed and running on your machine. By default, the app connects to a local MongoDB instance:

    ```plaintext
    mongodb://localhost:27017/
    ```

    If your MongoDB instance is different, update the connection string in the app.

6. **Set up environment variables:**

    Create a `.env` file in the project root directory and add the following:

    ```env
    SECRET_KEY=your_secret_key
    ```

## Running the Application

1. **Start the Flask application:**

    ```bash
    python app.py
    ```

2. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

### User Signup

- Navigate to `/signup` to create a new user account.

### User Login

- Navigate to `/` to log in with your username and password.

### Location Sharing

- After logging in, share your location using the `/share_location` route.

### Finding Nearby Users

- Use the `/find` route to find users within a certain distance from your location.

### Chat

- Use the `/chat` route to send and receive messages from other users with the same code.

## Project Structure

- `app.py`: Main application file
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.

