import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement_html = '''<div class="header-container" style="width: 100%; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; position: relative;">
        <div class="dropdown" style="position: absolute; left: 0;">
            <button class="icon-btn" onclick="toggleMenu(event)" style="background: none; border: none; font-size: 28px; cursor: pointer; transition: transform 0.2s;">💡</button>
            <div id="dropdown-menu" class="dropdown-content" style="display: none; position: absolute; background-color: white; min-width: 280px; box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2); z-index: 10; border-radius: 8px; top: 40px; left: 0; text-align: left;">
                <a href="index.html" style="color: black; padding: 12px 16px; text-decoration: none; display: block; font-weight: bold; border-bottom: 1px solid #eee;">Từ trái nghĩa (Tính từ)</a>
                <a href="verbs.html" style="color: black; padding: 12px 16px; text-decoration: none; display: block; font-weight: bold;">Tự/Tha động từ (自動詞他動詞練習)</a>
            </div>
        </div>
        <h2 style="margin: 0;">Từ Trái Nghĩa (Tính từ)</h2>
    </div>'''

html = re.sub(r'<h2>Học Từ Trái Nghĩa \(Tính từ\)</h2>', replacement_html, html)

js_addition = '''
    function toggleMenu(event) {
        event.stopPropagation();
        var menu = document.getElementById("dropdown-menu");
        if (menu.style.display === "block") {
            menu.style.display = "none";
        } else {
            menu.style.display = "block";
        }
    }
    
    window.onclick = function(event) {
        if (!event.target.matches('.icon-btn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            for (var i = 0; i < dropdowns.length; i++) {
                if (dropdowns[i].style.display === "block") {
                    dropdowns[i].style.display = "none";
                }
            }
        }
    }
'''

html = html.replace('let hasAnswered = false;', 'let hasAnswered = false;\n' + js_addition)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Patched index.html directly')
