# ITS Database 技術重點 - 表格彙整 (ITS_DATABASE_TECH.md)

本文件整理自 `www/ITS_Database/questions_ITS_Database.json`，提取其中包含的技術對照表與語法說明。

---

## 題目 ID: 5

| 指令 (Command) | 公式 / 語法結構 | 參數與功能說明 |
| --- | --- | --- |
| 一、 DDL (Data Definition Language) - 資料定義語言：定義資料庫結構 |
| CREATE | CREATE TABLE [表名] ([欄位] [型別] [約束]) | 建立新的資料表、視圖或預存程序。 CREATE TABLE Customer (   CustomerID int PRIMARY KEY, CustomerName nvarchar(255) NOT NULL); |
| ALTER | ALTER TABLE [表名] ADD [欄位]ALTER TABLE [表名] DROP COLUMN [欄位]ALTER TABLE [表名] ALTER COLUMN [欄位][型別] | 修改現有的資料庫結構，例如增加或刪除欄位。注意：MSSQL(SQL Server / T-SQL) 不可加括號。ALTER TABLE Customer ADD District INTEGER;//新增欄位District 型態(int)ALTER TABLE Customer ALTER COLUMN District bigint ;//修改欄位District 型態(bigint) |
| DROP | DROP TABLE/PROCEDURE [名稱] | 完全刪除物件（結構與內容皆不保留）。  DROP TABLE Customer |
| TRUNCATE | TRUNCATE TABLE [表名] | 快速清空整張表的記錄，但保留表格結構。 TRUNCATE TABLE Customer; |
| 二、 DML (Data Manipulation Language) - 資料操作語言：處理記錄內容 |
| INSERT | INSERT INTO [表名] ([欄位]) VALUES ([值]) | 將新記錄插入資料表。 INSERT INTO Customer (CustomerID, CustomerName, District) VALUES (1,N'張小明', 100) ; |
| UPDATE | UPDATE [表名] SET [欄位]=[值] WHERE [條件] | 修改現有資料；省略 WHERE 會更新全表。 UPDATE Customer SET District = 900 WHERE CustomerID = 1; |
| DELETE | DELETE FROM [表名] WHERE [條件] | 刪除表中的特定記錄。 DELETE FROM Customer WHERE CustomerID = 1 |
| 三、 DQL (Data Query Language) - 資料查詢語言：檢索資料 |
| SELECT | SELECT [欄位] FROM [表名] WHERE [條件] | 從資料庫中檢索資料，是最常用的指令 SELECT * FROM Customer; SELECT COLUMN_NAME, DATA_TYPE  FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_NAME = 'Customer' |
| JOIN | SELECT * FROM A JOIN B ON A.ID = B.ID | 結合多張表的資料（如 INNER, LEFT JOIN）。 SELECT   A.CustomerName, B.OrderAmount FROM Customer A JOIN Orders B ON A.CustomerID = B.CustomerID; |
| 四、 DCL (Data Control Language) - 資料控制語言：權限管理 |
| GRANT | GRANT [權限] ON [物件] TO [使用者] | 賦予使用者存取特定資料庫物件的權限。 |
| REVOKE | REVOKE [權限] ON [物件] FROM [使用者] | 撤銷先前賦予使用者的權限。 |
| 五、 TCL (Transaction Control Language) - 交易控制語言：確保原子性 |
| BEGIN TRANSACTION | BEGIN TRANSACTION | 標記交易處理的開始點。 |
| COMMIT | COMMIT | 永久儲存交易期間的所有變更。 |
| ROLLBACK | ROLLBACK | 將變更復原至交易前的狀態（撤銷操作）。 |

| 類別 | 指令公式 / 查詢對象 | 參數與功能說明 |
| --- | --- | --- |
| 查欄位 | SELECT * FROM INFORMATION_SCHEMA.COLUMNS | 查詢所有表或特定表的欄位名稱、型別、是否允許 NULL。 |
| 查表格 | SELECT * FROM INFORMATION_SCHEMA.TABLES | 列出資料庫中所有的資料表 (Base Table) 與視圖 (View)。 |
| 查程序 | SELECT * FROM INFORMATION_SCHEMA.ROUTINES | 查詢預存程序 (Stored Procedures) 與函數 (Functions) 的清單。 |
| 查參數 | SELECT * FROM INFORMATION_SCHEMA.PARAMETERS | 查詢預存程序中定義的參數（如 @UserName, @Age）。 |
| 指令 | 目標表是否存在？ | 語言類別 | 您的筆記重點 |
| SELECT INTO | 不存在 (自動建立新表) | DML | 快速備份，像「影印」出一張新紙。 |
| INSERT INTO ...  SELECT | 已存在 | DML | 將資料「倒進」現有的容器中。 |

