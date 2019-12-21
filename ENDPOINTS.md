# Endpoints
- root: `<URL>/v3`
## User
- root: `/users`
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
- root: `/project-groups`
* `/`
  * methods:
    * GET
    * POST
* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
  * `invite`
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
- root: `/projects`
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
- root: `/tasks`
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
- root: `/media`
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
- root: `/comments`
* `/id`
  * methods:
    * GET
    * PUT
    * DELETE

## Submissions
- root: `/submissions`
* `/id`
  * methods:
    * GET
    * PUT
    * DELETE
