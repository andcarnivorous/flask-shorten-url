# Installation

Install the requirements by running:

```pip3 install -r requirements.txt```

Before running the service.py script, you have to build the database by running:

```python3 db.py```

This will create the test.db file.

# Running the app

To run the app just run

```python3 service.py```

You can now send curl requests like so:

```curl 127.0.0.0:5000/shorten -d '{"url":"myurl.com", "shortcode":"myshortcode"}' -H 'Content-Type: application/json'```

Remember that the shortcodes must be 6 characters long, only letters, numbers and underscores are accepted.

```curl 127.0.0.0:5000/<yourshortcode> ```
Will return the corresponding url in the db. It will also update the redirect count and last redirect date.

```curl 127.0.0.0:5000/<yourshortcode>/stats ```
Will return the stats on the shortcode provided

# Running the unittest

```python3 -m unittest unittesting.py```

You can change some parameters in the unittesting script, like the number of urls to take from the ```urls.txt``` list.

You should remove and recreate the test.db between each run of the unittest script.
