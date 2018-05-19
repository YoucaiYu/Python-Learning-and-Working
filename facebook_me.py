import facebook
import csv

token = 'EAACEdEose0cBABeCyk8pHFaX3abi2qLGEaQ1bM01dChtkZAknRwMpaZAuF1anN8M2YLOFRg3w17tQJZBEk0pVJaLoShbMjWXQbgr7Ar5LPlS4o16kug1JZAI1hXZAcPvEcOmYARSNAZByEtHOfxpZBepBJkO3SRKerb9VuN09wrx506dkIIZBnROMKcdBdM9WjSrWhmwCMVA0QZDZD'
graph = facebook.GraphAPI(access_token=token)
post_info = graph.get_object(id='369398139865083')
print(post_info)
print('Page Name：', post_info['name'])
print('Page ID:', post_info['id'])

posts = graph.get_connections(id='369398139865083', connection_name='posts')
data = []
for daten in posts['data']:
    for key, value in daten.items():
        data.append((key, value))

with open('facebook_me.csv', 'a', encoding='utf-8', newline="") as csv_file:
    writer = csv.writer(csv_file)
    for key, value in data:
        rows = [key, value]
        writer.writerow(rows)


