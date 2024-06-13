
# Spyne Backend Task API

## Overview

This project is a Django-based API for managing discussions, users, comments, and likes. It allows users to sign up, log in, follow/unfollow each other, create discussions, comment on them, and like them. The API also provides functionality to search for users and discussions.

## Setup

### Prerequisites

- Python 3.8
- Django
- MySQL

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SChandel-cmd/SpyneTask.git
   cd SpyneTask
   ```
2. **Install the required packages**:
	 ```bash
	 pip install -r requirements.txt
	 ```
3. **Update MySQL database connection properties**:
	Open `backend/settings.py` and update the `DATABASES` section with your MySQL database connection properties:
	```python
	DATABASES = { 'default': 
		{ 'ENGINE': 'django.db.backends.mysql', 
		'NAME': 'your_database_name', 
		'USER': 'your_database_user', 
		'PASSWORD': 'your_database_password', 
		'HOST': 'your_database_host', 
		'PORT': 'your_database_port', 
		} 
	}
	```
4. **Make migrations and migrate**:
	```bash
	python manage.py makemigrations 
	python manage.py migrate
	```
5. **Run server**:
	 ```bash
	 python manage.py runserver
	```


## API Usage

For detailed API usage and endpoints, refer to [Documentation.md](Documentation.md).
