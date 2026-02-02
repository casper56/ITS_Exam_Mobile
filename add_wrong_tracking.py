import glob
import re
import os

def add_wrong_tracking():
    files = glob.glob('www/**/*.html', recursive=True)
    
    for file_path in files:
        if 'index.html' in file_path: continue
        
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Add CSS for .q-node.wrong
        if '.q-node.wrong' not in content:
            css_injection = """
        .q-node.wrong {
            background-color: #f8d7da;
            border-color: #f5c2c7;
            color: #842029;
        }
        """
            # Inject before .q-node.visited
            content = content.replace('.q-node.visited {', css_injection + '.q-node.visited {')

        # 2. Add Legend for "錯誤" (Wrong)
        # Look for the legend container
        legend_marker = '<span><span style="display:inline-block;width:10px;height:10px;background:#d1e7dd;border:1px solid #badbcc"></span> 已讀</span>'
        wrong_legend = '\n                <span><span style="display:inline-block;width:10px;height:10px;background:#f8d7da;border:1px solid #f5c2c7"></span> 錯誤</span>'
        
        if '錯誤</span>' not in content and legend_marker in content:
            content = content.replace(legend_marker, legend_marker + wrong_legend)

        # 3. JS State Initialization
        # We need to find where STORAGE_KEY is defined to add WRONG_KEY
        if 'const WRONG_KEY' not in content:
            # Extract safe name from existing STORAGE_KEY line to ensure consistency
            # Pattern: const STORAGE_KEY = 'something_visited_v1';
            match = re.search(r"const STORAGE_KEY = '(.+)_visited_v1';", content)
            if match:
                prefix = match.group(1)
                new_keys = f"const STORAGE_KEY = '{prefix}_visited_v1';\n    const WRONG_KEY = '{prefix}_wrong_v1';"
                content = content.replace(match.group(0), new_keys)
                
                # Also init the set
                content = content.replace('let visitedSet = new Set();', 'let visitedSet = new Set();\n    let wrongSet = new Set();')

        # 4. Update loadState
        if 'wrongSet = new Set(JSON.parse(savedWrong));' not in content:
            load_logic = """
        const savedWrong = localStorage.getItem(WRONG_KEY);
        if (savedWrong) {
            wrongSet = new Set(JSON.parse(savedWrong));
        }
            """
            # Insert before loading index
            content = content.replace('const savedIndex = localStorage.getItem(INDEX_KEY);', load_logic + 'const savedIndex = localStorage.getItem(INDEX_KEY);')

        # 5. Update saveState
        if 'localStorage.setItem(WRONG_KEY' not in content:
            save_logic = "localStorage.setItem(WRONG_KEY, JSON.stringify([...wrongSet]));"
            content = content.replace('localStorage.setItem(INDEX_KEY, currentIndex.toString());', 
                                      'localStorage.setItem(INDEX_KEY, currentIndex.toString());\n        ' + save_logic)

        # 6. Update resetProgress
        if 'localStorage.removeItem(WRONG_KEY);' not in content:
            reset_logic = "localStorage.removeItem(WRONG_KEY);"
            content = content.replace('localStorage.removeItem(INDEX_KEY);', 
                                      'localStorage.removeItem(INDEX_KEY);\n            ' + reset_logic)

        # 7. Update checkAnswer (Single & Multiple)
        # We look for the "incorrect" logic block
        # For Single choice: element.classList.add('incorrect');
        if 'wrongSet.add(qIdx);' not in content:
            # There are multiple places where 'incorrect' is added.
            # Strategy: Replace 'element.classList.add('incorrect');' with a block that also updates set and saves.
            
            # Note: We need to be careful not to break syntax.
            # The pattern is usually:
            # } else {
            #    element.classList.add('incorrect');
            
            # We can use a regex replacement to inject the logic safely.
            # Use a marker comment to avoid double injection if we run script again.
            
            # Replacement 1: Single choice incorrect
            # Pattern: element.classList.add('incorrect');
            # Context: checkAnswer function
            
            # We will search for specific blocks to be safer.
            
            # For Single/Multiple CheckAnswer:
            # We can inject at the top of the function or inside the logic?
            # Inside logic is better.
            
            # Let's search for "element.classList.add('incorrect');" and append logic.
            # But we only want to do this if it's NOT already there.
            # Since simple string replace does all occurrences, this covers both single and multiple logic paths in checkAnswer.
            
            # Wait, checkAnswer logic:
            # if (correctIndices.includes(optIdx)) { ... } else { element.classList.add('incorrect'); ... }
            
            # We want:
            # element.classList.add('incorrect');
            # wrongSet.add(qIdx);
            # saveState();
            
            replacement_code = """element.classList.add('incorrect');\n                wrongSet.add(qIdx);\n                saveState();"""
            
            # Careful with formatting/indentation, but JS is forgiving.
            # We replace "element.classList.add('incorrect');" with the block.
            # But avoid infinite replacement loop if we run twice.
            # We can check if 'wrongSet.add(qIdx)' is already present in the file globally (we did at start of block #7),
            # but specifically we want to know if it's near the classList add.
            
            # Let's do a regex substitution that asserts it's not followed by wrongSet.add
            
            content = re.sub(
                r"element\.classList\.add\('incorrect'\);(?!\s*wrongSet\.add)", 
                replacement_code, 
                content
            )

        # 8. Update checkSubAnswer
        # Similar logic. "element.classList.add('incorrect');" is used there too.
        # The previous replacement actually handles this too because it's the same line of code!
        # checkSubAnswer also has: element.classList.add('incorrect');
        # So the global replace in step 7 covers step 8 as well.
        # But wait, checkAnswer logic for multiple choice:
        # } else {
        #    element.classList.add('incorrect');
        #    element.classList.remove('correct');
        # }
        # My replacement above puts wrongSet.add right after .add('incorrect').
        # This is valid JS.
        
        # 9. Update updateUI
        # Logic:
        # if (i === currentIndex) node.classList.add('active');
        # else if (visitedSet.has(i)) node.classList.add('visited');
        #
        # We want to insert:
        # else if (wrongSet.has(i)) node.classList.add('wrong');
        #
        # Order matters: Active > Wrong > Visited? Or Active > Visited > Wrong?
        # User said "曾经選錯" (Ever wrong).
        # If I visited (Green) but it was wrong (Red), Red should probably take precedence to highlight attention needed.
        # But "Active" (Blue) must be top priority.
        # So: Active > Wrong > Visited.
        
        if 'else if (wrongSet.has(i)) node.classList.add(\'wrong\');' not in content:
            # We replace the visited check to insert wrong check before it.
            old_ui_logic = "else if (visitedSet.has(i)) node.classList.add('visited');"
            new_ui_logic = """else if (wrongSet.has(i)) node.classList.add('wrong');\n                else if (visitedSet.has(i)) node.classList.add('visited');"""
            
            content = content.replace(old_ui_logic, new_ui_logic)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    add_wrong_tracking()
