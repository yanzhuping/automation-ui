import json
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
restime = []
OK=[]

class Restime():
    def API(self,URL2,param):
        try:
            r = requests.get(URL2, params=param, timeout=10)
            r.raise_for_status() # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            print(e)
        else:
            js = json.dumps(r.json())
            return [r.json(), r.elapsed.total_seconds(),js]
    def circulation(self,num,URL2,param):
        for i in range(num):
            restime.append(Restime.API(URL2,param)[1])
            if json.loads(Restime.API(URL2, param)[2])["message"]=='ok':
                OK.append(json.loads(Restime.API(URL2, param)[2])["message"])
                logger.info('请求第' + str(i+1) + '次，请求'+json.loads(Restime.API(URL2, param)[2])["message"]+',状态码：'
                            +json.loads(Restime.API(URL2, param)[2])["status"])
            else:
                logger.info('请求第' + str(i+1) + '次，请求' + json.loads(Restime.API(URL2, param)[2])["message"] +
                            ',状态码：' +json.loads(Restime.API(URL2, param)[2])["status"])
        print('测试次数：',num)
        print('响应次数：', len(restime))
        print('正常响应次数：', len(OK))
        print('总响应最大时长：', max(restime))
        print('总响应最小时长：', min(restime))
        print('总响应时长：', sum(restime))
        print('平均响应时长：', sum(restime) / len(restime))


if __name__ == '__main__':
 Restime=Restime()
 num=10 #压力测试次数
 URL2 = 'http://www.kuaidi100.com/query' #地址
 param = {'type' : 'zhongtong' , 'postid' :'73116039505988' } #参数
 Restime.circulation(num,URL2,param)