# SM2KG-WebApp

The Sofware Metadata to Knowledge Graphs Web Application lets users enter a Github URL, and retrieve metadata about the repository, which can be downloaded in a JSON format.

Installation Instructions:

1st) 
  Make sure you have Python version 3!
  Follow the instructions here if you don't: https://wiki.python.org/moin/BeginnersGuide/Download
  
2nd) 
  in SM2kG/SM2KG-WebApp, run the following command:
  ```
  pip3 install -r requirements.txt
  ```
3rd)
  In the same directory as step 2, run:
  ```
  export FLASK_APP = sm2kgweb.py
  ```
4th)
  To run the Flask application run:
  ```
  flask run
  ```
Additional Instructions:
  If you're having trouble connection to github or downloading the sm2kg package, you can run the site on an example repo by running: 
  ```
  export SM2KG_TEST_MODE=TRUE
  flask run
  ```
  
