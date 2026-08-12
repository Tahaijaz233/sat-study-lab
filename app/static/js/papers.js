document.addEventListener('DOMContentLoaded', () => {
    let currentSessionId = null;
    let questions = [];
    let currentIndex = 0;
    let userAnswers = {}; // question_id -> { selected_choice_id, student_produced_answer, bookmarked }
    let timerInterval = null;
    let timeLeftSeconds = 0;
    let isTimedSession = false;

    // DOM Elements
    const setupModal = document.getElementById('setupModal');
    const scoreModal = document.getElementById('scoreModal');
    const btnOpenSetup = document.getElementById('btnOpenSetup');
    const btnCancelModal = document.getElementById('btnCancelModal');
    const btnStartModal = document.getElementById('btnStartModal');
    const btnFinish = document.getElementById('btnFinish');
    const btnPrev = document.getElementById('btnPrev');
    const btnNext = document.getElementById('btnNext');
    const btnFlag = document.getElementById('btnFlag');
    const flagText = document.getElementById('flagText');

    const sessionTitle = document.getElementById('sessionTitle');
    const sectionBadge = document.getElementById('sectionBadge');
    const timerDisplay = document.getElementById('timerDisplay');
    const currentQNum = document.getElementById('currentQNum');
    const stimulusContent = document.getElementById('stimulusContent');
    const questionContent = document.getElementById('questionContent');
    const optionsContainer = document.getElementById('optionsContainer');
    const questionGrid = document.getElementById('questionGrid');
    
    // Calculator elements
    const calculatorBtn = document.getElementById('calculator-btn');
    const desmosModal = document.getElementById('desmos-modal');
    const closeDesmosBtn = document.getElementById('close-desmos-btn');
    const desmosHeader = document.getElementById('desmos-header');
    const calculatorContainer = document.getElementById('calculator-container');
    let desmosCalc = null;

    function formatText(text) {
        if (!text || text === "null") return "";
        let str = String(text);
        
        str = str.replace(/\\u2013/g, "–")
                 .replace(/\\u2014/g, "—")
                 .replace(/\\u2019/g, "'")
                 .replace(/\\u201c/g, '"')
                 .replace(/\\u201d/g, '"');

        str = str.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        str = str.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
        str = str.replace(/___+/g, '<span class="inline-block px-3 py-0.5 border-b-2 border-indigo-500 font-mono font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50/50 dark:bg-indigo-950/50 rounded-t">______</span>');
        
        return str;
    }

    if (btnOpenSetup) {
        btnOpenSetup.addEventListener('click', () => {
            setupModal.classList.remove('hidden');
        });
    }
    
    // Auto-start session if session_id is in URL
    const urlParams = new URLSearchParams(window.location.search);
    const existingSessionId = urlParams.get('session_id');
    if (existingSessionId) {
        if (setupModal) setupModal.classList.add('hidden');
        currentSessionId = existingSessionId;
        fetchNextModule();
    }
    if (btnCancelModal) {
        btnCancelModal.addEventListener('click', () => {
            setupModal.classList.add('hidden');
        });
    }

    if (btnStartModal) {
        btnStartModal.addEventListener('click', async () => {
            const sectionSelect = document.getElementById('sectionSelect');
            const section = sectionSelect ? sectionSelect.value : 'Reading & Writing';
            isTimedSession = document.getElementById('timedMode').checked;
            
            btnStartModal.disabled = true;
            btnStartModal.textContent = "Starting...";

            try {
                // 1. Create session
                const res = await fetch('/api/papers/sessions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: `${section} Session`,
                        section: section,
                        session_type: 'practice'
                    })
                });
                
                const data = await res.json();
                currentSessionId = data.session_id;

                setupModal.classList.add('hidden');
                btnStartModal.disabled = false;
                btnStartModal.textContent = "Start Session";

                if (sessionTitle) sessionTitle.textContent = data.title;
                userAnswers = {};

                // 2. Fetch first module
                await fetchNextModule();

            } catch (err) {
                console.error(err);
                window.showToast("Failed to start session.", "error");
                btnStartModal.disabled = false;
                btnStartModal.textContent = "Start Session";
            }
        });
    }

    async function fetchNextModule() {
        if (!currentSessionId) return;
        
        try {
            const res = await fetch(`/api/papers/sessions/${currentSessionId}/next_module`, { method: 'POST' });
            const data = await res.json();
            
            if (data.completed) {
                showScoreReport(data);
                return;
            }
            
            questions = data.questions || [];
            if (questions.length === 0) {
                window.showToast("Error loading questions for next module.", "error");
                return;
            }
            
            currentIndex = 0;
            if (sectionBadge) sectionBadge.textContent = data.module_name;
            
            if (isTimedSession) {
                timeLeftSeconds = data.time_limit_seconds || 1800;
                startTimer();
            } else {
                if (timerDisplay) timerDisplay.textContent = "Untimed";
            }
            
            renderQuestion(0);
            renderQuestionGrid();
            window.showToast(`${data.module_name} started.`, "success");
            
            // Show or hide Desmos calculator button based on module name
            if (calculatorBtn) {
                if (data.module_name.includes('Math')) {
                    calculatorBtn.classList.remove('hidden');
                    initDesmos();
                } else {
                    calculatorBtn.classList.add('hidden');
                    if (desmosModal) desmosModal.classList.add('hidden');
                }
            }
            
        } catch (err) {
            console.error(err);
            window.showToast("Failed to load module.", "error");
        }
    }

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            if (timeLeftSeconds <= 0) {
                clearInterval(timerInterval);
                window.showToast("Time's up! Module finished.", "warning");
                fetchNextModule();
            } else {
                timeLeftSeconds--;
                const m = Math.floor(timeLeftSeconds / 60).toString().padStart(2, '0');
                const s = (timeLeftSeconds % 60).toString().padStart(2, '0');
                if (timerDisplay) timerDisplay.textContent = `${m}:${s}`;
            }
        }, 1000);
    }

    function renderQuestion(idx) {
        if (idx < 0 || idx >= questions.length) return;
        currentIndex = idx;

        const q = questions[idx];
        if (currentQNum) currentQNum.textContent = idx + 1;

        if (q.passage_content) {
            stimulusContent.innerHTML = `
                <h3 class="font-bold text-lg mb-2 text-indigo-600 dark:text-indigo-400">${q.passage_title || 'Passage'}</h3>
                <div>${formatText(q.passage_content)}</div>
            `;
        } else {
            stimulusContent.innerHTML = `
                <div class="text-center py-12 text-gray-400">
                    <p class="text-sm">This question has no associated reading passage.</p>
                </div>
            `;
        }

        questionContent.innerHTML = `<p>${formatText(q.prompt)}</p>`;
        optionsContainer.innerHTML = '';
        
        const savedAnswer = userAnswers[q.id] || {};

        if (q.question_type === 'Student-Produced Response' || !q.choices || q.choices.length === 0) {
            optionsContainer.innerHTML = `
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Enter your numerical or fraction answer:</label>
                    <input type="text" id="sprInput" value="${savedAnswer.student_produced_answer || ''}" 
                        class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-300 dark:border-gray-600 rounded-xl p-3 text-gray-900 dark:text-white font-mono text-lg" 
                        placeholder="e.g. 5 or 3/4">
                </div>
            `;
            const input = document.getElementById('sprInput');
            input.addEventListener('input', (e) => {
                saveAnswer(q.id, null, e.target.value);
            });
        } else {
            q.choices.forEach(c => {
                const isSelected = savedAnswer.selected_choice_id === c.id;
                const btn = document.createElement('button');
                btn.className = `w-full text-left p-4 rounded-xl border-2 font-medium transition-all flex items-center justify-between ${
                    isSelected 
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-900 dark:text-indigo-100' 
                        : 'border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600'
                }`;
                btn.innerHTML = `
                    <span><strong>${c.choice_letter})</strong> ${formatText(c.content)}</span>
                    ${isSelected ? '<i data-lucide="check-circle" class="w-5 h-5 text-indigo-600"></i>' : ''}
                `;
                btn.addEventListener('click', () => {
                    saveAnswer(q.id, c.id, null);
                    renderQuestion(currentIndex);
                });
                optionsContainer.appendChild(btn);
            });
        }

        if (savedAnswer.bookmarked) {
            if (btnFlag) btnFlag.classList.add('text-amber-500');
            if (flagText) flagText.textContent = "Bookmarked";
        } else {
            if (btnFlag) btnFlag.classList.remove('text-amber-500');
            if (flagText) flagText.textContent = "Mark for Review";
        }

        if (btnPrev) btnPrev.disabled = (idx === 0);
        if (btnNext) btnNext.textContent = (idx === questions.length - 1) ? "Finish Section" : "Next";

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

        renderQuestionGrid();
    }

    function saveAnswer(questionId, selectedChoiceId, sprAnswer) {
        if (!userAnswers[questionId]) {
            userAnswers[questionId] = {};
        }
        if (selectedChoiceId !== null) userAnswers[questionId].selected_choice_id = selectedChoiceId;
        if (sprAnswer !== null) userAnswers[questionId].student_produced_answer = sprAnswer;

        if (currentSessionId) {
            fetch(`/api/papers/sessions/${currentSessionId}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: questionId,
                    selected_choice_id: userAnswers[questionId].selected_choice_id,
                    student_produced_answer: userAnswers[questionId].student_produced_answer,
                    time_spent_seconds: 10,
                    bookmarked: userAnswers[questionId].bookmarked || false
                })
            }).catch(console.error);
        }
    }

    function renderQuestionGrid() {
        if (!questionGrid) return;
        questionGrid.innerHTML = '';
        questions.forEach((q, idx) => {
            const isCurrent = idx === currentIndex;
            const isAnswered = userAnswers[q.id] && (userAnswers[q.id].selected_choice_id || userAnswers[q.id].student_produced_answer);
            const isFlagged = userAnswers[q.id] && userAnswers[q.id].bookmarked;

            const bubble = document.createElement('button');
            bubble.className = `w-9 h-9 rounded-lg text-xs font-bold transition-all border ${
                isCurrent 
                    ? 'ring-2 ring-indigo-500 ring-offset-2 bg-indigo-600 text-white' 
                    : isAnswered 
                    ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300 border-emerald-300' 
                    : isFlagged
                    ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 border-amber-300'
                    : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600'
            }`;
            bubble.textContent = idx + 1;
            bubble.addEventListener('click', () => renderQuestion(idx));
            questionGrid.appendChild(bubble);
        });
    }

    if (btnFlag) {
        btnFlag.addEventListener('click', () => {
            if (questions.length === 0) return;
            const qId = questions[currentIndex].id;
            if (!userAnswers[qId]) userAnswers[qId] = {};
            userAnswers[qId].bookmarked = !userAnswers[qId].bookmarked;
            
            // Re-save immediately so backend knows about bookmark
            saveAnswer(qId, userAnswers[qId].selected_choice_id, userAnswers[qId].student_produced_answer);
            renderQuestion(currentIndex);
        });
    }

    if (btnPrev) {
        btnPrev.addEventListener('click', () => {
            if (currentIndex > 0) renderQuestion(currentIndex - 1);
        });
    }
    
    if (btnNext) {
        btnNext.addEventListener('click', () => {
            if (currentIndex < questions.length - 1) {
                renderQuestion(currentIndex + 1);
            } else {
                // If it's the last question in the module, clicking next means finishing the module
                fetchNextModule();
            }
        });
    }

    if (btnFinish) {
        btnFinish.addEventListener('click', () => {
            fetchNextModule();
        });
    }

    function showScoreReport(data) {
        if (timerInterval) clearInterval(timerInterval);
        document.getElementById('scoreModalCorrect').textContent = `${data.correct_count} / ${data.total_attempted}`;
        document.getElementById('scoreModalScaled').textContent = data.score_scaled;
        scoreModal.classList.remove('hidden');
    }

    const btnCloseScoreModal = document.getElementById('btnCloseScoreModal');
    if (btnCloseScoreModal) {
        btnCloseScoreModal.addEventListener('click', () => {
            scoreModal.classList.add('hidden');
            window.location.href = '/';
        });
    }

    // --- Desmos Calculator Logic ---
    function initDesmos() {
        if (!desmosCalc && window.Desmos && calculatorContainer) {
            desmosCalc = Desmos.GraphingCalculator(calculatorContainer, { expressions: true, settingsMenu: false });
        }
    }

    if (calculatorBtn) {
        calculatorBtn.addEventListener('click', () => {
            desmosModal.classList.toggle('hidden');
        });
    }

    if (closeDesmosBtn) {
        closeDesmosBtn.addEventListener('click', () => {
            desmosModal.classList.add('hidden');
        });
    }

    // Draggable Desmos Modal Logic
    if (desmosHeader && desmosModal) {
        let isDragging = false;
        let startX, startY, initialX, initialY;

        desmosHeader.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            
            const rect = desmosModal.getBoundingClientRect();
            initialX = rect.left;
            initialY = rect.top;
            
            // Temporarily disable transitions during drag
            desmosModal.style.transition = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            
            // Ensure we update style as absolute positioning relative to window
            desmosModal.style.left = `${initialX + dx}px`;
            desmosModal.style.top = `${initialY + dy}px`;
            desmosModal.style.right = 'auto'; // Disable initial right constraint
            desmosModal.style.bottom = 'auto';
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    }
});
