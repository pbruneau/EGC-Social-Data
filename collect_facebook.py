# examples using facebook-sdk, see e.g. https://github.com/mobolic/facebook-sdk/blob/master/examples/get_posts.py
# see also # http://facebook-sdk.readthedocs.io/en/latest/api.html

import facebook
import requests
import pdb
import json
import codecs

# process a single post, by updating results['message'] array
# and counter of stored messages, likes and comments
def process_post(post):
    global results
    global mess_count
    global like_count
    global comment_count
    if 'message' in post:
        mess_count += 1
        results['messages'].append({'message': post['message'], 'created_time': post['created_time']})
        likes = graph.get_connections(post['id'], 'likes')
        if len(likes['data']) > 0:
            results['messages'][-1]['likes'] = [{'id': item['id'], 'name': item['name']} for item in likes['data']]
            like_count += len(likes['data'])
        comments = graph.get_connections(post['id'], 'comments')
        if len(comments['data']) > 0:
            results['messages'][-1]['comments'] = [{'id': item['from']['id'], 'name': item['from']['name'], 'message': item['message'], 'created_time': item['created_time']} for item in comments['data']]
            comment_count += len(comments['data'])

			
# temporary tokens can be fetched here: here: https://developers.facebook.com/tools/explorer/
access_token = 'ACCESS_TOKEN'
# get_connections can be parametrized by any item name (e.g. account, page)
pagename = 'AssociationEGC'
results = {
            'messages': []
          }

graph = facebook.GraphAPI(access_token)
page = graph.get_object(pagename)
# NB: get_connections(page['id'], 'likes') is the list of pages liked by this page, not users liking the given page.
# the latter is apparently not possible: https://stackoverflow.com/questions/22801203/facebook-api-get-user-liked-page-using-fb-api
posts = graph.get_connections(page['id'], 'posts')

mess_count = 0
like_count = 0
comment_count = 0

# get_connections / get_all_connections: access likes and comments
# get likes for the page,
# get posts, and likes and comments for all posts
# build JSON-like structure:
# - messages
#   - message
#   - created_time
#   - likes
#     - [id, name]
#   - comments
#     - [id, name, message, created_time]

while True:
    try:
        [process_post(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
        
# write to JSON
with codecs.open('{}'.format('EGC_facebook.json'), 'w', encoding="utf-8") as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=2)
print('written {} messages'.format(mess_count))
print('written {} likes'.format(like_count))
print('written {} comments'.format(comment_count))
