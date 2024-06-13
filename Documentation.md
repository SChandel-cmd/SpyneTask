# API Documentation

## User & Authentication

### Sign Up

**URL**: `/api/v1/users/`

**Method**: `POST`

**Description**: Create a new user account.

**Request Body**:
```json
{
  "name": "<name>",
  "mobile": "<phone number>",
  "email": "<email>",
  "password": "<password>"
}
```

**Response Body**:
```json
{
  "id": <user id>,
  "name": "<name>",
  "mobile": "<phone number>",
  "email": "<email>"
}
```

### Login

**URL**: `/api/v1/token/`

**Method**: `POST`

**Description**: Login to the server and generate an auth token. Use the receieved auth token as a bearer token for every other API.

**Request Body**:
```json
{
  "email": "<email>",
  "password": "<password>"
}
```

**Response Body**:
```json
{
  "refresh": "<refresh token>",
  "access": "<access token>",
}
```

### Update

**URL**: `/api/v1/users/update/<user id>`

**Method**: `PUT`

**Description**: Update user details.

**Request Body**:
```json
{
  "name": "<name>",
  "mobile": "<phone number>",
  "email": "<email>",
  "password": "<password>"
}
```

**Response Body**:
```json
{
  "id": <user id>,
  "name": "<name>",
  "mobile": "<phone number>",
  "email": "<email>"
}
```

### Delete

**URL**: `/api/v1/users/delete/<user id>`

**Method**: `DELETE`

**Description**: Delete the specificied user.

**Request Body**:
```json
{
}
```

**Response Body**:
```json
{
    "id": <user id>,
    "message": "User deleted successfully"
}
```

### Search

**URL**: `api/v1/users/search`

**Method**: `GET`

**Description**: Search for a specific user.

**Request Parameters**:
* name=<name>

**Response Body**:
```json
[
    {
        "id": <user id>,
        "name": "<name>",
        "mobile": "<phone number>",
        "email": "<email>"
    }
]
```

### Follow

**URL**: `/api/v1/follows/`

**Method**: `POST`

**Description**: Follow the specified user.

**Request Body**:
```json
{
  "following_id": <user id>,
}
```

**Response Body**:
```json
{
    "id": <user id>,
    "follower": {
        "id": <user id>,
        "name": "<name>",
        "mobile": "<phone number>",
        "email": "<email>"
    },
    "following": {
        "id": <user id>,
        "name": "<name>",
        "mobile": "<phone number>",
        "email": "<email>"
    },
    "created_at": <timestamp>
}
```

### Unfollow

**URL**: `/api/v1/follows/<user id>/`

**Method**: `DELETE`

**Description**: Delete the specificied user.

**Request Body**:
```json
{
}
```

**Response Body**:
```json
{
    "id": <user id>,
    "message": "User unfollowed successfully."
}
```

### Following

**URL**: `api/v1/users/following/<user id>`

**Method**: `GET`

**Description**: Get all following of specified user.

**Response Body**:
```json
[
    {
        "id": <user id>,
        "name": "<name>"
    }
]
```

### Followers

**URL**: `api/v1/users/followers/<user id>`

**Method**: `GET`

**Description**: Get all followers of specified user.

**Response Body**:
```json
[
    {
        "id": <user id>,
        "name": "<name>"
    }
]
```

## Discussions

### Create

**URL**: `api/v1/discussions/`

**Method**: `POST`

**Description**: Create a new post/discussion.

**Request Body**:
```json
{
    "text": "<text>",
    "hashtags": "<hashtags> (in csv format)",
    "image": "<file selection through postman form-data>"
}
```

**Response Body**:
```json
{
    "id": <discussion id>,
    "user": <user id>,
    "text": "<text>",
    "image": "<image>",
    "hashtags": "<hashtags>",
    "created_on": "<timestamp>",
    "views": <views>,
    "likes": <likes>,
    "comments": [<comments>]
}
```
### Update

**URL**: `api/v1/discussions/update/<discussion id>`

**Method**: `PUT`

**Description**: Update an existing post/discussion.

**Request Body**:
```json
{
    "text": "<text>",
    "hashtags": "<hashtags> (in csv format)",
    "image": "<file selection through postman form-data>"
}
```

**Response Body**:
```json
{
    "id": <discussion id>,
    "user": <user id>,
    "text": "<text>",
    "image": "<image>",
    "hashtags": "<hashtags>",
    "created_on": "<timestamp>",
    "views": <views>,
    "likes": <likes>,
    "comments": [<comments>]
}
```

