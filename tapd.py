import requests
import json
import os
import sys
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
# https://github.com/Alir3z4/html2text/blob/master/docs/usage.md
import html2text
import openai
import time

if len(sys.argv) < 2:
    print("没有提供日期，格式 2023-01-01")
    sys.exit(0)

openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-3.5-turbo-0613"
max_tokens = 500



def get_third_occurrence(string, character):
  """
  获取字符串中第三个出现的字符。

  Args:
    string: 字符串。
    character: 字符。

  Returns:
    字符串中第三个出现的字符后面的部分。
  """
  indices = [i for i, c in enumerate(string) if c == character]
  if len(indices) >= 3:
    return string[indices[2] + 1:]
  else:
    return ""

def get_summary(messages):
    retries = 3    
    while retries > 0:    
        try: 
            response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    request_timeout=15
                )
            summary = response["choices"][0]["message"]["content"]
            return summary  
        except Exception as e:    
            if e: 
                print(e)   
                print('Timeout error, retrying...')    
                retries -= 1    
                time.sleep(5)    
            else:    
                raise e    
    print('API is not responding, moving on...')   
    return ""
   
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.single_line_break = True

auth=('QIhiPOt','15A05C95-A927-024A-2007-3D60D1E0D473')

file = open("tapd.txt", "a")
retry = Retry(total=10, connect=5, read=5, backoff_factor=10, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry))
session.auth = auth

page = 9
while page <= 100:
    print( f"current page: {page}" )
    params = { 'workspace_id': '31690354',
                'status': 'closed',
                'page': page,
                'order': 'created desc',
                'closed': '2023-08-17',
                'fields': 'id,title,description,created,closed'
             }


    r = session.get('https://api.tapd.cn/bugs', params=params)
    page = page + 1
    ret = json.loads(r.text)
    if ret['status'] != 1:
        print("response status is not 1, exit");
        exit()
    # print(ret['data'])

    for id in ret['data']:
        # print(id['Bug']['id'],id['Bug']['title'],h.handle(id['Bug']['description']).strip())
        bug_id = id['Bug']['id']
        bug_desc = get_third_occurrence(id['Bug']['title'],'】')
        if len(bug_desc) < 5:
            continue
        j = {}
        j['id'] = bug_id
        j['描述'] = bug_desc
        # print(id['Bug']['id'],get_third_occurrence(id['Bug']['title'],'】'))
        # echo -en "$(curl -u 'QIhiPOt:15A05C95-A927-024A-2007-3D60D1E0D473' 'https://api.tapd.cn/comments?workspace_id=31690354&entry_id=1131690354001020734')"

        params = { 'workspace_id': '31690354',
                'fields': "title,author,description,created",
                'order': "created asc",
                'entry_id': bug_id}
        r1 = session.get('https://api.tapd.cn/comments', params=params)
        ret1 = json.loads(r1.text)
        if ret1['status'] != 1:
            print("response status is not 1, exit")
            exit()
        # print(ret1['data'])
        j['处理过程'] = []
        i=0
        for c in ret1['data']:
            # print(c['Comment'])
            j['处理过程'].append({'姓名':c['Comment']['author'],"评论":h.handle(c['Comment']['description']).strip()[0:100]})
            # print(c['Comment']['author'],h.handle(c['Comment']['description']).strip())
            i=i+1
        print(j)

        prompt = "以下的JSON对象是一个问题的处理过程,用一句话总结问题的解决方案,不需要过程." + str(j)
        messages = []
        messages.append({"role": "user", "content": prompt})
        summary = get_summary(messages)
        print( summary )
        o = {'id': bug_id, 'desc': bug_desc, "summary": summary}
        file.write( f"{str(o)}\n" )
        file.flush()
file.close()