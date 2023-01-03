# Book Reviews Website API

**This API provides the necessary endpoints for a book review website similar to Goodreads. It allows users to sign up for the service, add books to reading lists, rate and review books, make posts about books, and other functionality.**

## Usage

**The following descriptions describe each endpoint of the API and its expected output.**

### /users

- GET
  Returns a jsonified list of all users and their attributes
- POST
  Adds a user to the database
  Requires: 'username', 'password', 'first_name', and 'last_name' must be included in request in JSON format
  Optional - 'bio' and 'birthdate' are optional attributes that can be optionally included in request in JSON format

### /users/<int:id>

- GET
  Returns a jsonified list of user that matches the id in <int:id> in the url

### /users/<int:id>/posts

- GET
  Returns a jsonified list of all posts that the user with matching id has made
- POST
  Creates a post for specified user
  Requires: 'title' and 'content' must be included in request in JSON format

### /users/<int:user_id>/posts/<int:post_id>

- GET
  Returns jsonified post that matches user id and post id
- PUT/PATCH
  Edit the title and content of a previous post
  Requires: Either 'title', 'content', or both must be included in request in JSON format
- DELETE
  Deletes a previous post

### /users/<int:id>/books

- GET
  Returns a jsonified list of all of the books that the user has added to their bookshelf ("currently reading", "read", or "want to read")
- POST
  Adds a book to the user's bookshelf
  Requires: 'book_id' and 'status' ("currently reading", "read", or "want to read") must be included in the request in JSON format

### /users/<int:id>/reading_challenge

- GET
  Returns the parameters of the specified user's reading challenge for the current year as a JSON object
- POST
  Signs a user up for the yearly reading challenge
  Requires: 'goal' (number of books to be read that year) must be included in the request in JSON format

### /users/<int:user_id>/<int:book_id>/rating

- GET
  Returns specified user's rating of the specified book as a JSON object
- POST
  Adds a rating of the specified book by the specified user
  Requires: 'rating' must be included in request in JSON format
  Optional: 'content' can be included in the request in JSON format. This represents the users written review of the book

### /books

- GET
  Returns a jsonified list of all books in the database
- POST
  Adds a book to the database
  Requires: 'title', 'publication_date', 'page_count', and 'author_id' to be included in the request in JSON format
  Optional: 'series_id' and 'series' order can be optionally included in the request in JSON format

### /books/<int:id>

- GET
  Returns JSON object of specified book attributes
- PUT/PATCH
  Updates attributes of specified book
  Requires: One or more of 'title', 'publication_date', 'page_count', 'author_id', 'series_id', or 'series_order' must be included in the request in JSON format
- DELETE
  Deletes specified book from database

### /books/<int:id>/ratings

- GET
  Returns a jsonified list of all ratings for specified book

### /books/<int:id>/avg_rating

- GET
  Returns a JSON object of average rating for the specified book

### /awards

- GET
  Returns a jsonified list of all awards in the database
- POST
  Adds an award to the database
  Requires: 'name' must be included in the request in JSON format

### /awards/<int:id>

- GET
  Returns a JSON object of specified award
- DELETE
  Deletes specified award from database

### /genres

- GET
  Returns a jsonified list of all genres in the database
- POST
  Adds a genre to the database
  Requires: 'name' must be included in the request in JSON format

### /genres/<int:id>

- GET
  Returns a JSON object of specified genre
- DELETE
  Deletes specified genre from the database

### /series

- GET
  RETURNS a jsonified list of all series in the database
- POST
  Adds a series to the dabase
  Requires: 'title' must be included in the request in JSON format

### /series/<int:id>

- GET
  Returns a JSON object of specified series
- PUT/PATCH
  Edits the series attributes
  Requires: 'title' must be included in the request in JSON format.
- DELETE
  Deletes specified series from database

## Retrospective

1. How did the project's design evolve over time?
   - I had to scale back from my original ER digaram. It took a lot more work to implement each endpoint than I thought it was going to take.
2. Did you choose to use an ORM or raw SQL?
   - I used an ORM to create the queries for the project. However, in a couple spots I used raw SQL as it was easier to fine tune the query exactly how I wanted it to be.
3. What future improvements are in store if any?
   - I have not finished all of the endpoints for the project, so I still need to do that to fully complete it.
