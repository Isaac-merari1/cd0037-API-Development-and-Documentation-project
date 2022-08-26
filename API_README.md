# API Development and Documentation Project

## Trivia App Endpoints with request parameter and response body

GET /categories
This endpoint returns all available categories in the database. The method does not take in any parameter in the request body and returns the success status, the categories avaiable and total number of categories availble.
Request Example : http://127.0.0.1:5000/categories 
Response Body example: 
{
    "success": True,
    "categories": {'1'	'Science'
                   '2'	'Art'
                   '3'	'Geography'
                   '4'	'History'
                   '5'	'Entertainment'
                   '6'	'Sports'},
    "total_categories": 6,
            }

GET /questions
This endpoint returns all the questions available in the database with pagination of 10 per page. The method does not take in any parameter in the request body and returns the success status, the total number of questions, the current category and the categories.
Request Example : http://127.0.0.1:5000/questions
Response Body : { 
    "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, 
    "current_category": "Science",
    "success": true,
    "questions": [ { "answer": "Maya Angelou", "category": "4", "difficulty": 2, "id": 5, "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?" }, { "answer": "Edward Scissorhands", "category": "5", "difficulty": 3, "id": 6, "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?" }, { "answer": "Muhammad Ali", "category": "4", "difficulty": 1, "id": 9, "question": "What boxer's original name is Cassius Clay?" }, { "answer": "Brazil", "category": "6", "difficulty": 3, "id": 10, "question": "Which is the only team to play in every soccer World Cup tournament?" }, { "answer": "Uruguay", "category": "6", "difficulty": 4, "id": 11, "question": "Which country won the first ever soccer World Cup in 1930?" },
    "total_questions": 5



GET /categories/<int:category_id>questions/question
This endpoint returns questions available in a specific category. The method takes in the category ID as an input parameter to get the information of that specific category. The repsonse includes succcess, the list of questions, total questions in that category and the type of category.
Request Example : http://127.0.0.1:5000/categories/2/questions
Response Body: { 
                "current_category": "Geography", 
                "success": true, 
                "questions": [ { "answer": "Lake Victoria", "category": 3, "difficulty": 2, "id": 13, "question": "What is the largest lake in Africa?" }, { "answer": "The Palace of Versailles", "category": 3, "difficulty": 3, "id": 14, "question": "In which royal palace would you find the Hall of Mirrors?" }, { "answer": "Agra", "category": 3, "difficulty": 2, "id": 15, "question": "The Taj Mahal is located in which Indian city?" } ], 
    
                "total_questions": 3 }

POST /questions
This endpoint creates a new question and add to the list of questions.  It doesn't take in input parameter in the request body. It require you pass in the question and answer text, category, and difficulty of the question.
Request Example: curl http://127.0.0.1:5000/question -x POST -H " -d "Content-Type: application/json" -d '{"question":"Which dung beetle was worshipped by the ancient Egyptians?", "answer": "Scarab","category" :"4", "difficulty":"4"}' 
Response Body: {
                    "success": True,
                    "question_created": 23,
                    "Questions": [ { "answer": "Lake Victoria", "category": 3, "difficulty": 2, "id": 13, "question": "What is the largest lake in Africa?" }, { "answer": "The Palace of Versailles", "category": 3, "difficulty": 3, "id": 14, "question": "In which royal palace would you find the Hall of Mirrors?" }, { "answer": "Agra", "category": 3, "difficulty": 2, "id": 15, "question": "The Taj Mahal is located in which Indian city?" }, { "answer": "Brazil", "category": "6", "difficulty": 3, "id": 10, "question": "Which is the only team to play in every soccer World Cup tournament?" }, {"answer": "Scarab","category" :"4", "difficulty":"4", "id": 23, "question":"Which dung beetle was worshipped by the ancient Egyptians?" } ],
                    "total_questions": 5
}

POST /search
This endpoint creates a Post to get questions based on a search term. It returns any questions for whom the search term is a substring of the question.
Request Body : curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}

Response Body : { 
            "success": True,
             "questions": [ { "answer": "Maya Angelou", "category": "4", "difficulty": 2, "id": 5, "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?" }, { "answer": "Edward Scissorhands", "category": "5", "difficulty": 3, "id": 6, "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?" } ], 
             "total_questions": 2 }

POST /quiz_questions
This endpoint allow Trivia users to play games and Create a POST endpoint to get questions to play the quiz. It takes in category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
Request Body: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"History","id":"4"}, "previous_questions":[3]}' 
Response Body: { 
            "success": true
            "question": { "answer": "Carver", "category": "4", "difficulty": 2,         "id": 12,   "question": "TWho invented Peanut Butter?	George  Washington" },  }

DELETE /question/<int:question_id>
This endpoint deletes a specific question from the database. It takes in the question ID as an input parameter in the request body which is of type Int. If successfully returns a success status of true and the quuestion ID deleted.
Request Example : http://127.0.0.1:5000/question/5
Response Body: {
            "success": True,
            "deleted": 5,
            "questions": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
            "total_questions": 4,
}

## Trivia App Error Response and their message
Error Response: {
    {"error_code": 404,
    "message": resource not found},
    {"error_code": 422,
    "message": unprocessable},
    {"error_code": 400,
    "message": "bad request"},
{    "error_code": 405,
    "message": "method not allowed"},
    {"error_code": 500,
    "message": "Internal server error!"}
}
