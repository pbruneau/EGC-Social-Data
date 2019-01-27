## Available Data Description

``.json`` contains a JSON array of all tweets (i.e. ``status`` in Twitter terminology) emitted by the @associationEGC since its creation on 03/06/2016 to 27/01/2016. More information about the feature data fields may be found at https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html

## Running the Collection Script

First, install requirements:

    pip3 install -r requirements.txt

After adapting scripts with valid access tokens (see code comments for links), run:

    python3 collect_twitter.py