---

## 題目 ID: 9

| 正確術語 | 英文名稱 | 參數與功能說明 |
| --- | --- | --- |
| 串聯刪除 | Cascade Delete | 唯一正確術語。當主資料表（父表）的一列被刪除時，自動刪除所有關聯表（子表）中對應的列。 |
| 瀑布法 | Waterfall | 錯誤。這是軟體開發流程 (SDLC) 的模型名稱，與資料庫刪除無關。 |
| 骨牌法 | Domino | 錯誤。這只是描述連鎖反應的形容詞，並非 SQL 語法關鍵字。 |
| 繼承法 | Inherited | 錯誤。這通常指物件導向程式設計 (OOP) 的特性，而非刪除規則。 |

---

## 題目 ID: 11

| 語法狀態 | 範例程式碼 | 執行結果 |
| --- | --- | --- |
| 錯誤語法 | ADD Prefix varchar(4) DEFAULT; | ERROR |
| 正確語法 (常數) | ADD Prefix varchar(4) DEFAULT 'N/A' | SUCCESS |
| 正確語法 (數值) | ADD Score int DEFAULT 0 | SUCCESS |
| 正確語法 (函數) | ADD CreateDate date DEFAULT GETDATE() | SUCCESS |

---

## 題目 ID: 33

| 指令 (Command) | 公式 / 語法結構 | 參數與功能說明 |
| --- | --- | --- |
| OUTER JOIN | 改為 LEFT OUTER JOIN | SQL 需要明確方向（左、右或全連線）。 |
| WHERE | 改為 ON | ON 用於定義表與表之間的「橋樑」；WHERE 用於橋蓋好後的「資料過濾」。 |
| student.courseID | 改為 students.courseID | 注意資料表名稱的單複數（小細節，但考試常考拼字一致性）。 |

| 指令 (Command) | 公式 / 語法結構 | 參數與功能說明 |
| --- | --- | --- |
| SELECT | students.name, courses.name | 選取結果：你想從這兩張表分別拿什麼資料？ |
| FROM + JOIN | students INNER JOIN courses | 設定橋樑：哪兩張表要黏在一起？ |
| ON | students.courseID = courses.courseID | 匹配規則：靠哪個欄位來對齊資料？ |

---

## 題目 ID: 35

| 運算元 | 邏輯 | 結果範圍 | 是否自動去重複？ |
| --- | --- | --- | --- |
| UNION | 聯集 (OR)A∪B | 全部 (A + B) | 是 |
| UNION ALL | 聯集 (純合併)A∪B | 全部 (A + B) | 否 (保留重複) |
| INTERSECT | 交集 (AND)A∩B | 只有重疊的部分 | 是 |
| EXCEPT | 差集 (Minus) A−(A∩B) 或 A∖B | A 有但 B 沒有的部分 | 是 |

| 圖片標籤 | 紅色/橘色選中區域 | 集合代數公式 | 對應 SQL 關鍵字 |
| --- | --- | --- | --- |
| A | 左圓全紅 (含交集) | A | LEFT JOIN |
| B | 右圓全紅 (含交集) | B | RIGHT JOIN |
| A' | A 留白，其餘全橘 | A′=U−A | NOT A |
| B' | B 留白，其餘全橘 | B′=U−B | NOT B |
| A ∪ B | 雙圓全紅 (聯集) | A∪B | UNION |
| A ∩ B | 只有中間橄欖紅 | A∩B | INTERSECT |

---

## 題目 ID: 64

| 特性 | 叢集索引 (Clustered) | 非叢集索引 (Non-Clustered) |
| --- | --- | --- |
| 數量 | 一表僅限一個。 | 一表可有多個。 |
| 物理順序 | 索引順序 = 資料存放順序。 | 索引順序 ≠ 資料存放順序。 |
| 內容 | 葉層就是資料列本身。 | 葉層是鍵值 + 指向資料的指標。 |
| 搜尋效率 | 極快（範圍查詢最強）。 | 稍慢（找到索引後還要去「查表」）。 |

---

