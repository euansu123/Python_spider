from pyquery import PyQuery as pq
import os
import requests

class Baidu:

    def __init__(self,baiduname):
        self.url = f'https://tieba.baidu.com/f?kw={baiduname}&ie=utf-8'
        self.headers = {
            "User-Agent":"Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0) "
        }

    # 获取数据
    def get_data(self,url):
        res = requests.get(url,headers=self.headers)
        # print(res)
        return res.content

    # 解析帖子网址
    def parse_page(self,htmlpage):
        doc = pq(htmlpage)
        node_list = doc.find('.j_thread_list .threadlist_title a')
        # print(node_list.attr('href'))
        data_list = []
        # 遍历node_list，拿到当前贴吧页面的帖子链接
        for item in node_list.items():
            tmp = 'http://tieba.baidu.com' + item.attr('href') # 贴子链接
            # tmp['title'] = item.text() # 帖子名称
            data_list.append(tmp)
        # print(data_list)

        # 提取下一页的的链接
        page = doc.find('.thread_list_bottom #frs_list_pager .next').attr('href')
        nextpage = 'https:' + page
        # print(nextpage)
        return data_list,nextpage

    # 获取图片
    def parse_img_list(self,htmlpage):
        page_doc = pq(htmlpage)
        img_items = page_doc.find('.BDE_Image').items()
        img_list = []
        for img in img_items:
            image = img.attr('src')
            img_list.append(image)
            # print(img.attr('src'))
        return img_list

    # 存取图片
    def download(self,img_list):
        if not os.path.exists('tieba_images'):
            os.makedirs('tieba_images')
        for img in img_list:
            img_name = 'tieba_images/' + img.split('/')[-1]
            ima_data = self.get_data(img)
            with open(img_name, 'wb') as f:
                f.write(ima_data)

    def run(self):
        current_url = self.url
        while current_url:
            html_page = self.get_data(current_url)
            url_list,current_url = self.parse_page(html_page)
            for url in url_list:
                detail = self.get_data(url)
                img_list = self.parse_img_list(detail)
                self.download(img_list)



if __name__ == '__main__':
    baidu = Baidu('校花')
    baidu.run()