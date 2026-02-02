import glob
import re

def upgrade_to_v4():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Inject Submit Button & Update "Show Answer" button visibility
        # Find where footer and btn are created
        # Pattern: const footer = document.createElement('div'); ... const btn = document.createElement('button');
        
        # We need to inject submitBtn before btn.
        # And maybe hide submitBtn if answered. 
        
        submit_btn_logic = """
        const footer = document.createElement('div');
        footer.className = 'mt-5 pt-4 border-top text-center';
        
        // Submit Button
        if (userAnswers[index] === undefined) {
            const submitBtn = document.createElement('button');
            submitBtn.className = 'btn btn-success px-4 me-2';
            submitBtn.innerHTML = '📝 答題';
            submitBtn.onclick = () => submitAnswer();
            footer.appendChild(submitBtn);
        }

        const btn = document.createElement('button');"""
        
        # Replace the creation block
        # We look for:
        # const footer = document.createElement('div');
        # footer.className = 'mt-5 pt-4 border-top text-center';
        # 
        # const btn = document.createElement('button');
        
        target_footer = r"const footer = document\.createElement\('div'\);\s+footer\.className = 'mt-5 pt-4 border-top text-center';\s+const btn = document\.createElement\('button'\);"
        
        # We need to construct replacement string carefully for regex
        # Actually, simpler string replace might be safer if indentation matches
        
        old_block = """const footer = document.createElement('div');
        footer.className = 'mt-5 pt-4 border-top text-center';
        
        const btn = document.createElement('button');"""
        
        if old_block in content:
            content = content.replace(old_block, submit_btn_logic)
        else:
            # Try regex if exact match fails due to whitespace
            content = re.sub(target_footer, submit_btn_logic, content, flags=re.DOTALL)

        # 2. Modify Option OnClick (Single/Multiple)
        # Old: onclick="checkAnswer(this, ${index}, ${optIdx}, event)"
        # New: onclick="toggleSelection(this, event)"
        
        # We need to pass event to stop propagation if needed?
        # Actually my helper toggleSelection will handle it.
        
        content = content.replace(
            "onclick=\"checkAnswer(this, ${index}, ${optIdx}, event)\"",
            "onclick=\"toggleSelection(this, event)\""
        )

        # 3. Modify Sub-Option OnClick
        # Old: onclick="checkSubAnswer(this, ${index}, ${optIdx}, ${subIdx}, event)"
        # New: onclick="toggleSelection(this, event)" (Reuse same generic toggle)
        
        content = content.replace(
            "onclick=\"checkSubAnswer(this, ${index}, ${optIdx}, ${subIdx}, event)\"",
            "onclick=\"toggleSelection(this, event)\""
        )

        # 4. Add Helper Functions & Submit Logic
        # We will inject these before renderQuestion
        
        new_js_logic = """
    function toggleSelection(element, event) {
        const input = element.querySelector('input');
        if (event && event.target !== input) {
            if (input.type === 'radio') {
                input.checked = true;
                // For radio groups (sub-questions), we don't need to manually uncheck others, browser does it via 'name' attr.
            } else {
                input.checked = !input.checked;
            }
        }
    }

    function submitAnswer() {
        const item = quizData[currentIndex];
        const isMultiple = item.type === 'multiple';
        let savedAns = null;
        let isWrong = false;

        // 1. Collect Answer
        if (item.options && item.options.some(opt => typeof opt === 'string' && opt.includes('|'))) {
            // Quiz Type (Multi-part)
            // options is array of strings. Each string has pipes.
            // Rows = options.length.
            // We need to find checked sub-index for EACH row.
            
            let quizAnswers = [];
            let allAnswered = true;
            
            // Loop through "rows" (optIdx)
            // Look for name="q${currentIndex}_opt${optIdx}"
            const options = item.quiz || item.options || [];
            
            for(let r=0; r<options.length; r++) {
                const inputs = document.querySelectorAll(`input[name="q${currentIndex}_opt${r}"]`);
                let selectedSub = -1;
                inputs.forEach((inp, subIdx) => {
                    if(inp.checked) selectedSub = subIdx;
                });
                
                if(selectedSub === -1) {
                    allAnswered = false;
                    break;
                }
                quizAnswers.push(selectedSub);
            }
            
            if (!allAnswered) {
                alert('請回答所有小題！');
                return;
            }
            savedAns = quizAnswers;
            
            // Validate Quiz
            let answers = item.answer;
            if (!Array.isArray(answers)) answers = [answers];
            
            // Compare each row
            for(let r=0; r<quizAnswers.length; r++) {
                // Correct answer in JSON is 1-based index usually?
                // checkSubAnswer logic: const correctSubIdx = parseInt(answers[optIdx]) - 1;
                // So yes, 1-based.
                let correctSub = parseInt(answers[r]) - 1;
                if (quizAnswers[r] !== correctSub) {
                    isWrong = true;
                }
            }

        } else if (isMultiple) {
            // Multiple Choice
            const inputs = document.querySelectorAll(`input[name="q${currentIndex}"]`);
            let checked = [];
            inputs.forEach((inp, idx) => {
                if (inp.checked) checked.push(idx);
            });
            
            if (checked.length === 0) {
                alert('請選擇答案！');
                return;
            }
            savedAns = checked;
            
            // Validate
            // correctIndices logic from checkAnswer
            let answers = item.answer;
            if (!Array.isArray(answers)) answers = [answers];
            const correctIndices = answers.map(a => parseInt(a) - 1);
            
            // Logic: Must match exactly? Or partial? Usually exact match.
            // Check if all checked are correct AND all correct are checked.
            if (checked.length !== correctIndices.length) isWrong = true;
            else {
                // Sort and compare strings or loop
                checked.sort();
                correctIndices.sort((a,b) => a-b);
                for(let i=0; i<checked.length; i++) {
                    if (checked[i] !== correctIndices[i]) isWrong = true;
                }
            }
            
        } else {
            // Single Choice
            const inputs = document.querySelectorAll(`input[name="q${currentIndex}"]`);
            let selected = -1;
            inputs.forEach((inp, idx) => {
                if (inp.checked) selected = idx;
            });
            
            if (selected === -1) {
                alert('請選擇答案！');
                return;
            }
            savedAns = selected;
            
            // Validate
            let answers = item.answer;
            if (!Array.isArray(answers)) answers = [answers];
            const correctIndices = answers.map(a => parseInt(a) - 1);
            
            if (!correctIndices.includes(selected)) isWrong = true;
        }

        // 2. Save
        userAnswers[currentIndex] = savedAns;
        if (isWrong) {
            wrongSet.add(currentIndex);
        } else {
            // Maybe remove from wrong set if correct now? 
            // "曾經選錯" (Ever wrong) implies persistence.
            // But if I retry and get it right, usually it stays "Ever Wrong" until reset?
            // Or does it clear?
            // User said "答對與答錯" (Correct and Wrong).
            // If I answer correctly NOW, it is currently "Correct".
            // But if I previously got it wrong, do I still mark it red?
            // Grid logic in V3: if (wrongSet.has(i)) -> Red.
            // If I don't remove it from wrongSet, it stays Red even if I answer correctly now.
            // I'll keep it Red (Strict mode) or remove it?
            // Usually "Correction" allows clearing the wrong status.
            // I will remove from wrongSet if correct.
            if (wrongSet.has(currentIndex)) wrongSet.delete(currentIndex);
        }
        saveState();

        // 3. Update UI (Reload question to apply 'Already Answered' logic)
        renderQuestion(currentIndex);
    }
    """
        
        # Inject functions before renderQuestion
        content = content.replace('function renderQuestion(index) {', new_js_logic + '\n    function renderQuestion(index) {')

        # 5. Fix Restore Logic in renderQuestion for Quiz Type
        # V3 script didn't implement Quiz restore. V4 must.
        # Find the restore block
        
        restore_quiz_logic = """
            } else {
                # Quiz Type (Multi-part)
                if (Array.isArray(saved) && item.options && item.options.some(opt => typeof opt === 'string' && opt.includes('|'))) {
                     # It is a quiz type array
                     saved.forEach((subSel, rowIdx) => {
                         # Find input: name="q${index}_opt${rowIdx}"
                         # But we need the specific input by ID?
                         # renderQuestion generates IDs: id="o${optIdx}_s${subIdx}"
                         # where optIdx is Row, subIdx is Col.
                         const input = document.getElementById(`o${rowIdx}_s${subSel}`);
                         if (input) {
                             input.checked = true;
                             const wrapper = input.closest('.sub-opt-container');
                             
                             # Validation Visuals
                             # Correct answer for this row
                             let answers = item.answer;
                             if (!Array.isArray(answers)) answers = [answers];
                             let correctSub = parseInt(answers[rowIdx]) - 1;
                             
                             if (subSel === correctSub) {
                                 wrapper.classList.add('correct');
                             } else {
                                 wrapper.classList.add('incorrect');
                                 # Show correct one
                                 const correctInput = document.getElementById(`o${rowIdx}_s${correctSub}`);
                                 if(correctInput) correctInput.closest('.sub-opt-container').classList.add('correct');
                             }
                         }
                     });
                     
                     # Disable all sub inputs
                     options.forEach((_, r) => {
                         const subInps = document.querySelectorAll(`input[name="q${index}_opt${r}"]`);
                         subInps.forEach(i => i.disabled = true);
                     });
                } else if (Array.isArray(saved)) {
                    # Multiple Choice (Existing V3 logic)
        """
        
        # We need to replace the `else { // Multiple Choice` block in the existing restore logic.
        # This is getting specific.
        
        # Existing block in V3:
        # } else {
        #    # Multiple Choice
        #    if (Array.isArray(saved)) {
        
        # I will replace `} else {
                # Multiple Choice` with `} else { // Complex check`
        
        # Since I can't easily match exactly, I'll rely on the structure I injected in V3.
        # It was:
        #             } else {
        #                 # Multiple Choice
        #                 if (Array.isArray(saved)) {
        
        # I'll replace that entire else block start.
        
        target_restore_else = r"\} else \{\s+// Multiple Choice\s+if \(Array\.isArray\(saved\)\) \{" 
        
        new_restore_else = """} else {
                # Complex Types (Quiz or Multiple)
                # Check if Quiz
                const isQuiz = item.options && item.options.some(opt => typeof opt === 'string' && opt.includes('|'));
                
                if (isQuiz && Array.isArray(saved)) {
                     # Quiz Restore
                     saved.forEach((subSel, rowIdx) => {
                         const input = document.getElementById(`o${rowIdx}_s${subSel}`);
                         if (input) {
                             input.checked = true;
                             const wrapper = input.closest('.sub-opt-container');
                             
                             let answers = item.answer;
                             if (!Array.isArray(answers)) answers = [answers];
                             let correctSub = parseInt(answers[rowIdx]) - 1;
                             
                             if (subSel === correctSub) {
                                 wrapper.classList.add('correct');
                             } else {
                                 wrapper.classList.add('incorrect');
                                 const correctInput = document.getElementById(`o${rowIdx}_s${correctSub}`);
                                 if(correctInput) correctInput.closest('.sub-opt-container').classList.add('correct');
                             }
                         }
                     });
                     # Disable
                     const options = item.quiz || item.options || [];
                     options.forEach((_, r) => {
                         const subInps = document.querySelectorAll(`input[name="q${index}_opt${r}"]`);
                         subInps.forEach(i => i.disabled = true);
                     });
                     
                } else if (Array.isArray(saved)) {"""
        
        # Replace
        content = re.sub(target_restore_else, new_restore_else, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    upgrade_to_v4()
