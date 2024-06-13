# API Documentation

## Authentication

### Sign Up

**URL**: `/api/v1/users/`

**Method**: `POST`

**Description**: Create a new user account.

**Request Body**:
```json
{
  "name": "sarthak",
  "mobile": "9876543210",
  "email": "sarthakchandel12@gmail.com",
  "password": "password12"
}
```

**Response Body**:
```json
{
  "id": 1,
  "name": "Sarthak",
  "mobile": "9876543210",
  "email": "sarthakchandel12@gmail.com"
}
```
