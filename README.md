# legalmation_challenge
Python Challenge from LegalMation

Thank You for reviewing my submission to your challenge!

Step 1:
    Clone the Respository
Step 2:
    Make sure you are using a python3 virtualenv, with flask installed
Step 3:
    Activate the virtual env: source env/bin/activate
Step 4:
    run python app.py in the terminal and open the local server
Step 5:
    you should see a simple webpage with a form to upload an xml file 
Step 6:
    Once you upload a valid file it will store relevant information and redirect you to /files 
    where the stored info will be displayed in a table, you visit this whenever you need.
Step 7:
    You can hit the api at /api/files or /api/get_file/<id>. The former will return a JSON of all stored files and their info. The latter will return a specific file's info based on the id you provide. You can view all files and their ids at /files.
Step 8:
    If you want to run the tests you will need to install pytest and run pytest in the terminal. Those are just some of the tests but many of those I was testing and changing based on specfic contexts of the app so some of those may fail in the form you clone the repository. I wanted to give you a heads up because I was testing the app in many different states so the state that you clone the repo in will fail many of the tests currently in those files.
