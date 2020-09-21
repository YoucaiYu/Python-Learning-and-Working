import requests
import json
import csv
import pandas as pd
import facebook

file_name = 'FB_link_list.csv'

with open(file_name) as f:
    reader = csv.reader(f)
    fb_link_list = []
    for row in reader:
        fb_link_list.append(row[0])


main_link = 'https://graph.facebook.com/v3.0/'
id_search = '?fields=id,name&access_token='
token = 'EAACEdEose0cBAAmFYbMzyOxnZCsKvZB990gaZARPQokuNc5KoLCWmNrUgb6NucZBcvbiwIZC2e0nWTqN5Sk25ZByNJ0wCZBDqkgD0ZBDgihwAqRUC47xLhBTkAMzCqzrvEniY8u8B0FStL98aVcBh9mmVMtASTSHUqPUAZBOKG1yc2GDVaZBEoqpF9VSY7ZBkfoKRx7s8jeKZB3ouAZDZD'

fb_info_list = []
i = 1
for fb_id in fb_link_list:
    id_search_link = main_link + fb_id + id_search + token
    response = requests.get(id_search_link)
    html = json.loads(response.text)
    user_id = html['id']
    user_name = html['name']
    print("第 ", i , " 个 infor.")
    fb_info_list.append((str(user_id), user_name))
    i = i + 1

final_list = pd.DataFrame(fb_info_list)
final_list.to_csv('FB_Fanpage_ID_and_Name.csv', mode='a', index=False, header=False, encoding='utf-8')

# define a function
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

tt = 'EAACEdEose0cBAJkLuIhjImSlLUyZBRQlro7HCJ098zfWvGDSoGRR0vZAWIIDoYMJHZC8o1RfYb7X9M5XTxJUE6eC3ZC6UAyrurMHxdFgQaGjT81x1zYq70JuJZAEnOuVr2XM6yIjdw9qeJtjveDdsZC5AHqSSLbxVsU6T2dMYjVjWuVClxREPDQccCJ4hX9SBpCbqWrDAFQwZDZD'
i = 1
id_list = ['103870236321424', '1565998713679090', '133959183559', '1239952466122240', '232958166719419', '869443773140058', '271558952944264', '198801466796872', '234926376572738', '147272032747087']

for id in id_list:
    try:
        df = get_post_info(id, tt)
        df.to_csv('fb_posts.csv', mode='a', index=False, header=False, encoding='utf-8')
        print(i)
    except facebook.GraphAPIError:
        print("ID Error: ", i)

    i = i + 1



