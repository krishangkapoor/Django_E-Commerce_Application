Summary:

This project is a comprehensive e-commerce web application built with Django. It features user authentication, product management, a shopping cart, and email notifications for user interactions such as adding items to the cart and completing purchases. The application is designed to be deployed and run using Docker for a seamless setup process.

Features:

User registration and login with email verification.

Product catalog and detailed product views.

Shopping cart functionality with email notifications.

Password reset functionality with secure email-based password reset links.

Super admin, Admin, and moderator roles for user and product management.

Prerequisites:

Docker

Step-by-Step Guide to Download and Run the Application:

Step 1. Clone the repository or Download the zip file from this GitHub page by clicking code and then download zip.

Step 2. Open the command prompt and create an .env file in the root directory of the project. 

Step 3. Use the below variables for email configuration. Change the configurations to your actual configurations. You can make your app password by going to Gmail security and 
enabling the 2-step verification. Then go to app passwords and create one.  

EMAIL_HOST_USER=your_gmail@gmail.com 

EMAIL_HOST_PASSWORD=your_app_password

You can also do the same by going to the settings.py and changing the credentials to your own.

Step 4. Build the docker images and run all the containers (Django app, PostgreSQL, Redis, and Celery) by applying the following command on your cmd. 

docker-compose up --build

Step 5. Access the application at http://localhost:8000 in your browser.

Step 6. To access the admin you can make a superuser by using the following command in your cmd.

docker-compose exec web python manage.py createsuperuser

Step 7. To stop the application use the following command in your cmd.

docker-compose down


