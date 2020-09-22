import requests
from lxml import etree
import os

class Baidu:

    def __init__(self,baiduname):
        self.url = f'https://tieba.baidu.com/f?kw={baiduname}&ie=utf-8'
        self.header = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0) '
        }

    # 获取网页数据
    def get_data(self,url):
        res = requests.get(url,headers=self.header)
        return res.content

    # 获取帖子网页
    def parse_url_list(self,htmlpage):
        xml_page = etree.HTML(htmlpage)
        # res = etree.tostring(xml_page)
        # print(res.decode())
        # url_list = xml_page.xpath('//*[@id="thread_list"]/li[2]/div/div[2]/div[1]/div[1]/a/@href') 取出li[2]的href属性，也即第二个帖子的href属性
        url_list = xml_page.xpath('//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a/@href')
        # 取出当前页面的所有li的href属性
        # print(url_list)
        # 拿到href属性后，访问百度贴吧，发现帖子的网址：https://tieba.baidu.com+“/p/6974108643”(帖子的href属性)
        tiezi_url = []
        for url in url_list:
            res_url = 'https://tieba.baidu.com' + url
            tiezi_url.append(res_url)
        # print(tiezi_url)
        # //*[@id="frs_list_pager"]/a[last()-1]/@href下一页
        next_url = xml_page.xpath('//*[@id="frs_list_pager"]/a[last()-1]/@href')
        print('https:' + next_url[0])
        return tiezi_url,'https:'+ next_url[0]

    # 获取网页中的图片列表
    def parse_img_list(self,htmlpage):
        xml_page = etree.HTML(htmlpage)
        # //*[@id="post_content_123509215078"]/img[1]图片的xpath
        # //*[@id="post_content_123509215078"]/img[2]
        # class="d_post_content j_d_post_content  clearfix" 图片存放的路径
        img_list = xml_page.xpath('//cc//div[contains(@class,"d_post_content")]/img[@class="BDE_Image"]/@src')
        # print("-"*50)
        # print(img_list)
        return img_list

    # 存取图片
    def download(self,img_list):
        # 检查是否存在目录，若不存在则创建目录
        if not os.path.exists('baidu_images'):
            os.makedirs('baidu_images')
        for img in img_list:
            img_name = 'baidu_images/' + img.split('/')[-1]
            # 确定图片名称：'http://tiebapic.baidu.com/forum/w%3D580/sign=d4a3dc0337a446237ecaa56aa8237246/cbcaa40f4bfbfbed12e590066ff0f736aec31ff4.jpg'
            # split切割产生一个数组，数组的最后一个元素[-1]即是cbcaa40f4bfbfbed12e590066ff0f736aec31ff4.jpg，也就是我们希望的图片名称
            ima_data = self.get_data(img)
            with open(img_name,'wb') as f:
                f.write(ima_data)



    def run(self):
        currenturl = self.url
        while currenturl:
            htmlpage = self.get_data(currenturl)
            # 获取网页数据
            url_list,currenturl = self.parse_url_list(htmlpage)
            for url in url_list:
                detail_data = self.get_data(url)
                img_list = self.parse_img_list(detail_data)
                self.download(img_list)

if __name__ == '__main__':
    baidu = Baidu('校花')
    baidu.run()