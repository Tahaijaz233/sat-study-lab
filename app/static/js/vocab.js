document.addEventListener('DOMContentLoaded', () => {
    let terms = [];
    let currentIndex = 0;
    let currentStatus = 'unseen';

    // DOM Elements
    const flashcard = document.getElementById('flashcard');
    const ratingControls = document.getElementById('ratingControls');
    const tabContainer = document.getElementById('tabContainer');
    
    const vocabCounter = document.getElementById('vocabCounter');
    const vocabWord = document.getElementById('vocabWord');
    const vocabPOS = document.getElementById('vocabPOS');
    const vocabEtymology = document.getElementById('vocabEtymology');

    const backVocabWord = document.getElementById('backVocabWord');
    const vocabDefinition = document.getElementById('vocabDefinition');
    const vocabUsage = document.getElementById('vocabUsage');
    const vocabDrill = document.getElementById('vocabDrill');
    const vocabSynonyms = document.getElementById('vocabSynonyms');
    const vocabAntonyms = document.getElementById('vocabAntonyms');

    const btnVocabPrev = document.getElementById('btnVocabPrev');
    const btnVocabNext = document.getElementById('btnVocabNext');

    async function loadVocabTerms() {
        const url = `/api/vocab?status=${currentStatus}&per_page=100`;
        try {
            const res = await fetch(url);
            const data = await res.json();
            terms = data.terms || [];
            currentIndex = 0;
            renderCard(0);
        } catch (err) {
            console.error("Failed to load vocab terms:", err);
        }
    }

    function renderCard(idx) {
        // Reset flip state
        if (flashcard) flashcard.classList.remove('rotate-y-180');
        if (ratingControls) ratingControls.classList.add('opacity-0', 'pointer-events-none');

        if (terms.length === 0) {
            vocabCounter.textContent = "0 terms";
            vocabWord.textContent = "All Done!";
            vocabPOS.textContent = "status";
            vocabEtymology.textContent = "No terms pending in this filter category.";
            backVocabWord.textContent = "Complete!";
            vocabDefinition.textContent = "Great job! Try switching to 'All Words' tab to review any word.";
            vocabUsage.textContent = "";
            vocabDrill.textContent = "";
            vocabSynonyms.textContent = "-";
            vocabAntonyms.textContent = "-";

            btnVocabPrev.disabled = true;
            btnVocabNext.disabled = true;
            return;
        }

        if (idx < 0) idx = 0;
        if (idx >= terms.length) idx = terms.length - 1;
        currentIndex = idx;

        const term = terms[idx];

        vocabCounter.textContent = `Card ${idx + 1} of ${terms.length}`;
        vocabWord.textContent = term.word;
        vocabPOS.textContent = term.part_of_speech || 'noun';
        vocabEtymology.textContent = term.roots_prefixes_suffixes || 'N/A';

        backVocabWord.textContent = term.word;
        vocabDefinition.textContent = term.definition;

        const usageArr = term.usage_examples || [];
        vocabUsage.textContent = usageArr.length > 0 ? `"${usageArr[0]}"` : "No usage example.";

        const drillArr = term.sentence_completion_drill || [];
        vocabDrill.textContent = drillArr.length > 0 ? drillArr[0] : "";

        const synArr = term.synonyms || [];
        vocabSynonyms.textContent = synArr.length > 0 ? synArr.join(', ') : 'None listed';

        const antArr = term.antonyms || [];
        vocabAntonyms.textContent = antArr.length > 0 ? antArr.join(', ') : 'None listed';

        btnVocabPrev.disabled = (idx === 0);
        btnVocabNext.disabled = (idx === terms.length - 1);
    }

    // Card Flip
    if (flashcard) {
        flashcard.addEventListener('click', () => {
            if (terms.length === 0) return;
            flashcard.classList.toggle('rotate-y-180');
            if (flashcard.classList.contains('rotate-y-180')) {
                ratingControls.classList.remove('opacity-0', 'pointer-events-none');
            } else {
                ratingControls.classList.add('opacity-0', 'pointer-events-none');
            }
        });
    }

    // SM-2 Rating Button Click
    if (ratingControls) {
        ratingControls.addEventListener('click', async (e) => {
            const btn = e.target.closest('button');
            if (!btn || terms.length === 0) return;

            const quality = parseInt(btn.dataset.quality, 10);
            const currentTerm = terms[currentIndex];

            try {
                const res = await fetch(`/api/vocab/${currentTerm.id}/rate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ quality: quality })
                });

                const data = await res.json();
                window.showToast(`Rated '${currentTerm.word}' (Quality ${quality}) -> Status: ${data.new_status}`, 'success');

                // Next card
                if (currentIndex < terms.length - 1) {
                    renderCard(currentIndex + 1);
                } else {
                    loadVocabTerms();
                }
            } catch (err) {
                console.error(err);
                window.showToast("Failed to record rating", "error");
            }
        });
    }

    // Tab Filters
    if (tabContainer) {
        tabContainer.addEventListener('click', (e) => {
            const btn = e.target.closest('.tab-btn');
            if (!btn) return;

            tabContainer.querySelectorAll('.tab-btn').forEach(b => {
                b.classList.remove('bg-white', 'dark:bg-gray-700', 'text-indigo-700', 'dark:text-indigo-300', 'shadow-sm');
                b.classList.add('text-gray-600', 'dark:text-gray-400');
            });

            btn.classList.add('bg-white', 'dark:bg-gray-700', 'text-indigo-700', 'dark:text-indigo-300', 'shadow-sm');
            btn.classList.remove('text-gray-600', 'dark:text-gray-400');

            currentStatus = btn.dataset.status;
            loadVocabTerms();
        });
    }

    // Manual Nav Buttons
    if (btnVocabPrev) btnVocabPrev.addEventListener('click', () => renderCard(currentIndex - 1));
    if (btnVocabNext) btnVocabNext.addEventListener('click', () => renderCard(currentIndex + 1));

    // Initial Load
    loadVocabTerms();
});