### Search

**URL**: `api/v1/discussions/search`

**Method**: `GET`

**Description**: Search for a specific discussion based on text and hashtag.

**Request Parameters**:
* text=<text>
* hashtags=<hashtag>

**Response Body**:
```json
[
    {
        {
            "id": <discussion id>,
            "user": <user id>,
            "text": "<text>",
            "image": "<image>",
            "hashtags": "<hashtags>",
            "created_on": "<timestamp>",
            "views": <views>,
            "likes": <likes>,
            "comments": [<comments>]
        }
    }
]
```

### Detailed View

**URL**: `api/v1/discussions/<discussion id>/`

**Method**: `GET`

**Description**: Get details for a specific post/discussion.

**Response Body**:
```json
[
    {
        "id": <discussion id>,
        "user": <user id>,
        "text": "<text>",
        "image": "<image>",
        "hashtags": "<hashtags>",
        "created_on": "<timestamp>",
        "views": <views>,
        "likes": <likes>,
        "comments": [<comments>]
    }
]
```

### Delete 

**URL**: `api/v1/discussions/delete/<discussion id>`

**Method**: `DELETE`

**Description**: Delete a specific post/discussion.

**Response Body**:
```json
{
    "id": <discussion id>,
    "message": "Discussion deleted successfully"
}
```

## Comments

### Create

**URL**: `api/v1/comments/`

**Method**: `POST`

**Description**: Create a new comment on a discussion.

**Request Body**:
```json
{
    "text": "<text>",
    "discussion": <dicussion id>
}
```
**Response Body**:
```json
{
    "id": <comment id>,
    "user": <user id>,
    "discussion": <discussion id>,
    "text": "<text>",
    "created_on": "timestamp"
}
```

### Update

**URL**: `api/v1/comments/<comment id>/`

**Method**: `PUT`

**Description**: Update a comment on a discussion.

**Request Body**:
```json
{
    "text": "<text>",
}
```
**Response Body**:
```json
{
    "id": <comment id>,
    "user": <user id>,
    "discussion": <discussion id>,
    "text": "<text>",
    "created_on": "timestamp"
}
```

### Delete

**URL**: `api/v1/comments/<comment id>/`

**Method**: `DELETE`

**Description**: Delete a comment on a discussion.

**Response Body**:
```json
{
    "id": <comment id>,
    "message": "Comment deleted successfully"
}
```

## Replies

### Create

**URL**: `api/v1/replies/`

**Method**: `POST`

**Description**: Create a new reply on a comment.

**Request Body**:
```json
{
    "text": "<text>",
    "comment": <commet id>
}
```
**Response Body**:
```json
{
    "id": <reply id>,
    "user": <user id>,
    "comment": <comment id>,
    "text": "<text>",
    "created_on": "timestamp"
}
```

### Update

**URL**: `api/v1/replies/<reply id>/`

**Method**: `PUT`

**Description**: Update a reply on a comment.

**Request Body**:
```json
{
    "text": "<text>",
}
```
**Response Body**:
```json
{
    "id": <reply id>,
    "user": <user id>,
    "comment": <comment id>,
    "text": "<text>",
    "created_on": "timestamp"
}
```

### Delete

**URL**: `api/v1/replies/<reply id>/`

**Method**: `DELETE`

**Description**: Delete a reply on a comment.

**Response Body**:
```json
{
    "id": <reply id>,
    "message": "Reply deleted successfully"
}
```

## Likes

### Like Discussion

**URL**: `api/v1/likes/`

**Method**: `POST`

**Description**: Like a discussion.

**Request Body**:
```json
{
    "discussion": <discussion id>,
}
```
**Response Body**:
```json
{
    "id": <like id>,
    "user": <user id>,
    "discussion": <discussion id>,
    "created_on": "<timestamp>"
}
```

### Unlike Discussion

**URL**: `api/v1/likes/<discussion id>/`

**Method**: `DELETE`

**Description**: Unlike a discussion.

### Like Comment

**URL**: `api/v1/likes/`

**Method**: `POST`

**Description**: Like a comment.

**Request Body**:
```json
{
    "comment": <comment id>,
}
```
**Response Body**:
```json
{
    "id": <like id>,
    "user": <user id>,
    "comment": <comment id>,
    "created_on": "<timestamp>"
}
```
