# 51zhy_pdf_downloader

腳本思路過程請參考:https://medium.com/@mikeyjou/%E6%82%85%E8%AE%80-%E5%8F%AF%E7%9F%A5-pdf%E4%B8%8B%E8%BC%89%E4%B9%8B%E6%97%85-ee31ee9ef88


使用方法:
照medium文章將專案上JS放上chrome，在書本頁面重新整理下載JSON檔，將JS下載下來的key.json、authorize.json檔放在跟py檔同一資料夾
直接python3 51zhy.py即可
腳本很簡單並且防呆也沒有做得很好，如果出現解密錯誤通常是授權過期，需要重新去網頁上下載json檔案
