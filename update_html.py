import json

# Read the extracted json
with open('flashcards.json', 'r', encoding='utf-8') as f:
    flashcards_json_str = f.read()

# We will inject flashcards_json_str into the new HTML

html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Từ Trái Nghĩa Tiếng Nhật</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            user-select: none;
        }}
        .app-container {{
            width: 100%;
            max-width: 500px;
            padding: 20px;
            text-align: center;
            background: #fff;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        /* Flashcard Mode Styles */
        .flashcard-container {{
            perspective: 1000px;
            margin: 20px 0;
            height: 350px;
            cursor: pointer;
        }}
        .flashcard {{
            width: 100%;
            height: 100%;
            position: relative;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border-radius: 15px;
            background-color: white;
        }}
        .flashcard.is-flipped {{
            transform: rotateY(180deg);
        }}
        .card-face {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 15px;
            padding: 20px;
            box-sizing: border-box;
        }}
        .card-back {{
            transform: rotateY(180deg);
            background-color: #fdfbf7;
            border: 2px solid #e0dcd3;
        }}
        .lesson-tag {{
            position: absolute;
            top: 15px;
            left: 15px;
            background-color: #4CAF50;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }}
        .lesson-tag.new-word {{
            background-color: #FF9800;
        }}
        .word-kana {{
            font-size: 48px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .word-kanji {{
            font-size: 24px;
            color: #666;
            margin-bottom: 15px;
        }}
        .word-vn {{
            font-size: 22px;
            color: #1976D2;
            font-weight: bold;
        }}
        .no-antonym {{
            font-size: 32px;
            color: #9e9e9e;
            font-weight: bold;
        }}
        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
        }}
        .nav-btn {{
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        .nav-btn:hover {{
            background-color: #1976D2;
        }}
        .nav-btn:disabled {{
            background-color: #ccc;
            cursor: not-allowed;
        }}
        .progress {{
            font-size: 18px;
            color: #555;
            font-weight: bold;
        }}
        .mode-switch-btn {{
            background-color: #9C27B0;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 10px;
            transition: background 0.3s;
        }}
        .mode-switch-btn:hover {{
            background-color: #7B1FA2;
        }}

        /* Quiz Mode Styles */
        #quiz-mode {{
            display: none;
        }}
        .small-card {{
            width: 100%;
            height: 180px;
            background-color: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            border: 2px solid #e0e0e0;
        }}
        .small-card .word-kana {{
            font-size: 36px;
            margin-bottom: 5px;
        }}
        .small-card .word-kanji {{
            font-size: 20px;
            margin-bottom: 5px;
        }}
        .small-card .word-vn {{
            font-size: 18px;
        }}
        .quiz-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .quiz-controls .nav-btn {{
            padding: 10px 20px;
            font-size: 18px;
        }}
        .quit-btn {{
            background-color: #f44336;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
        }}
        .quit-btn:hover {{
            background-color: #d32f2f;
        }}
        .choices-container {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .choice-btn {{
            background-color: #fff;
            border: 2px solid #2196F3;
            color: #333;
            padding: 15px;
            font-size: 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: bold;
        }}
        .choice-btn:hover {{
            background-color: #e3f2fd;
        }}
        .choice-btn.correct {{
            background-color: #e8f5e9; color: #333; border-color: #81c784;
        }}
        .choice-btn.wrong {{
            background-color: #ffebee; color: #333; border-color: #e57373;
        }}
        .choice-btn:disabled {{
            cursor: not-allowed;
        }}
        #quiz-feedback {{
            margin-top: 15px;
            font-size: 18px;
            font-weight: bold;
            min-height: 27px;
        }}
    </style>
</head>
<body>

<div class="app-container">
    <h2>Học Từ Trái Nghĩa (Tính từ)</h2>
    
    <!-- FLASHCARD MODE -->
    <div id="flashcard-mode">
        <button class="mode-switch-btn" onclick="startQuiz()">Trắc nghiệm từ trái nghĩa (3択クイズ)</button>
        <div class="flashcard-container" onclick="flipCard()">
            <div class="flashcard" id="flashcard">
                <div class="card-face card-front">
                    <div class="lesson-tag" id="front-lesson"></div>
                    <div class="word-kana" id="front-kana"></div>
                    <div class="word-kanji" id="front-kanji"></div>
                    <div class="word-vn" id="front-vn"></div>
                </div>
                <div class="card-face card-back">
                    <div class="lesson-tag" id="back-lesson"></div>
                    <div id="back-content">
                        <div class="word-kana" id="back-kana"></div>
                        <div class="word-kanji" id="back-kanji"></div>
                        <div class="word-vn" id="back-vn"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="controls">
            <button class="nav-btn" onclick="prevCard()" id="btn-prev">&lt;&lt;</button>
            <div class="progress"><span id="current-idx">1</span> / <span id="total-cards"></span></div>
            <button class="nav-btn" onclick="nextCard()" id="btn-next">&gt;&gt;</button>
        </div>
    </div>

    <!-- QUIZ MODE -->
    <div id="quiz-mode">
        <div class="small-card">
            <div class="word-kana" id="quiz-kana"></div>
            <div class="word-kanji" id="quiz-kanji"></div>
            <div class="word-vn" id="quiz-vn"></div>
        </div>
        
        <div class="quiz-controls">
            <button class="nav-btn" onclick="prevQuiz()" id="quiz-btn-prev">&lt;&lt;</button>
            <button class="quit-btn" onclick="quitQuiz()">やめる (Thoát)</button>
            <button class="nav-btn" onclick="nextQuiz()" id="quiz-btn-next">&gt;&gt;</button>
        </div>
        
        <div class="choices-container" id="choices-container">
            <!-- Choices will be injected here -->
        </div>
        
        <div id="quiz-feedback"></div>
        <div class="progress" style="margin-top: 10px;"><span id="quiz-current-idx">1</span> / <span id="quiz-total-cards"></span></div>
    </div>
</div>

<script>
    const flashcards = {flashcards_json_str};
    let currentIndex = 0;

    // Quiz State
    let quizCards = [];
    let currentQuizIndex = 0;
    let quizChoices = [];
    let hasAnswered = false;

    // --- FLASHCARD MODE LOGIC ---
    function renderCard() {{
        const card = flashcards[currentIndex];
        
        document.getElementById('front-lesson').textContent = "Bài " + card.front.lesson.replace('Lesson ', '');
        document.getElementById('front-kana').textContent = card.front.kana;
        document.getElementById('front-kanji').textContent = card.front.kanji || '';
        document.getElementById('front-vn').textContent = card.front.vn;
        
        const backContent = document.getElementById('back-content');
        const backLesson = document.getElementById('back-lesson');
        
        if (!card.back) {{
            backLesson.style.display = 'none';
            backContent.innerHTML = '<div class="no-antonym">Không có từ trái nghĩa<br>(対義語無し)</div>';
        }} else {{
            backLesson.style.display = 'block';
            if (card.back.is_new) {{
                backLesson.textContent = 'Chưa học (未習語)';
                backLesson.className = 'lesson-tag new-word';
            }} else {{
                backLesson.textContent = "Bài " + card.back.lesson;
                backLesson.className = 'lesson-tag';
            }}
            backContent.innerHTML = `
                <div class="word-kana">${{card.back.kana}}</div>
                <div class="word-kanji">${{card.back.kanji || ''}}</div>
                <div class="word-vn">${{card.back.vn}}</div>
            `;
        }}
        
        document.getElementById('current-idx').textContent = currentIndex + 1;
        document.getElementById('total-cards').textContent = flashcards.length;
        document.getElementById('btn-prev').disabled = currentIndex === 0;
        document.getElementById('btn-next').disabled = currentIndex === flashcards.length - 1;
        
        document.getElementById('flashcard').classList.remove('is-flipped');
    }}

    function flipCard() {{
        document.getElementById('flashcard').classList.toggle('is-flipped');
    }}

    function nextCard() {{
        if (currentIndex < flashcards.length - 1) {{
            currentIndex++;
            renderCard();
        }}
    }}

    function prevCard() {{
        if (currentIndex > 0) {{
            currentIndex--;
            renderCard();
        }}
    }}

    // --- QUIZ MODE LOGIC ---
    function startQuiz() {{
        // Filter cards that have an antonym
        quizCards = flashcards.filter(c => c.back !== null);
        
        // Shuffle the quiz cards if desired, but here we just start from 0 for predictability or shuffle them
        // Let's shuffle quiz cards so it's a real quiz
        quizCards = quizCards.sort(() => Math.random() - 0.5);
        
        if (quizCards.length === 0) return; // Edge case
        
        currentQuizIndex = 0;
        document.getElementById('flashcard-mode').style.display = 'none';
        document.getElementById('quiz-mode').style.display = 'block';
        
        renderQuiz();
    }}

    function quitQuiz() {{
        document.getElementById('quiz-mode').style.display = 'none';
        document.getElementById('flashcard-mode').style.display = 'block';
        // Re-render flashcard mode to ensure it's in a clean state
        renderCard();
    }}

    function getDistractors(correctBack, count) {{
        // Get all unique back cards that are NOT the correct one
        const allBacks = flashcards.filter(c => c.back !== null && c.back.kana !== correctBack.kana).map(c => c.back);
        
        // Remove duplicates based on kana
        const uniqueBacks = [];
        const seen = new Set();
        for (let b of allBacks) {{
            if (!seen.has(b.kana)) {{
                seen.add(b.kana);
                uniqueBacks.push(b);
            }}
        }}
        
        // Shuffle and pick
        const shuffled = uniqueBacks.sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    }}

    function renderQuiz() {{
        hasAnswered = false;
        const card = quizCards[currentQuizIndex];
        
        // Render small headword card
        document.getElementById('quiz-kana').textContent = card.front.kana;
        document.getElementById('quiz-kanji').textContent = card.front.kanji || '';
        document.getElementById('quiz-vn').textContent = card.front.vn;
        
        // Prepare choices
        const correctChoice = card.back;
        const distractors = getDistractors(correctChoice, 2);
        
        quizChoices = [correctChoice, ...distractors];
        quizChoices.sort(() => Math.random() - 0.5); // Shuffle choices
        
        // Render choices
        const container = document.getElementById('choices-container');
        container.innerHTML = '';
        
        quizChoices.forEach((choice, idx) => {{
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            
            // Display Kana and optionally Kanji
            let text = choice.kana;
            if (choice.kanji) text += ` (${{choice.kanji}})`;
            
            btn.textContent = text;
            btn.onclick = () => selectChoice(idx, choice.kana === correctChoice.kana);
            container.appendChild(btn);
        }});
        
        document.getElementById('quiz-feedback').textContent = '';
        document.getElementById('quiz-feedback').style.color = '#333';
        
        // Update navigation
        document.getElementById('quiz-btn-prev').disabled = currentQuizIndex === 0;
        document.getElementById('quiz-btn-next').disabled = currentQuizIndex === quizCards.length - 1;
        document.getElementById('quiz-current-idx').textContent = currentQuizIndex + 1;
        document.getElementById('quiz-total-cards').textContent = quizCards.length;
    }}

    function selectChoice(selectedIndex, isCorrect) {{
        if (hasAnswered) return;
        hasAnswered = true;
        
        const buttons = document.getElementById('choices-container').children;
        const card = quizCards[currentQuizIndex];
        
        for (let i = 0; i < buttons.length; i++) {{
            buttons[i].disabled = true; // Disable all
            
            // Highlight the correct one regardless of choice
            if (quizChoices[i].kana === card.back.kana) {{
                buttons[i].classList.add('correct');
            }}
        }}
        
        const feedback = document.getElementById('quiz-feedback');
        if (isCorrect) {{
            feedback.textContent = '⭕ Chính xác! (正解)';
            feedback.style.color = '#4CAF50';
        }} else {{
            buttons[selectedIndex].classList.add('wrong');
            feedback.textContent = '❌ Sai rồi! (不正解)';
            feedback.style.color = '#f44336';
        }}
    }}

    function nextQuiz() {{
        if (currentQuizIndex < quizCards.length - 1) {{
            currentQuizIndex++;
            renderQuiz();
        }}
    }}

    function prevQuiz() {{
        if (currentQuizIndex > 0) {{
            currentQuizIndex--;
            renderQuiz();
        }}
    }}

    // Initialize flashcard mode
    renderCard();
</script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("index.html updated successfully with quiz mode.")

