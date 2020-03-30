# Crawl Chinese medical dialogues from haodf

Let's crawl down urls first.

You can execute the codes in this directory directly.

Before executing the codes, you will need to fill in User-Agent(用户代理) information of your brower in the codes. For Google Chrome, you can find it by accessing [chrome://version//](chrome://version//)

Fill it in headers in each python file:

```python
# example:
# headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    headers = 
```

Then you can execute the files from command line:

```
$ python3 crawl_date_url.py -year 2019
$ python3 craw_all_urls_in_one_year.py -year 2019
```

This is the first time I have crawled data from web. I would be very grateful if you can provide me some suggesstions or find any bugs in the code. (Actually I believe there are bugs in the code)



```
$ python3 crawl_actual_data.py -year **** -start_id 1
```

这份代码可能只适用于19年，20年以及18年的一部分，而且爬取速度堪忧，可以考虑改一下代码中的sleep时间，如果不用一些并行之类的办法的话。

这个命令用来提取\****年的具体对话数据，`start_id`是你想要的下一个对话的编号。

一般来说不会因为异常中断，并且会输出有问题的url到一个叫`problematic_urls_****`的文件中。

输入`control c`能让程序中断，并且输出当前正在处理的页面的url，当继续运行时，可以删掉`all_urls_in_****`中已经提取过的ur，最好也看一眼输出文件`conversation_in_****`的情况，需要在重新运行命令时重填一下`start_id`	，当然后期统一处理id也是可以的，文件打开方式已经是'a'（追加模式）

别忘了填一下`headers`



If you have any problems, please contact me:

Email:

shu_chen@pku.edu.cn

Wechat:

cs32963



