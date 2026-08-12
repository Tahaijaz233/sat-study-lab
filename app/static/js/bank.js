document.addEventListener('DOMContentLoaded', () => {
    let questions = [];
    let currentIndex = 0;

    // DOM Elements
    const searchInput = document.getElementById('searchInput');
    const sectionFilter = document.getElementById('sectionFilter');
    const subtopicFilter = document.getElementById('subtopicFilter');
    const difficultyFilter = document.getElementById('difficultyFilter');
    
    const cardBadgeSection = document.getElementById('cardBadgeSection');
    const cardBadgeDifficulty = document.getElementById('cardBadgeDifficulty');
    const cardBadgeTopic = document.getElementById('cardBadgeTopic');
    const cardBadgeSubtopic = document.getElementById('cardBadgeSubtopic');
    const cardCounter = document.getElementById('cardCounter');
    const cardPassage = document.getElementById('cardPassage');
    const cardPrompt = document.getElementById('cardPrompt');
    const cardChoicesContainer = document.getElementById('cardChoicesContainer');
    const cardExplanationContainer = document.getElementById('cardExplanationContainer');
    const cardExplanationText = document.getElementById('cardExplanationText');

    const btnCardPrev = document.getElementById('btnCardPrev');
    const btnCardNext = document.getElementById('btnCardNext');
    const jumpDropdown = document.getElementById('jumpDropdown');

    function formatText(text) {
        if (!text || text === "null") return "";
        let str = String(text);
        
        // Clean unescaped unicode escapes
        str = str.replace(/\\u2013/g, "–")
                 .replace(/\\u2014/g, "—")
                 .replace(/\\u2019/g, "'")
                 .replace(/\\u201c/g, '"')
                 .replace(/\\u201d/g, '"');

        // Bold & Italic markdown formatting
        str = str.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        str = str.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
        
        // Blank line box formatting
        str = str.replace(/___+/g, '<span class="inline-block px-3 py-0.5 border-b-2 border-indigo-500 font-mono font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50/50 dark:bg-indigo-950/50 rounded-t">______</span>');
        
        return str;
    }

    async function loadQuestions() {
        const q = searchInput ? searchInput.value.trim() : '';
        const sec = sectionFilter ? sectionFilter.value : '';
        const diff = difficultyFilter ? difficultyFilter.value : '';
        const sub = subtopicFilter ? subtopicFilter.value : '';

        const url = `/api/questions?q=${encodeURIComponent(q)}&section=${encodeURIComponent(sec)}&difficulty=${encodeURIComponent(diff)}&per_page=3000`;

        try {
            const res = await fetch(url);
            const data = await res.json();
            let rawList = data.questions || [];

            // Filter subtopic client-side if selected
            if (sub) {
                rawList = rawList.filter(item => item.topic === sub || item.subtopic === sub);
            }

            questions = rawList;
            currentIndex = 0;

            populateSubtopicDropdown(data.questions || []);
            populateJumpDropdown();
            renderCard(0);
        } catch (err) {
            console.error("Failed to load questions:", err);
        }
    }

    function populateSubtopicDropdown(allQuestions) {
        if (!subtopicFilter) return;
        const currentSelected = subtopicFilter.value;
        const topicsSet = new Set();
        
        allQuestions.forEach(q => {
            if (q.topic) topicsSet.add(q.topic);
            if (q.subtopic && q.subtopic !== "General SAT Concept") topicsSet.add(q.subtopic);
        });

        subtopicFilter.innerHTML = '<option value="">All Topics & Subtopics</option>';
        Array.from(topicsSet).sort().forEach(t => {
            const opt = document.createElement('option');
            opt.value = t;
            opt.textContent = t;
            if (t === currentSelected) opt.selected = true;
            subtopicFilter.appendChild(opt);
        });
    }

    function populateJumpDropdown() {
        if (!jumpDropdown) return;
        jumpDropdown.innerHTML = '';
        if (questions.length === 0) {
            jumpDropdown.innerHTML = '<option>No cards found</option>';
            return;
        }

        const step = questions.length > 400 ? Math.ceil(questions.length / 250) : 1;
        questions.forEach((q, idx) => {
            if (idx % step === 0 || idx === questions.length - 1) {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.textContent = `Card ${idx + 1}: ${q.section} (${q.topic})`;
                jumpDropdown.appendChild(opt);
            }
        });
    }

    function renderCard(idx) {
        if (questions.length === 0) {
            if (cardCounter) cardCounter.textContent = "Card 0 of 0";
            if (cardBadgeSection) cardBadgeSection.textContent = "N/A";
            if (cardBadgeDifficulty) cardBadgeDifficulty.textContent = "N/A";
            if (cardBadgeTopic) cardBadgeTopic.textContent = "No data";
            if (cardBadgeSubtopic) cardBadgeSubtopic.classList.add('hidden');
            if (cardPassage) cardPassage.classList.add('hidden');
            if (cardPrompt) cardPrompt.innerHTML = "<p class='text-gray-500 text-center py-8'>No questions found matching your filter criteria.</p>";
            if (cardChoicesContainer) cardChoicesContainer.innerHTML = "";
            if (cardExplanationContainer) cardExplanationContainer.classList.add('hidden');
            if (btnCardPrev) btnCardPrev.disabled = true;
            if (btnCardNext) btnCardNext.disabled = true;
            return;
        }

        if (idx < 0) idx = 0;
        if (idx >= questions.length) idx = questions.length - 1;
        currentIndex = idx;

        const q = questions[idx];

        if (cardCounter) cardCounter.textContent = `Card ${idx + 1} of ${questions.length}`;
        if (cardBadgeSection) cardBadgeSection.textContent = q.section;
        if (cardBadgeDifficulty) cardBadgeDifficulty.textContent = q.difficulty;
        if (cardBadgeTopic) cardBadgeTopic.textContent = q.topic;
        
        if (cardBadgeSubtopic) {
            if (q.subtopic && q.subtopic !== 'General SAT Concept') {
                cardBadgeSubtopic.classList.remove('hidden');
                cardBadgeSubtopic.textContent = q.subtopic;
            } else {
                cardBadgeSubtopic.classList.add('hidden');
            }
        }

        // Passage
        if (q.passage_content) {
            cardPassage.classList.remove('hidden');
            cardPassage.innerHTML = `
                <h4 class="font-bold mb-2 text-indigo-600 dark:text-indigo-400">${q.passage_title || 'Passage'}</h4>
                <div>${formatText(q.passage_content)}</div>
            `;
        } else {
            cardPassage.classList.add('hidden');
        }

        // Prompt
        cardPrompt.innerHTML = `<p>${formatText(q.prompt)}</p>`;

        // Choices
        cardChoicesContainer.innerHTML = '';
        cardExplanationContainer.classList.add('hidden');

        if (q.question_type === 'Student-Produced Response' || !q.choices || q.choices.length === 0) {
            cardChoicesContainer.innerHTML = `
                <div class="space-y-3">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Student-Produced Answer:</label>
                    <div class="flex gap-3">
                        <input type="text" id="checkSprInput" class="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-300 dark:border-gray-600 rounded-xl p-3 text-gray-900 dark:text-white font-mono" placeholder="Type answer...">
                        <button id="btnCheckSpr" class="px-5 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-bold">Check Answer</button>
                    </div>
                </div>
            `;
            const checkBtn = document.getElementById('btnCheckSpr');
            checkBtn.addEventListener('click', () => {
                const val = document.getElementById('checkSprInput').value.trim();
                const correctVal = (q.correct_answer_value || '').trim();
                if (val === correctVal) {
                    window.showToast("Correct Answer!", "success");
                } else {
                    window.showToast(`Incorrect. Correct Answer: ${correctVal}`, "error");
                }
                showExplanation(q.answer_explanation);
            });
        } else {
            q.choices.forEach(c => {
                const btn = document.createElement('button');
                btn.className = "w-full text-left p-4 rounded-xl border-2 border-gray-200 dark:border-gray-700 hover:border-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-all font-medium";
                btn.innerHTML = `<strong>${c.choice_letter})</strong> ${formatText(c.content)}`;
                
                btn.addEventListener('click', () => {
                    // Check choice correctness
                    const allBtns = cardChoicesContainer.querySelectorAll('button');
                    allBtns.forEach(b => b.classList.remove('border-indigo-600', 'border-emerald-500', 'bg-emerald-50', 'border-red-500', 'bg-red-50'));
                    
                    if (c.is_correct || c.choice_letter === q.correct_answer_value) {
                        btn.className = "w-full text-left p-4 rounded-xl border-2 border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-900 dark:text-emerald-100 font-medium";
                        window.showToast("Correct!", "success");
                    } else {
                        btn.className = "w-full text-left p-4 rounded-xl border-2 border-red-500 bg-red-50 dark:bg-red-900/20 text-red-900 dark:text-red-100 font-medium";
                        window.showToast(`Incorrect. Correct Answer: ${q.correct_answer_value}`, "error");
                    }
                    showExplanation(q.answer_explanation);
                });
                cardChoicesContainer.appendChild(btn);
            });
        }

        // Nav states
        btnCardPrev.disabled = (idx === 0);
        btnCardNext.disabled = (idx === questions.length - 1);
        if (jumpDropdown) jumpDropdown.value = idx;

        // KaTeX Math & Icons
        if (window.renderMathInElement) {
            window.renderMathInElement(document.body, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false
            });
        }
        if (window.lucide) window.lucide.createIcons();
    }

    function showExplanation(exp) {
        if (!exp) return;
        cardExplanationText.innerHTML = `<p>${formatText(exp)}</p>`;
        cardExplanationContainer.classList.remove('hidden');
        if (window.renderMathInElement) {
            window.renderMathInElement(cardExplanationText, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false
            });
        }
    }

    // Event Listeners
    if (searchInput) searchInput.addEventListener('input', debounce(loadQuestions, 300));
    if (sectionFilter) sectionFilter.addEventListener('change', loadQuestions);
    if (subtopicFilter) subtopicFilter.addEventListener('change', loadQuestions);
    if (difficultyFilter) difficultyFilter.addEventListener('change', loadQuestions);

    if (btnCardPrev) btnCardPrev.addEventListener('click', () => renderCard(currentIndex - 1));
    if (btnCardNext) btnCardNext.addEventListener('click', () => renderCard(currentIndex + 1));
    
    if (jumpDropdown) {
        jumpDropdown.addEventListener('change', (e) => {
            const val = parseInt(e.target.value, 10);
            if (!isNaN(val)) renderCard(val);
        });
    }

    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Initial Load
    loadQuestions();
});
