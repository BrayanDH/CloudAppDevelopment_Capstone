# Dealership Review App

This project is a Dealership Review Web Application developed using Django, a popular web application framework for Python. The primary objective of this project is to allow users to review and rate car dealerships and their services. Additionally, this version of the app includes an IBM Sentiment Analyzer feature that analyzes the sentiment of user reviews and provides feedback on whether the review is positive, negative, or neutral.

## Features

- User Authentication: Users can create accounts, log in, and log out.
- Dealership List: Users can view a list of car dealerships available in the app.
- Dealership Details: Users can see reviews for a specific car dealership.
- Review Submission: Authenticated users can submit reviews for car dealerships.
- IBM Sentiment Analyzer: The app analyzes the sentiment of user reviews and provides feedback on the review's sentiment.

## Installation and Setup

Install Docker on your machine: [Docker Installation Guide ](https://docs.docker.com/engine/install/)

- Clone this repository:

  ```
  git clone https://github.com/BrayanDH/Dealership_Review_App-Sentiment_Analyzer_and_Django-.git
  ```

- Navigate to the project directory:

  ```
  cd Dealership_Review_App-Sentiment_Analyzer_and_Django-\server
  ```

- Build the Docker container:

  ```
  docker build -t dealership_review_app .
  ```

- Run the container:

  ```
  docker run -p 8080:8080 dealership_review_app
  ```

- Open your web browser and visit http://localhost:8000/djangoapp/ to access the Dealership Review App.

To run the Todo App locally without docker, follow these steps:

Install Python 3.8 on your machine: [Python Installation](https://www.python.org/downloads/)

1. Clone the repository:

   ```
   git clone https://github.com/BrayanDH/Dealership_Review_App-Sentiment_Analyzer_and_Django-.git
   ```

2. Navigate to the project directory:

   ```
   cd Dealership_Review_App-Sentiment_Analyzer_and_Django-\server
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations(only the first time):

   ```
   python manage.py migrate
   ```

5. Create a superuser (Admin) to manage the app(only the first time):

   ```
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```
   python manage.py runserver
   ```

7. Open your web browser and visit http://localhost:8000/djangoapp/ to access the Dealership Review App.

## Dependencies

The Dealership Review App utilizes the following dependencies:

- Django
- Requests (for making API calls)

Please refer to the requirements.txt file for the complete list of dependencies and their versions.

## Usage

### About

The "About" page provides static information about the Dealership Review App.

### Contact

The "Contact" page is a static contact form for users to reach out to the website administrators.

### Login

The "Login" page allows users to log in to the app. If the user is already logged in, they will be redirected to the homepage.

### Registration

The "Registration" page allows new users to sign up for an account. If the provided username already exists, the user will be prompted to choose a different username.

### Index (Homepage)

The "Index" page displays a list of car dealerships available in the app. Each dealership's name is linked to its details page, where users can view reviews for that specific dealership.

### Dealer Details

The "Dealer Details" page displays the reviews for a specific car dealership. Authenticated users can also submit their own reviews for the dealership.

### Add Review

The "Add Review" page allows authenticated users to submit a review for a car dealership. Users can select the car model, provide a review, and indicate if they made a purchase from the dealership.

## Contributions

Contributions to the Dealership Review App are welcome! Feel free to open issues or submit pull requests to improve the app's features or fix any bugs.

## License

This project is licensed under the MIT License.

## Acknowledgments

Special thanks to the creators and maintainers of Django and the dependencies used in this project.
