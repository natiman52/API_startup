# TESTS

* first test password reset pipe line (IMPORTANT)

### React setup needs

* I am using JWT for authentication (http-only)
* you don't need to set tokens as those are set automatically by the browser
* you need to handle csrftokens as dj_rest_auth needs it
* main api route """ /api/auth/* """ 

### IMPORTANT ROUTES

* "/api/auth/user" used to check user loged in status (as we use non-js cookies we cant read them)
* "api/auth/google/" is the endpoint for signup with google Oauth
* 