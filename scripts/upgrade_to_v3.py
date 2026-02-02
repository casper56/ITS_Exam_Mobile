import glob
import re
import os

def upgrade_to_v3():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path and 'ITS_' not in file_path and 'AI900' not in file_path: continue # Skip main index
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update Legend
        # Old: 未讀, 已讀, 錯誤, 當前
        # New: 未讀, 答對, 答錯
        # We find the sidebar content div
        legend_start = '<div class="d-flex justify-content-between small mb-2 text-muted">'
        legend_end = '</div>'
        
        if legend_start in content:
            new_legend = """<div class="d-flex justify-content-between small mb-2 text-muted">
                <span><span style="display:inline-block;width:10px;height:10px;background:#fff;border:1px solid #ccc"></span> 未讀</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#d1e7dd;border:1px solid #badbcc"></span> 答對</span>
                <span><span style="display:inline-block;width:10px;height:10px;background:#f8d7da;border:1px solid #f5c2c7"></span> 答錯</span>
            </div>"""
            # Use regex to replace the block
            content = re.sub(r'<div class="d-flex justify-content-between small mb-2 text-muted">.*?</div>', new_legend, content, flags=re.DOTALL)

        # 2. JS State Init
        if 'let userAnswers = {};' not in content:
            # Add userAnswers and ANSWERS_KEY
            content = content.replace('let wrongSet = new Set();', 'let wrongSet = new Set();\n    let userAnswers = {};')
            # Extract prefix for key
            match = re.search(r"const WRONG_KEY = '(.+)_wrong_v1';", content)
            if match:
                prefix = match.group(1)
                content = content.replace(match.group(0), f"{match.group(0)}\n    const ANSWERS_KEY = '{prefix}_answers_v1';")

        # 3. JS loadState
        if 'const savedAnswers = localStorage.getItem(ANSWERS_KEY);' not in content:
            load_logic = """
        const savedAnswers = localStorage.getItem(ANSWERS_KEY);
        if (savedAnswers) {
            userAnswers = JSON.parse(savedAnswers);
        }
            """
            content = content.replace('if (savedWrong) {', load_logic + 'if (savedWrong) {')

        # 4. JS saveState
        if 'localStorage.setItem(ANSWERS_KEY' not in content:
            content = content.replace('localStorage.setItem(WRONG_KEY, JSON.stringify([...wrongSet]));', 
                                      'localStorage.setItem(WRONG_KEY, JSON.stringify([...wrongSet]));\n        localStorage.setItem(ANSWERS_KEY, JSON.stringify(userAnswers));')

        # 5. JS resetProgress
        if 'localStorage.removeItem(ANSWERS_KEY);' not in content:
            content = content.replace('localStorage.removeItem(WRONG_KEY);', 
                                      'localStorage.removeItem(WRONG_KEY);\n            localStorage.removeItem(ANSWERS_KEY);')

        # 6. JS updateUI (Grid Logic)
        # Remove "Current" background logic, prioritize Wrong/Correct
        # Old: 
        # if (i === currentIndex) node.classList.add('active');
        # else if (wrongSet.has(i)) node.classList.add('wrong');
        # else if (visitedSet.has(i)) node.classList.add('visited');
        
        # New:
        # if (i === currentIndex) node.classList.add('current-node'); # We'll verify this class exists or add style
        # if (wrongSet.has(i)) node.classList.add('wrong');
        # else if (userAnswers[i] !== undefined) node.classList.add('visited'); # Reusing visited style for Correct
        
        # We need to replace the entire loop logic in updateUI
        old_loop_logic = r"for \(let i = 0; i < quizData\.length; i\+\+\) \{.*?\}\s*\}"
        
        new_loop_logic = """for (let i = 0; i < quizData.length; i++) {
            const node = document.getElementById(`node-${i}`);
            if (node) {
                node.className = 'q-node';
                if (i === currentIndex) node.style.border = '2px solid #0d6efd'; # Active indicator
                
                if (wrongSet.has(i)) {
                    node.classList.add('wrong');
                } else if (userAnswers[i] !== undefined) {
                    node.classList.add('visited'); # Visited = Correct in this context (Green)
                }
            }
        }
    }"""
        # We replace the content of the loop.
        # Finding the loop body is tricky with regex.
        # Let's target the inner part.
        
        # Target:
        # const node = document.getElementById(`node-${i}`);
        # if (node) {
        # ...
        # }
        
        target_inner = """if (node) {
                node.className = 'q-node';
                if (i === currentIndex) node.classList.add('active');
                else if (wrongSet.has(i)) node.classList.add('wrong');
                else if (visitedSet.has(i)) node.classList.add('visited');
            }"""
            
        replacement_inner = """if (node) {
                node.className = 'q-node';
                if (i === currentIndex) {
                    node.style.border = '2px solid #0d6efd';
                    node.style.transform = 'scale(1.1)';
                }
                
                if (wrongSet.has(i)) {
                    node.classList.add('wrong');
                } else if (userAnswers[i] !== undefined) {
                    node.classList.add('visited');
                }
            }"""
        
        # Normalize whitespace for replacement
        content = content.replace(target_inner, replacement_inner)
        
        # Also clean up the 'active' style if we are not using it? 
        # Actually .active style sets background blue. We removed .active class application, so blue bg is gone for current. Good.

        # 7. JS checkAnswer (Logic Update)
        # We need to capture the answer.
        # Single choice:
        # if (correctIndices.includes(optIdx)) { ... }
        
        # We need to inject `userAnswers[qIdx] = optIdx;`
        # And for Multiple: `userAnswers[qIdx] = [indices...]`
        
        # This is getting complex to regex replace safely.
        # Strategy: Replace the entire checkAnswer function if possible, or inject at top?
        # But we need it to update specific lines.
        
        # Single Choice Injection:
        # Search: if (!isMultiple) {
        # Inject: userAnswers[qIdx] = optIdx; saveState();
        
        if 'userAnswers[qIdx] = optIdx;' not in content:
            content = content.replace('if (!isMultiple) {', 'if (!isMultiple) {\n            userAnswers[qIdx] = optIdx;\n            saveState();')
            
        # Multiple Choice Injection:
        # This is harder because `optIdx` is just the clicked one. We need the full set of checked items.
        # But wait, the user requirement says "Show previously answered answer".
        # For multiple choice, we need to save the state of ALL checkboxes.
        # My current structure `userAnswers[qIdx] = optIdx` is fine for Single.
        # For multiple, I should probably scan all inputs.
        
        # Let's simplify.
        # Update `checkAnswer` to:
        # Store answer.
        # If Single: store optIdx.
        # If Multiple: store array of checked indices.
        
        # I'll replace the function entirely. It's safer.
        new_checkAnswer = """function checkAnswer(element, qIdx, optIdx, event) {
        const item = quizData[qIdx];
        const isMultiple = item.type === 'multiple';
        let answers = item.answer;
        if (!Array.isArray(answers)) answers = [answers];
        const correctIndices = answers.map(a => parseInt(a) - 1);
        const input = element.querySelector('input');

        if (event && event.target !== input) {
            if (isMultiple) {
                input.checked = !input.checked;
            } else {
                input.checked = true;
            }
        }
        
        # Save Answer
        if (!isMultiple) {
            userAnswers[qIdx] = optIdx;
        } else {
            # Collect all checked
            const inputs = document.querySelectorAll(`input[name="q${qIdx}"]`);
            let checked = [];
            inputs.forEach((inp, idx) => {
                if (inp.checked) checked.push(idx);
            });
            userAnswers[qIdx] = checked;
        }
        saveState();

        if (!isMultiple) {
            if (item.answered) return;
            item.answered = true;

            const inputs = document.querySelectorAll(`input[name="q${qIdx}"]`);
            inputs.forEach(i => i.disabled = true);

            if (correctIndices.includes(optIdx)) {
                element.classList.add('correct');
            } else {
                element.classList.add('incorrect');
                wrongSet.add(qIdx); # Mark as wrong
                saveState(); # Save wrong set
                const correctInput = document.querySelector(`input[name="q${qIdx}"][id="o${correctIndices[0]}"]`);
                if (correctInput) correctInput.closest('.option-item').classList.add('correct');
            }
            const el = document.getElementById('ans-section');
            el.style.display = 'block';
        } else {
            # Multiple Choice - Visual Feedback
            if (input.checked) {
                if (correctIndices.includes(optIdx)) {
                    element.classList.add('correct');
                    element.classList.remove('incorrect');
                } else {
                    element.classList.add('incorrect');
                    wrongSet.add(qIdx); # Mark as wrong if ANY wrong option selected
                    saveState();
                    element.classList.remove('correct');
                }
            } else {
                element.classList.remove('correct');
                element.classList.remove('incorrect');
            }
        }
    }"""
    
        # Replace the existing checkAnswer function
        # Regex to match the whole function body
        content = re.sub(r'function checkAnswer\(.*?\n    }', new_checkAnswer, content, flags=re.DOTALL)

        # 8. JS renderQuestion (Restore State)
        # Insert logic at end of renderQuestion (before updateUI)
        restore_logic = """
        # Restore User Answer
        if (userAnswers[index] !== undefined) {
            const item = quizData[index];
            const isMultiple = item.type === 'multiple';
            let answers = item.answer;
            if (!Array.isArray(answers)) answers = [answers];
            const correctIndices = answers.map(a => parseInt(a) - 1);
            
            const saved = userAnswers[index];
            
            if (!isMultiple) {
                # Single Choice
                const input = document.getElementById(`o${saved}`);
                if (input) {
                    input.checked = true;
                    const wrapper = input.closest('.option-item');
                    
                    # Visuals
                    if (correctIndices.includes(saved)) {
                        wrapper.classList.add('correct');
                    } else {
                        wrapper.classList.add('incorrect');
                        # Show correct
                        const correctInput = document.querySelector(`input[name="q${index}"][id="o${correctIndices[0]}"]`);
                        if (correctInput) correctInput.closest('.option-item').classList.add('correct');
                    }
                }
            } else {
                # Multiple Choice
                if (Array.isArray(saved)) {
                    saved.forEach(idx => {
                        const input = document.getElementById(`o${idx}`);
                        if (input) {
                            input.checked = true;
                            const wrapper = input.closest('.option-item');
                            if (correctIndices.includes(idx)) {
                                wrapper.classList.add('correct');
                            } else {
                                wrapper.classList.add('incorrect');
                            }
                        }
                    });
                }
            }
            
            # Disable inputs
            const inputs = document.querySelectorAll(`input[name="q${index}"]`);
            inputs.forEach(i => i.disabled = true);
            
            # Show Explanation
            const el = document.getElementById('ans-section');
            el.style.display = 'block';
        }
        """
        
        if '// Restore User Answer' not in content:
            content = content.replace('updateUI();', restore_logic + '\n        updateUI();')

        # 9. Handle checkSubAnswer (Quiz type)
        # Similar restore logic needed for Sub answers?
        # User requirement: "分頁都建立曾經選錯的題目紀錄"
        # The main logic handles Single/Multiple. "multioption" (Quiz) is complex.
        # I'll stick to the main request. `userAnswers` map currently stores basic types.
        # If `multioption` needs support, it requires more complex logic.
        # Given "checkSubAnswer" exists, I should probably patch it too or leave it.
        # I'll patch checkSubAnswer to store state too.
        
        # Patch checkSubAnswer to store: `userAnswers[qIdx] = { subIdx: optIdx }`?
        # This gets complicated. I will implement basic restore for single/multiple first.
        # If I break multioption, that's bad.
        # I'll add a simple `wrongSet.add` to checkSubAnswer (already done in previous script).
        # For restore, I'll skip multioption for now to avoid breaking it, or just add basic support.
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    upgrade_to_v3()
