#作者:"小云"
#QQ:3521714145
#交流群:156517302

import urllib3
import re
from urllib import parse
import json
from threading import Thread  # 创建线程的模块

count=0
def iY(str):
   return input("\033[1;33;m"+str+"\033[0m")
def pR(str):
   print("\033[1;31;m"+str+"\033[0m")
def pY(str):
   print("\033[1;33;m"+str+"\033[0m")
def pB(str):
   print("\033[1;36;m"+str+"\033[0m")
class DL(Thread):
   def __init__(self,url,file):
      super().__init__()
      self.url=url
      self.file=file
   def run(self):
      # 创建一个连接池
      global count
      count=count+1
      poolManager=urllib3.PoolManager()
      resp=poolManager.request('GET',self.url)
      with open(self.file,"wb") as file:
         file.write(resp.data)
      resp.release_conn()
def getInfoBySong(name,type): 
   if name ==None or name=="":
      pR("歌曲名不能为空")
      return
   http=urllib3.PoolManager()
   res=http.request("POST","http://music.9q4.cn/",body="input="+parse.quote(name)+"&filter=name&type="+type+"&page=1",headers={
   "Accept":"application/json, text/javascript, */*; q=0.01",
   "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
   "Accept-Encoding":"gzip, deflate",
   "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
   "X-Requested-With":"XMLHttpRequest"
   })
   r=json.loads(res.data)
   return r["data"][0]
def home():
   global type
   global path
   cmd=iY("ygm->")
   if cmd=="/quit":
      exit()
   if cmd=="/config":
      pB("引擎:"+type+"\n"+"下载目录:"+path)
      return
   if re.findall("/en ",cmd):
      tmp=cmd.split("/en ")[1]
      if re.findall(tmp,"netease/qq/kugou/kuwo"):
         type=tmp
         pY("引擎更换成功,当前引擎:"+type)
      else:
         pR("不存在的引擎")
      return
   if re.findall("/path ",cmd):
      tmp=cmd.split("/path ")[1]
      if tmp!="" or tmp !=None:
         path=tmp
         pY("下载目录更换成功,当前目录:"+path)
      return
   else:
      info=getInfoBySong(cmd,type)
      if info!=None:
         song_name=info["title"]
         song_author=info["author"]
         song_type=info["type"]
         url=info["url"]
         file=path+song_name+"_"+song_author+".mp3"
         dl=DL(url,file)
         dl.start()
         pR("该歌曲已开始自动下载.......")
         pY("="*20)
         tip="歌名:"+song_name+"\n"+"歌手:"+song_author+"\n"+"来源:"+song_type+"\nurl:"+url
         pB(tip)
         pY("="*20)


if __name__ == '__main__':
   icon="""__    __  _____       ___  ___  
\ \  / / /  ___|     /   |/   | 
 \ \/ /  | |        / /|   /| | 
  \  /   | |  _    / / |__/ | | 
  / /    | |_| |  / /       | | 
 /_/     \_____/ /_/        |_| 1.0
 
  """
   pB(icon)
   path=iY("请指明文件存储目录(末尾带/)=>")
   if path=="":
      pR("下载目录请不要留空")
      exit()
   type=iY("请选择你需要使用的引擎[netease/qq/kugou/kuwo]:")
   if re.findall(type,"netease/qq/kugou/kuwo"):
      type="netease"
   while True:
      home()
