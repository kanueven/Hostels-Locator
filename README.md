# Hostel Locator

Welcome to the Hostel Locator project! This is a web application built with Django that helps travelers find and book hostels around the world. The application allows users to search for hostels based on location, price, and amenities, and also includes features for managing bookings and saving favorite properties.

## Features

* Search for hostels based on location, price, and amenities
* View detailed information about each hostel, including photos, reviews, and ratings
* Book hostels directly through the platform
* Sign up for an account to save your favorite hostels and manage your bookings
* Hostel owners can add and manage their properties through the platform
* Mobile-responsive design for easy access on any device

## Getting Started

To get started with the Hostel Locator project, follow these steps:

1. Clone the repository and navigate into it:

```bash
git clone https://github.com/kanueven/Hostels-Locator.git
cd Hostels-Locator
```


2. Install the required dependencies in an environment of your choosing:

```bash
pip install -r requirements.txt
```


3. Set up the database:

```bash
python manage.py migrate
```


4. Run the development server:

```bash
python manage.py runserver
```


5. Open your web browser and navigate to `http://localhost:8000/` to view the application.

## Testing(Optional)

To test the functionality of the application do the following:

1. Create a superuser account to work as the host account for the dummy data to be generated:

```bash
python manage.py createsuperuser
```


2. Run the command and enter the number of hostels to create:

```bash
python create_hostels.py
```


3. Wait for the process to complete then navigate to the homepage on the browser:


## Contributing

We welcome contributions from the community! If you'd like to contribute to the project, please submit a pull request or open an issue on the project's GitHub page.

## Contact Us

If you have any questions or feedback, please don't hesitate to get in touch. You can reach us through our website's contact form or via email at info@hostellocator.com.

Thank you for using Hostel Locator!
