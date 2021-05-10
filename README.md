# Survey API
API to create and manage Surveys written in Django Rest Framework

## Descritpion and Design

This api can be used to create and manage Surveys. Surveys can be assigned to specific users as well as groups or both. 
Surveys have publication and expiration date to control the display duration allong with an interval to define the frequency of the survey display.
Surveys have also different categories that each Survey belongs to. Finally there is a rating system available and can be used as star rating for example.
Different questions and types of questions can be added to the survey. 

## ERD

The image bellow depicts the Entity Relation Diagram created in DBVizualizer.


![survey_erd](https://user-images.githubusercontent.com/14307335/117629841-3dc3b400-b183-11eb-97b6-1f3a7fd3708f.jpg)


## Setting Up the environment using Docker:

1. Install Docker and docker-compose
2. Run the poject
## Setting Up the environment using Docker:

1. Install Docker and docker-compose
2. Run the poject
```bash
$ docker-compose up
```
Go to https://localhost:8000 to see the results.

```bash
$ docker-compose up -d  (to run in the background)
```
Use http://localhost:8000 as base url.

```bash
$ docker-compose up -d  (to run in the background)
```

## Working with the environment

Firt of all an admin user is required and can be created from Django shell.

1. Go inside the container 

```bash
$ docker-compose exec web bash  
```
2. Create super user inside the container

```bash
$ python3 manage.py createsuperuser
```
3. Go to Django admin page at "http://localhost:8000/admin" and login with the user.

## Django Admin page

Through Django Admin Page you can do almost anything. Create Users, Groups, Surveys, Questions assing Users to Surveys etc.
First of all just create another simple user from the admin page.

## API 

API is used to create also and manage Surveys. As of now no Authorization is implemented for this project

## API Endpoints


1. Get List of Surveys
  ```
  METHOD: GET

  URL: http://localhost:8000/surveys/
  ```
 2. Get Single Survey (detail)
 
   ```
    METHOD: GET

    URL: http://localhost:8000/surveys/<survey_id>/
   ```
 2. Create Survey
 
 ```
 METHOD: POST
 URL: http://localhost:8000/surveys/
 
 BODY:
  {
    "name": "Survey Name", --> char
    "description": "Description ", --> char
    "category": <category_id>, --> int
    "user_emails": ["test@example.com",] --> list 
    "groups": [<group_id:in>, <group_id>], -->list
    "questions": [
        {"text":"text1", "question_type": "checkbox", "required": false},
        {"text":"text2", "question_type": "text", "required": true},
        {"text":"text3", "question_type": "radio", "required": true, "choices":"choice_text1, choice_text2"}

    ],
    "pub_date": "2021-05-13T17:58:24Z", --> timestamp
    "exp_date": "2021-05-16T17:58:24Z", --> timestamp
    "period": "25:00:00" --> translates to 1d and 1h
}
 ```
 
 
 3. Get Survey Questions

 
   ```
    METHOD: GET

    URL: http://localhost:8000/surveys/<survey_id>/questions/
    
   ```
 
 4. Update a Survey
 
 ```
    METHOD: PUT

    URL: http://localhost:8000/surveys/<survey_id>/
    
    BODY: 
    {
    "name": "Survey Name",
    "description": "Survey Desc",
    "category": <category_id:int>,
    "user_emails": ["user@example.com"],
    "groups": [<group_id:int>, <group_id:int>],
    "pub_date": "2021-05-13T17:58:24Z",
    "exp_date": "2021-05-16T17:58:24Z"
    
}
 
 ```
 *Note Altough we can add questions when we create Survey we cannot update question when we update Survey. We update from question endpoint
   
 5. Delete a Survey
 ```
    METHOD: DELETE

    URL: http://localhost:8000/surveys/<survey_id>/
 ```
 
 
 6. Adding Questions to existing Survey
 
 ```
 METHOD: POST
 URL: http://localhost:8000/surveys/<survey_id>/
 
 BODY:
  {
    "questions": [
        {"text":"text1", "question_type": "checkbox", "required": false},
        {"text":"text2", "question_type": "text", "required": true},
     ]
}
 ```
 
 7. Update Question

```
 METHOD: PUT
 URL: http://localhost:8000/questions/<question_id>/
 
 BODY:
 
 {"text":"NewText", "question_type": "radio", "required": true, "choices": " ", "survey":"<survey_id>"}

 
```
6. Question Detail
 ```
 METHOD: GET
 URL: http://localhost:8000/questions/<question_id>/
 ```

7. Get Survey Categories
```
 METHOD: PUT
 URL: http://localhost:8000/surveys/categories/
```

