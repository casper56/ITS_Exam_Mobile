/**
 * ITS 考試成績同步管理工具 (SyncManager)
 * 負責將模擬考成績同步至 localStorage['its_exam_history']，
 * 以供 study_checklist.html (進度表) 使用。
 */
const SyncManager = {
    HISTORY_KEY: 'its_exam_history',

    /**
     * 儲存單次模擬考成績。
     * @param {string} subjectName - 科目名稱 (需對應進度表的顯示名稱)
     * @param {number} score - 分數
     */
    saveExamResult: function(subjectName, score) {
        // 1. 防呆檢查：若科目名稱無效或為預留位置，則跳過
        if (!subjectName || subjectName === 'REPLACE_SYNC_NAME' || subjectName === 'Unknown') {
            console.warn('SyncManager: 無效的科目名稱，跳過同步。');
            return;
        }

        try {
            // 2. 讀取現有紀錄
            const history = JSON.parse(localStorage.getItem(this.HISTORY_KEY) || '[]');
            
            // 3. 準備當前數據
            const today = new Date().toLocaleDateString('en-CA'); // 強制輸出為 YYYY-MM-DD
            const timestamp = Date.now();
            
            const newEntry = {
                date: today,
                subject: subjectName,
                score: score,
                timestamp: timestamp
            };
            
            // 4. 加入紀錄並存回 LocalStorage
            history.push(newEntry);
            localStorage.setItem(this.HISTORY_KEY, JSON.stringify(history));
            
            console.log(`SyncManager: 已自動將 ${subjectName} 分數 (${score}) 同步至進度表 [日期: ${today}]`);
        } catch (e) {
            console.error('SyncManager: 儲存成績時發生錯誤', e);
        }
    }
};

/**
 * SyncManager Patch - 自動恢復 PDF 遺失紀錄
 */
(function() {
    const RECOVERY_DATA = [
        { subject: "ITS_AI", date: "2026-03-12", score: 97 },
        { subject: "ITS_AI", date: "2026-03-11", score: 97 },
        { subject: "ITS_程式設計", date: "2026-03-12", score: 95 },
        { subject: "ITS_程式設計", date: "2026-03-11", score: 92 },
        { subject: "ITS_Python", date: "2026-03-12", score: 97, note: "1" },
        { subject: "ITS_Python", date: "2026-03-12", score: 98 },
        { subject: "ITS_Python", date: "2026-03-11", score: 98, note: "2" },
        { subject: "ITS_Python", date: "2026-03-11", score: 98, note: "1" },
        { subject: "ITS_Python", date: "2026-03-11", score: 98 },
        { subject: "ITS_程式設計", date: "2026-03-10", score: 95, note: "1" },
        { subject: "ITS_程式設計", date: "2026-03-10", score: 95 },
        { subject: "ITS_程式設計", date: "2026-03-08", score: 97 },
        { subject: "ITS_Python", date: "2026-03-10", score: 97 },
        { subject: "ITS_Python", date: "2026-03-09", score: 98 },
        { subject: "ITS_Python", date: "2026-03-08", score: 98 },
        { subject: "ITS_Python", date: "2026-03-06", score: 93 },
        { subject: "ITS_AI", date: "2026-03-09", score: 97 },
        { subject: "ITS_AI", date: "2026-03-08", score: 95 },
        { subject: "ITS_AI", date: "2026-03-07", score: 97 },
        { subject: "ITS_Database", date: "2026-03-11", score: 95 },
        { subject: "ITS_Database", date: "2026-03-10", score: 100 },
        { subject: "ITS_Database", date: "2026-03-09", score: 95 },
        { subject: "ITS_Database", date: "2026-03-07", score: 95, note: "1" },
        { subject: "ITS_Database", date: "2026-03-07", score: 95 },
        { subject: "ITS_程式設計", date: "2026-03-07", score: 90 },
        { subject: "ITS_程式設計", date: "2026-03-06", score: 92 },
        { subject: "ITS_Database", date: "2026-03-06", score: 95 },
        { subject: "ITS_Python", date: "2026-03-05", score: 90 },
        { subject: "ITS_Database", date: "2026-02-23", score: 95 }
    ];

    const historyKey = 'its_exam_history';
    let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
    let changed = false;

    RECOVERY_DATA.forEach(record => {
        const exists = history.some(h => h.subject === record.subject && h.date === record.date && (!record.note || h.note === record.note));
        if (!exists) {
            history.push({
                ...record,
                timestamp: new Date(record.date).getTime(),
                recovered: true
            });
            changed = true;
        }
    });

    if (changed) {
        localStorage.setItem(historyKey, JSON.stringify(history));
        console.log('SyncManager: 已自動從 PDF 備份恢復遺失的練習紀錄。');
    }
})();
