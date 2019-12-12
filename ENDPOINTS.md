# Endpoints

## User

* `/register`
  * methods:
    * POST
* `/login`
  * methods:
    * POST 
* `/authorize`
  * methods:
    * GET
* `/reset`
  * methods:
    * GET
    * POST
* `/me`
  * methods:
    * GET
    * PUT
    * DELETE


## Project Groups

* `/`
  * methods:
    * GET
    * POST
* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
  * `invite` (NOT IMPLEMENTED)
    * methods:
      * POST
  * `projects`
    * methods:
      * GET 
  * `members` (NOT IMPLEMENTED)
    * methods:
      * GET
      * id (NOT IMPLEMENTED)
        * methods:
          * DELETE
  * `comments` (NOT IMPLEMENTED)
    * methods:
      * GET 

## Projects

* `/`
  * methods:
    * GET
    * POST
* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
  * `tasks`
    * methods:
      * GET
      * POST
  * `task`
    * methods:
      * GET
      * POST (NOT IMPLEMENTED)
  * `import/tasks/csv`
  * `reimport/tasks/csv`
    * methods:
      * POST
  * `members`
    * methods:
      *  GET
  * `invite`
    * methods:
      * POST 
  * `submissions`
    * methods:
      * GET
  * `comments`
    * methods:
      * GET 

## Tasks

* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
  * `media`
    * methods:
      * GET
  * `submissions`
    * methods:
      * GET
      * POST
  * `stats`
    * methods:
      * GET 
  * `comments`
    * methods:
      * GET
      * POST


## Media

* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
* `/source/sid`
  * methods:
    * GET 
* `/upload`
  * methods:
    * POST 

## Comments

* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
