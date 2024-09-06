# Backend - Trivia API

The backend for this Trivia app is a simple Flask app that defines a SQLALchemy database and exposes the necessary API endpoints for accessing the contained contained in the database.

## Setting up the Backend

No extraneous setup should be necessary to interact with the backend once the Docker container is running.  To inspect the logs for this service, run:

```
docker logs -f trivia-app
```

## API Documentation

Endpoints can be tested with the Docker container running, either using `curl` from the command line, or by accessing URLs at [http://localhost:5000](http://localhost:5000).

`GET /categories`

- Description: Fetches all available categories.
- Request Arguments: None
- Returns: An object containing a success flag and a dictionary of categories.

```sh
curl localhost:5000/categories 
```

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`GET /questions`

- Description: Fetches a paginated list of questions.
- Request Arguments:

  - `page` (integer): The page number to fetch.

- Returns: An object of all categories, the current category string, an object a containing a list of paginated questions, a success flag, and the total number of questions.

```sh
curl localhost:5000/questions\?page=1
```

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    ...
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

`DELETE /questions/<int:question_id>`

- Description: Deletes a specific question by its ID.
- Request Arguments:

  - `question_id` (integer): The ID of the question to delete.

- Returns: An object containing the ID of the deleted question, an updated list of questions to display, and a success flag.

```sh
curl -X DELETE localhost:5000/questions/23
```

```json
{
  "deleted": 23,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true
}
```

`POST /questions`

- Description: Creates either a new question or searches for questions based on a search term.
- Request Arguments:

  - `searchTerm` (string, optional): The term to search for in questions.
  - `question` (string, required if not searching): The text of the question.
  - `answer` (string, required if not searching): The text of the answer.
  - `category` (integer, required if not searching): The category ID of the question.
  - `difficulty` (integer, required if not searching): The difficulty level of the question.

- Returns: If searching, an object containing the current category, a list of questions, a success flag, and the total number of questions for the search. If creating, it returns the ID of the created question, a list of paginated questions to display, and a success flag.

Example Response for Search, where `{"searchTerm": "title"}` is passed as a payload:

```sh
curl -X POST localhost:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "title"}'
```

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

Example Response for Creation, where `{"question": "Why does a ball fall?", "answer": "gravity", "difficulty": 1, "category": 1}` is passed as a payload:

```sh
curl -X POST localhost:5000/questions -H "Content-Type: application/json" -d '{"question":"Why does a ball fall?","answer":"gravity","difficulty":"1","category":"1"}'
```

```json
{
  "created": 25,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true
}
```

`GET /categories/<int:category_id>/questions`

- Description: Fetches questions for a specific category.
- Request Arguments:

  - `category_id` (integer): The ID of the category to fetch questions for.

- Returns: An object containing the current category string, a list of paginated questions, a success flag, and the total number of questions.

```sh
curl localhost:5000/categories/3/questions
```

```json
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

`POST /quizzes`

- Description: Fetches a random question for a quiz, excluding previously asked questions.
- Request Arguments:

  - `previous_questions` (list of integers): A list of IDs of previously asked questions.
  - `quiz_category` (object): An object containing the ID and type of the quiz category.

- Returns: An object containing a random question from the given category (or from the entire list of questions if `0` is passed as `id`) and a success flag.

Example response, when `{"previous_questions": [], "quiz_category": {"id": 1, "type": "Science"}}` is passed as a payload:

```sh
curl -X POST localhost:5000/quizzes -H "Content-Type:application/json" -d '{"previous_questions":[],"quiz_category":{"id":1,"type":"Science"}}'
```

```json
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```
