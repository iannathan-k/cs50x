# CS50 GenAI Guru

#### Video Demo: https://youtu.be/XgXPRa7U3v4

#### Description:

This Final Project offers a website for users to experience Generative AI in action, powered by Google Gemini. Users will be able to test their trivia skills by answering several AI-generated questions and manually track which ones they got it right. They can continue play by fetching the next set of AI-generated questions. Their achievements are then tracked and the top-10 will show up on the Leaderboard. To make it more fair to everyone, the top-10 shown can be based on their lifetime records, last 24-hour as well as last hour. Users can show the different top-10 with a simple Javascript-based links.

The files in this project are put into several subdirectories:
1. project/static - to store all static files like images, javascript and css
2. project/templates - to store all flask template files that are use for rendering
3. project - to store all the python and db files, along with miscellaneous files like requirements.txt and this README.md file

### project/static

- favicon.ico - the small icon showed on the brower's tab when the webpage is loaded
- I_heart_validator.png - the small logo showed at the bottom of every page
- project.js - the JavaScript file used in this project
- styles.css - the css file used in this project

### project/templates

- ama.html - the page that allows users to type in any questions for the GenAI to answer
- ama_done.html - the page that displays the GenAI's answer to the user's question
- apology.html - the page that shows a memegen with embedded custom text, used to show an error/warning to users
- index.html - the landing page when users visit this website. It provides a simple explanation about what the users can do.
- layout.html - the main HTML page with a preallocated space to show the contents from all other template pages
- login.html - the page to handle user login
- register.html - the page to allow new users register for an account
- stats.html - the page that shows user's achievement and top-10 leaderboards. Users will be able to toggle among the top-10 based on their lifetime achievements, or just based on their achievements in the last 24 hours or last 1 hour.
- trivia.html - the page that shows GenAI-generated trivia questions, along with most-recent and most-frequent questions. Users will be able to toggle between the most-recent and most-frequent list of questions by clicking a link. The click will then be handled by a JavaScript function that sends a HTTP POST request to the backend asyncrhonously using AJAX.

### Generative AI

One of the primary objectives in this Final Project is to gain the experience of using Generative AI programmatically. There are a number of GenAI engines that people can choose from. This Final Project decides to use Google Gemini.

Several preparation steps to follow include:
1. Create a new Google Cloud project using a gmail account
2. Sign in to [Google AI Studio](https://ai.google.dev/aistudio)
3. Generate GenAI API Key using the "Get API key" button
4. Optionally go through the "Set up Billing" option in case you plan to use this GenAI beyond the free usage provided by Google
5. Use the [Gemini API Docs for Python](https://ai.google.dev/gemini-api/docs/text-generation?lang=python) as a reference

This Final Project exercises specifically the Text Generation capability of the Google Gemini. It uses the **gemini-1.5-pro** foundation model.

Before executing the flask run, do export the API_KEY on the command line.
The API_KEY should not be hard-coded in the python code since it belongs to a specific user of the Google project and there is a limited free quota to use.

### Input-dependent Custom SQL and Aggregations

This project also allows users to be more interactive on the page, which then decides the exact SQL query to the database. On the Leaderboard page, users are able to show the Top-10 based on lifetime achievement or just last 24-hour and last-hour. On the Trivia page, users are able to show the 5 most-recent questions or 5 most-frequently asked questions. This interaction will then decide the WHERE clause of the SQL before aggregating the stats using GROUP BY.

### HTML Ajax

This Final Project also showcases how AJAX (Asynchronous JavaScript and XML) can be used to make a page to be more interactive for the users without having to reload the entire pages. It leverages JavaScript to send an HTTP request to the backend. In this project, the Trivia page uses AJAX to send a HTTP POST request to the backend when users self-grade themselves. The backend will then track the stats in the database. Upon successful tracking, the API will simply return **ok** and the webpage will simply ignore it, regardless whether the tracking was actually successful or not.


### Bootstrap

This Final Project also leverages various Bootstrap classes like container, row-md-xx, col-md-xx, btn, btn-primary, btn-secondary, text alignments, etc.
