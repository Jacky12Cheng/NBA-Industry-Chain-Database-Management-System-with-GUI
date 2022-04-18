# NBA-Industry-Chain-Database-Management-System-with-GUI
Using SQL and tkinter to realize DBMS with GUI 


**背景**

此資料庫管理系統是以籃球運動的產業鏈為發想，除了球賽本身與其參與的成員外，亦將場外相關的球員經濟人與球迷等考慮進來，希望以這樣的概念來建置一個小型簡易的資料庫系統，來記錄球賽與球員和球隊之間的關係以及球迷在賽事中的進場紀錄等。


**此資料庫需求定義如下:**
- 每支球隊(TEAMs)被記錄著他們的球隊名稱、戰績、奪冠次數、所屬分區，每一場比賽一定會由多支球隊所參與，但並不是每支球隊都參與至每場球賽。
- 記錄每場球賽(GAMEs)的球賽編號、球賽時長、比賽場館、進場觀眾數，且每場球賽被一個或多個球員經紀人所贊助並同時記錄贊助金額；每個經紀人(AGENTs)會記錄其名字、年紀及電話號碼。
- 記錄球隊是否擁有過球員，而每個球員都一定都會被一個或多個球隊所擁有過，且每個球隊都擁有過一個或多個球員。
- 每個粉絲(FANs)進場過一場或多場球賽而每一場球賽都有球迷進場，每個粉絲會被記錄著粉絲編號、名字、支持的球隊及年紀。
- 球員(PLAYERs)被記錄著球員編號、名字、場上位置以及薪水；而多個球員可能被多個經紀人所經營，且每個產品必定屬於某個經紀人所經營。

**ER-diagram**

依據上述定義的需求所構成的ER-diagram如下所示:

![This is an image](https://github.com/Jacky12Cheng/NBA-Industry-Chain-Database-Management-System-with-GUI/blob/main/ER_Diagram_and_Relation_Schema/ER-diagram.png)

**關聯綱要(Relation Schema)**

將上圖的ER-diagram映射成關聯並經過第三正規化後形成的關聯綱要如下所示，總共形成八個關聯(表格)。
  
![This is an image](https://github.com/Jacky12Cheng/NBA-Industry-Chain-Database-Management-System-with-GUI/blob/main/ER_Diagram_and_Relation_Schema/Relation%20Schema.png)

- GAMEs紀錄每場比賽資訊及有進場的特定球迷
  - GNo(PK)
- TEAMs紀錄每個球隊資訊
  - TName(PK)
- SPONSOR紀錄每個經紀人所贊助的球賽及金額
  - GNo(PK)、PNo(PK)、ANo(PK)
- PLAY紀錄該場球賽是由哪個球員出賽與哪支球隊有參與
  - PNo(PK)、TName(PK)
- FANs紀錄球迷資訊
  - FNo(PK)
- BELONG_TO紀錄球員是否被特定球隊擁有過
  - TName(PK) 、PNo(PK)
- PLAYERs紀錄每個球員的資訊
  - PNo(PK)
- AGENT紀錄球員經紀人的資訊
  - PNo(PK)、ANo(PK)

**系統架構與環境及使用說明**
- 程式:Python3.7
- 編譯器:Anaconda3-Spyder

