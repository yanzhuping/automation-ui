###验证码识别
from aip import AipOcr
from os import path
from PIL import Image
from selenium import webdriver
import time

def get_photo(file_name):
  driver = webdriver.Chrome()
  driver.get("https://qa.tranderpay.com/#/login")
  driver.maximize_window()
  driver.execute_script('document.body.style.zoom="0.8"')
  time.sleep(2)
    # 1.登录页面截图并保存在C:/test.png
  driver.save_screenshot(file_name)
    # 2.获取图片验证码坐标和尺寸
  code_element = driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/form/div[4]/div[2]/img')
  left = code_element.location['x']
  top = code_element.location['y']
  right = code_element.size['width'] + left
  height = code_element.size['height'] + top
  im = Image.open(file_name)
    # 截取图片验证码
  img = im.crop((left, top, right, height))
    #zhanshijietu
    # img.show()
  driver.close()
  return img

#jiangtupianzhuanhuidu
def processing_image(file_name):
  img=get_photo(file_name)
  img = img.convert("L")  # 转灰度
  pixdata = img.load()
  w, h = img.size
  threshold = 155
  # 遍历所有像素，大于阈值的为黑色
  for y in range(h):
    for x in range(w):
      if pixdata[x, y] < threshold:
        pixdata[x, y] = 0
      else:
        pixdata[x, y] = 255



  data = img.getdata()
  w, h = img.size
  black_point = 0
  for x in range(1, w - 1):
    for y in range(1, h - 1):
      mid_pixel = data[w * y + x]  # 中央像素点像素值
      if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
        top_pixel = data[w * (y - 1) + x]
        left_pixel = data[w * y + (x - 1)]
        down_pixel = data[w * (y + 1) + x]
        right_pixel = data[w * y + (x + 1)]
        # 判断上下左右的黑色像素点总个数
        if top_pixel < 10:
          black_point += 1
        if left_pixel < 10:
          black_point += 1
        if down_pixel < 10:
          black_point += 1
        if right_pixel < 10:
          black_point += 1
        if black_point < 1:
          img.putpixel((x, y), 255)
          black_point = 0
  # img.show()
  img.save(file_name)

def baiduOCR(picfile):
  filename = path.basename(picfile)#图片名称
  print(filename)
  APP_ID = '16989624'
  API_KEY = 'ZLevVvfyPNKNqzN8TXOFbRz7'
  SECRET_KEY = '0OEdF5F3uG6yAyiDNIYMfYfYO1qPCnfG'
  client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
  i = open(picfile, 'rb')
  img = i.read()

  #普通标准
  # message = client.basicAccurate(img)
  #高精准
  message=client.basicAccurate(img)
  i.close()
  for text in message.get('words_result'):#识别的内容
    print(text.get('words'))

def pri_result(file_name):
  processing_image(file_name)
  baiduOCR(file_name)

if __name__ == '__main__' :
  pri_result(r'C:\Users\admin\Desktop\test.png')