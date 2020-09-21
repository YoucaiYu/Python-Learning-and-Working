import facebook
import pandas as pd
import requests
import json

def get_post_info(page_id, token):

    graph = facebook.GraphAPI(access_token=token)
    all_posts = graph.get_connections(page_id, connection_name='posts', summary=True)
    data = []
    main_link = 'https://graph.facebook.com/v3.0/'
    share_search = '?fields=shares&access_token='

    for post_new in all_posts['data']:
        if 'message' in post_new:
            post_id = post_new['id']
            post_content = post_new['message']
            post_time = post_new['created_time']
            likes = graph.get_connections(post_id, connection_name='likes', summary=True)
            count_likes = likes['summary']['total_count']
            user_id = page_id
            try:
                share_search_link = main_link + post_id + share_search + token
                response = requests.get(share_search_link)
                html = json.loads(response.text)
                share_count = html['shares']['count']
            except KeyError:
                share_count = 'NA'
            data.append([post_id, post_content, count_likes, share_count, user_id, post_time])
        else:
            continue

    information_list = pd.DataFrame(data)
    return information_list

id = ['18269172444', '2227081004182820', '7003656077']
tt = 'EAACEdEose0cBAFb1PZC6dBqez3DZAtC5jIDoOeC7hhXZBNOPgYLqUW31fjZAps2XUZC3vZBvrhPkVSj2EBhZBWZB6fzVhVr1hxBHt5wZCmXJKB5HQ9MtsQa2irufYRE8oK4ZBZAJwLt6mc6eL9KeriOKDqg1XYSoa3XtkKZBFbm0lsAb7NciwPU8HaIMO2c7zDrEePQrTYtjFOaY6wZDZD'

df = get_post_info(id, tt)

print(df)
df.to_csv('Agilent Technologies_Posts.csv', index=False, header=False, encoding='utf-8')








