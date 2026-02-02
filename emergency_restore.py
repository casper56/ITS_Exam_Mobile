import os
import json
import glob
import re

def emergency_restore():
    # Base directory
    base_dir = 'www'
    
    # Common styles and scripts to inject
    zoom_css = """
        /* Zoom Controls */
        .zoom-controls {
            position: fixed;
            bottom: 90px;
            right: 20px;
            z-index: 1100;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .zoom-btn {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: #fff;
            color: #0d6efd;
            border: 1px solid #0d6efd;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            font-size: 1.5rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
            padding: 0;
            line-height: 1;
        }
        .zoom-btn:active {
            background: #0d6efd;
            color: #fff;
            transform: scale(0.95);
        }
    "

    zoom_html = """
    <!-- Zoom Controls V6 -->
    <div class="zoom-controls">
        <button class="zoom-btn" type="button" onclick="doZoom(2)">+</button>
        <button class="zoom-btn" type="button" onclick="doZoom(-2)">-</button>
    </div>
    ""

    zoom_js = """
    // --- ZOOM LOGIC V6 (Force Sync) ---
    var _zoomLevel = 16; // We decide this is the standard
    
    function doZoom(change) {
        _zoomLevel += change;
        
        // Safety bounds
        if (_zoomLevel < 10) _zoomLevel = 10;
        if (_zoomLevel > 40) _zoomLevel = 40;
        
        applyZoom();
    }
    
    function applyZoom() {
        // Apply to both root and body with !important
        document.documentElement.style.setProperty('font-size', _zoomLevel + 'px', 'important');
        document.body.style.setProperty('font-size', _zoomLevel + 'px', 'important');
    }
    
    // FORCE SYNC ON LOAD
    window.addEventListener('DOMContentLoaded', function() {
        applyZoom(); 
    });
    // ------------------------------------
    ""

    # Iterate through all subdirectories in www
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
            
        # Find JSON file in this subdir
        json_files = glob.glob(os.path.join(subdir_path, '*.json'))
        if not json_files:
            print(f"Skipping {subdir}: No JSON found.")
            continue
            
        json_path = json_files[0]
        html_filename = f"{subdir}.html" # e.g. ITS_Python.html
        html_path = os.path.join(subdir_path, html_filename)
        
        print(f"Restoring {html_path} from {json_path}...")
        
        # Load JSON data
        try:
            with open(json_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  Error reading JSON: {e}")
            continue
            
        # Try to find the generator script to use as template
        gen_script = os.path.join(subdir_path, 'json_to_html.py')
        if not os.path.exists(gen_script):
            # Fallback: try to find ANY json_to_html.py to use as template
            fallback = glob.glob(os.path.join(base_dir, '**', 'json_to_html.py'), recursive=True)
            if fallback:
                gen_script = fallback[0]
            else:
                print("  No generator script found.")
                continue
        
        # Read template
        with open(gen_script, 'r', encoding='utf-8') as f:
            template_code = f.read()
            
        # Extract HTML template
        match = re.search(r'html_content = f"""(.*?)"""', template_code, re.DOTALL)
        if not match:
            print("  Template extraction failed.")
            continue
            
        html_template = match.group(1)
        
        # Prepare variables
        display_title = subdir.replace('_', ' ')
        json_str = json.dumps(data, ensure_ascii=False)
        safe_name = subdir.lower().replace(' ', '_').replace('-', '_')
        storage_key = f"{safe_name}_visited_v1"
        index_key = f"{safe_name}_current_idx_v1"
        
        # Inject Zoom features into the template BEFORE filling data
        # Inject CSS
        html_template = html_template.replace('</style>', zoom_css + '\n    </style>')
        
        # Inject HTML Buttons
        html_template = html_template.replace('<!-- Scripts -->', zoom_html + '\n<!-- Scripts -->')
        
        # Inject JS Logic
        html_template = html_template.replace('// Init', zoom_js + '\n    // Init')
        
        # Fix Viewport
        html_template = html_template.replace('content="width=device-width, initial-scale=1.0"', 
                                              'content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0, user-scalable=yes"')

        # Fill template
        # We need to manually replace the f-string placeholders because we are not executing the python code
        # The template has {var} which we need to replace.
        # Note: The template source code has {{ for literal { in f-strings.
        # We need to be careful.
        
        final_html = html_template
        final_html = final_html.replace('{display_title}', display_title)
        final_html = final_html.replace('{json_str}', json_str)
        final_html = final_html.replace('{storage_key}', storage_key)
        final_html = final_html.replace('{index_key}', index_key)
        final_html = final_html.replace('{len(data)}', str(len(data)))
        
        # Write the restored HTML file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write("<!DOCTYPE html>\n<html lang=\"zh-TW\">
" + final_html)
            
        print(f"  Successfully restored {html_path}")

    print("Restoration complete.")

if __name__ == "__main__":
    emergency_restore()
