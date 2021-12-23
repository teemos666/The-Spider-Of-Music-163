# 1. 找到未加密的参数
# 2. 想办法把参数进行加密（必须参考网易的逻辑） ，params => encText, encSecKey => encSecKey
# 3. 请求到网易，拿到评论信息

# pip install pycryptodome
from Crypto.Cipher import AES
from base64 import b64encode
from bs4 import BeautifulSoup
import requests
import json

url = "https://music.163.com/weapi/cloudsearch/get/web"
url_comment = "https://music.163.com/weapi/comment/resource/comments/get"
# 请求方式是POST

data = {
    "hlposttag": "</span>",
    "hlpretag": "<span class=\"s-fc7\">",
    "limit": 30,
    "offset": 0,
    "s": "叙世",
    "total": "true",
    "type": "1"
}

data_comment = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_464756496",
    "threadId": "R_SO_4_464756496"
}

# 单曲歌 R_SO_4_1313118277
# 25706282
# 歌单 "A_PL_0_2022186054"

# 服务于d函数的
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'nYXLafpydDFlqRNh'  # 手动固定，人家的是随机的

def get_encSecKey():  # 由于i，e，f固定，那么c函数结果固定
    return "8f2960e5fa10ec2f643aa6a9f76f6b40f85dc4e0f7cfadc70370991ffa3234b08987d5f684619660448a8f0880dbc34436011b1f5b1091d1de4b448acc8ae259d71f84573229ade8ed9894ea55ebbfb6cd1a92e827c93ae14f5af34bdd994c004286dfa3fee40c12cf1d9da5cc3a33313a9f6b19cb10f1eb28d45d9cb8933590"


# 转化成16的倍数，为下方加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def enc_params(data, key):  # 加密过程
    iv = '0102030405060708'
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), iv=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode('utf-8'))  # 加密，加密的内容的长度必须是16的倍数，AES加密的逻辑
    # bs的结果不能直接转换成字节,需要先转换成base64

    return str(b64encode(bs), 'utf-8')  # 转换成字符串返回


# 把参数进行加密
def get_params(data):  # data为json字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second


def get_song(song):
    # 保存信息
    song_name = []
    song_id = []
    song_author = []
    song_source = []

    data['s'] = song
    resp = requests.post(url, data={
        'params': get_params(json.dumps(data)),
        'encSecKey': get_encSecKey()
    })
    resp_data = json.loads(resp.text)['result']['songs']
    song_lengh = len(resp_data)

    for i in range(song_lengh):
        # 获取歌名
        song_name.append(resp_data[i]['name'])
        # 获取id
        song_id.append(resp_data[i]['id'])
        # 获取作者
        song_author.append(resp_data[i]['ar'][0]['name'])
        # 获取来源来源歌单
        song_source.append(resp_data[i]['al']['name'])

    retu_data = {
        "code": 0,
        "msg": "",
        "count": song_lengh,
        "data": []
    }
    for i in range(song_lengh):
        info = {}
        info['id'] = song_id[i]
        info['name'] = song_name[i]
        info['author'] = song_author[i]
        info['source'] = song_source[i]
        retu_data['data'].append(info)

    print(resp_data)

    print(song_author)
    print(song_source)
    print(retu_data)

    return json.dumps(retu_data)

def get_comments(id):
    retu_data = {}
    # 保存用户名和评论
    user_name = []
    comments = []

    data_comment['rid'] = 'R_SO_4_' + str(id)
    data_comment['threadId'] = 'R_SO_4_' + str(id)

    resp = requests.post(url_comment, data={
        'params': get_params(json.dumps(data_comment)),
        'encSecKey': get_encSecKey()
    })

    resp_data = json.loads(resp.text)['data']



    hotComments = resp_data['hotComments']
    if hotComments == None:
        print('数据为空')
        retu_data['count'] = 0
        retu_data['data'] = []

        info = {}
        info['user'] = '该歌曲暂无热评哦~'
        info['comm'] = '暂无'
        retu_data['data'].append(info)
        return json.dumps(retu_data)

    lengh = len(resp_data['hotComments'])
    # 获取用户名
    for i in range(lengh):
        user_name.append(hotComments[i]['user']['nickname'])
    # 获取评论内容
    for i in range(lengh):
        comments.append(hotComments[i]['content'])

    with open('utils/comments.txt', 'w', encoding='utf-8') as f:
        for i in comments:
            f.writelines(i)


    retu_data['count'] = lengh
    retu_data['data'] = []
    for i in range(lengh):
        info = {}
        info['user'] = user_name[i]
        info['comm'] = comments[i]
        retu_data['data'].append(info)

    return json.dumps(retu_data)

# 发送请求得到评论
if __name__ == '__main__':
    song = '叙世'
    song = '夜空中最亮的星'
    id = '1458313766'
    # get_song(song)
    get_comments(id)

