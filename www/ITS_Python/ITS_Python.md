# ITS Python 認證題庫統計分析 (2026-02-27 更新)

## 1. 題庫規模與組成
*   **總題數**：185 題
*   **官方版本 (1-94)**：94 題
*   **補充/模擬版本 (95-185)**：91 題

## 2. 題型分佈 (精確統計)
*   **單選題 (Single Choice)**：116 題
*   **複選題 (Multiple Choice)**：11 題
*   **多重下拉/題組 (Multi-option)**：58 題

## 3. 2026-02-27 系統性編排更新
今日針對全科系題庫執行了以下優化：
*   **ID 全域重索引**：因應題量微調，確保所有題目 ID 具備連續性且與 `config.json` 同步。
*   **模擬考權重校準**：基於最新題量分佈，調整了模擬考抽取演算法，確保高頻考點覆蓋率。

## 4. 考點分佈與出題權重評估

若以正式考試 **40 題** 為抽題標準，建議分佈如下：

| 類別 | 母體題數 | 佔比 | 建議考題數 | 強度評估 |
| :--- | :---: | :---: | :---: | :--- |
| D0_官方鑑定考點 | 8 | 4.3% | 2 | 🟢 適中 |
| D1_資料型別與運算子 | 46 | 24.9% | 10 | 🔴 高強度 |
| D2_流程控制與判斷 | 30 | 16.2% | 6 | 🟡 核心 |
| D3_輸入輸出與檔案 | 30 | 16.2% | 6 | 🟡 核心 |
| D4_函式與註解 | 33 | 17.8% | 7 | 🟡 核心 |
| D5_錯誤處理與測試 | 18 | 9.7% | 4 | 🟢 適中 |
| D6_模組與常用工具 | 20 | 10.8% | 4 | 🟡 核心 |

> **維護提醒**：本題庫已完成全量分析，建議考生優先練習高佔比類別以獲取認證基本盤。

## 5. 考前衝刺必勝策略 (超額訓練法)

(超額訓練法)

(超額訓練法)

本系統模擬考設定為 **60 題 / 50 分鐘**，而 ITS 實測僅 **40 題**。這種「超額訓練」配置是為了建立考生的容錯空間與抗壓性。

### 🎓 核心衝刺策略
1.  **耐力加強 (The 150% Rule)**：
    *   **策略**：實際考試 40 題，模擬考 60 題 (50% 增量)，鍛鍊專注力。
    *   **目標**：能在 60 題壓力下維持 80 分，實測 40 題將游刃有餘。

2.  **時間壓測 (0.8 Min/Question)**：
    *   **策略**：模擬考平均 50 秒處理 1 題。
    *   **目標**：能在 50 分鐘內穩健完成 60 題，實測時將有極大餘裕進行檢查。

3.  **官方池 (1-99) 反射機制**：
    *   **策略**：模擬考中 95% 抽自官方池。目標是「看到題目關鍵字即反射正確答案」。
    *   **必勝點**：實測 40 題極高機率全數出自這 99 題核心庫。

4.  **列印錯題報告**：
    *   **策略**：利用系統的「列印錯題」功能，在考前 24 小時針對曾出錯的題目進行深度解析閱讀。
    *   **複習點**：ITS 考試通常會有 2-3 題變形題，透過補充題 (100-190) 的練習可增加對語法細節的敏感度。

---

棊峰網頁
一、使用資料型別和運算子進行操作
1. 評估運算式以識別 Python 分配給變數的資料型別
2. 執行和分析資料和資料型別的操作
3. 根據運算子的優先順序確定執行順序
4. 選擇運算子以達到預期的結果
二、使用決策和迴圈進行流程控制
1. 建構並分析使用分支語句的程式碼段
2. 建構並分析執行迭代的程式碼段
三、輸入和輸出操作
1. 建構並分析執行檔案輸入 and 輸出操作的程式碼段
2. 建構並分析執行控制台輸入 and 輸出操作的程式碼段
四、程式碼文件和結構
1. 文件化程式碼段
2. 建構並分析包含函式定義的程式碼段
五、故障排除和錯誤處理
1. 分析、偵測並修正具有錯誤的程式碼段
2. 分析並建構處理例外狀況的程式碼段
3. 執行單元測試
六、使用模組和工具進行操作
1. 使用內建模組執行基本檔案系統和命令列操作
2. 使用內建模組解決複雜的運算問題件

ITS SPECIALIST EXAM OBJECTIVES
1. Operations using Data Types and Operators
1.1 Evaluate expressions to identify the data types Python assigns to variables
• str, int, float, and bool
1.2 Perform and analyze data and data type operations
• Data type conversion, indexing, slicing, construct data structures, lists, list operations (including sorting, merging, appending, inserting, removing, finding maximum and minimum, and reversing)
1.3 Determine the sequence of execution based on operator precedence
• Assignment (=, +=, -=, /=, %=, //=, **=), comparison (==, >=, <=, !=), logical (and, or, not), logical, arithmetic (+, -, /, //, %, **, unary + and -), identity (is), containment (in)
1.4 Select operators to achieve the intended results
• Assignment (=, +=, -=, /=, %=, //=, **=), comparison (==, >=, <=, !=), logical (and, or, not), logical, arithmetic (+, -, /, //, %, **, unary + and -), identity (is), containment (in)
2. Flow Control with Decisions and Loops
2.1 Construct and analyze code segments that use branching statements
• if, elif, else, nested and compound conditional expressions
2.2 Construct and analyze code segments that perform iteration
• while, for, break, continue, pass, nested loops, loops that include compound conditional expressions
3. Input and Output Operations
3.1 Construct and analyze code segments that perform file input and output operations
• open, close, read, write, append, check existence, delete, with statement
3.2 Construct and analyze code segments that perform console input and output operations
• Read input from console, print formatted text (string.format() method, f-String method), use command-line arguments
IT SPECIALIST EXAM OBJECTIVES
Python
Candidates for this exam should be able to recognize and write syntactically correct well-documented Python 3 code that will logically solve a given problem, correctly use data types supported by Python, and use common libraries to write a program that solves a complex problem.
Candidates are expected to have had at least 150 hours of instruction and/or hands-on experience with the Python programming language, be familiar with its features and capabilities, and understand how to write, debug, and maintain well-formed, well-documented Python code.
© 2025 Certiport, Inc. Certiport and the Certiport logo are registered trademarks of Certiport Inc. All other trademarks and registered trademarks are the property of their respective holders.

4. Code Documentation and Structure
4.1 Document code segments
• Use indentation, white space, comments, and docstrings; generate documentation by using pydoc
4.2 Construct and analyze code segments that include function definitions
• Call signatures, default values, return, def, pass
5. Troubleshooting and Error Handling
5.1 Analyze, detect, and fix code segments that have errors
• Syntax errors, logic errors, runtime errors
5.2 Analyze and construct code segments that handle exceptions
• try, except, else, finally, raise
5.3 Perform unit testing
• Unittest, functions, methods, and assert methods (assertIsInstance, assertEqual, assertTrue, assertIs, assertIn)
6. Operations using Modules and Tools
6.1 Perform basic file system and command-line operations by using built-in modules
• io, os, os.path, sys (importing modules, using modules to open, read, and check existence of files, command-line arguments)
6.2 Solve complex computing problems by using built-in modules
• Math (fabs, ceil, floor, trunc, fmod, frexp, nan, isnan, sqrt, isqrt, pow, pi) datetime (now, strftime, weekday), random (randrange, randint, random, shuffle, choice, sample)
IT SPECIALIST EXAM OBJECTIVES