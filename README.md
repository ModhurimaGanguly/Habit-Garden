# Habit Garden
#### Video Demo: <URL HERE>
#### Description:

Habit Garden is a web-based habit tracker built with Python, Flask, and SQLite for CS50x's final project. Rather than reducing habit tracking to a plain checklist and a streak number, Habit Garden represents each habit as a small virtual plant that grows through visible stages — seed, sprout, growing, blooming, and flourishing — as the user's streak builds, and wilts back a stage if a day is missed. The goal was to take something CS50 teaches very directly (a login system, a database-backed CRUD app) and combine it with a simple, motivating visual metaphor, without reaching for any tools or libraries beyond what the course covers.

## What the project does

A user registers an account, logs in, and can add any number of habits they want to track — for example "Drink water" or "Study for 2 hours." Each habit starts as a seed. Every day the user visits the site and marks a habit as done, its streak count increases and, once it crosses certain thresholds, the plant visually grows into a new stage. If the user misses a day, the plant doesn't reset all the way back to a seed — it drops back by one stage instead, which felt more forgiving and realistic than punishing a single missed day as harshly as an entire abandoned habit. Users can also view a short history of their last seven check-ins per habit, and delete habits they no longer want to track.

## Project structure and what each file does

**`app.py`** is the heart of the application. It sets up the Flask app and connects to the SQLite database, and defines every route: `/register` and `/login` handle account creation and authentication (passwords are hashed with `werkzeug.security`, never stored in plain text); `/habits` queries the database for the logged-in user's habits and calculates each one's current growth stage before rendering the page; `/add` and `/delete` handle creating and removing habits; `/checkin` contains the core streak logic, deciding whether today continues a consecutive streak or follows a missed day; and `/history` pulls a habit's last seven check-in dates. A `login_required` decorator wraps every route that should only be accessible to a logged-in user, redirecting anonymous visitors to the login page. A small `get_stage()` helper function maps a numeric streak value to one of the five plant stages.

**`schema.sql`** defines the three database tables: `users` (id, username, and a hashed password), `habits` (id, which user it belongs to, its name, its current streak, and the date it was last checked in), and `checkins` (a log of every date a given habit was marked done). Keeping a full check-in log, rather than only storing the current streak number, made the history feature possible and made debugging the streak logic far easier, since I could inspect the raw data instead of trusting a single running number.

**`templates/`** holds the Jinja HTML templates: `login.html` and `register.html` for authentication, `habits.html` for the main dashboard showing every habit's plant and streak, `add_habit.html` for the habit-creation form, and `history.html` for the seven-day check-in view.

**`static/style.css`** contains all of the site's styling, and **`static/plants/`** holds five hand-built SVG illustrations, one per growth stage, swapped in based on the habit's current stage.

**`requirements.txt`** lists the Python dependencies (Flask and cs50).

## Design decisions I debated

The biggest decision was how a missed day should affect the streak. My first instinct was to simply reset the streak to zero, matching how most habit trackers work. I decided against this because it felt overly punishing for a project meant to encourage consistency rather than shame a single lapse — one missed day of drinking water shouldn't erase two weeks of progress. Instead, `/checkin` checks whether the previous check-in was exactly yesterday; if so, the streak increments normally, but if a day (or more) was missed, the streak only drops by one before counting today's completion. This meant the growth-stage thresholds also had to be chosen carefully, so that dropping "one stage" felt meaningful without being either too lenient or too harsh.

I also debated how to visually represent growth. My first version used plain colored `<div>` elements sized differently per stage, purely to get the logic working end-to-end before investing in visuals. Once the underlying streak and check-in logic were solid, I replaced these with small SVG illustrations of a potted plant at each stage — still simple enough to hand-build without any design tools, but far more recognizable as an actual plant than a colored rectangle.

Finally, I considered giving each user a single combined "garden" showing all their habits as one scene, rather than a separate plant per habit. I chose one plant per habit instead, since it maps each visual much more directly and clearly to the specific habit it represents, and was considerably simpler to implement correctly.

## AI usage disclosure

Portions of this project — including the Flask route structure, the SQL schema, the streak-calculation logic, and the plant SVG illustrations — were developed with assistance from Claude (Anthropic). All generated code was reviewed, tested, debugged, and understood by me before submission, in keeping with CS50's policy that such tools may amplify but not replace the student's own work. This disclosure is also noted as a comment at the top of `app.py`.
