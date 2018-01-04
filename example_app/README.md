# This is an example Flask application using the Nordeas Open Banking API

## Quickstart

First, open the `example_app/config.cfg` file and set your app id, app secret and redirect uri there. The app id and secret can be found from the developer portal, please see the documentation there to learn how to find and generate these values.

To run the app within docker container use:

`docker run -p 5000:5000 example --name example`

To run it locally without docker, just type:

`./run.sh`


After starting the app, navigate to http://127.0.0.1:5000/


## Warning

Please note that this application is NOT USING TLS so all traffic between the client and this application is UNPROTECTED.

Moreover, there are no tests and this application is purely meant to be example showing how the API could be used.

DO NOT USE THIS APPLICATION IN PRODUCTION AND DO NOT EXPOSE IT TO THE OPEN INTERNET.
