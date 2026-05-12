(function () {
    const questions = JSON.parse(document.getElementById("questions-data").textContent);
    const config = window.MCQ_CONFIG;
    const storageKey = `mcq-${config.roleId}`;
    const questionBox = document.getElementById("questionBox");
    const progressBar = document.getElementById("progressBar");
    const timer = document.getElementById("timer");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let state = JSON.parse(localStorage.getItem(storageKey) || "null") || {
        index: 0,
        answers: {},
        remaining: config.durationSeconds,
        startedAt: Date.now()
    };

    function saveState() {
        localStorage.setItem(storageKey, JSON.stringify(state));
    }

    function renderQuestion() {
        if (!questions.length) {
            questionBox.innerHTML = "<p>No questions available.</p>";
            return;
        }
        const question = questions[state.index];
        const selected = state.answers[question.id];
        questionBox.innerHTML = `
            <p class="text-sm font-semibold text-slate-500">Question ${state.index + 1} of ${questions.length}</p>
            <h2 class="mt-3 text-2xl font-bold text-slate-950">${question.question}</h2>
            <div class="mt-6 grid gap-3">
                ${question.options.map(option => `
                    <button type="button" class="option-btn ${selected === option ? "selected" : ""}" data-option="${option}">
                        ${option}
                    </button>
                `).join("")}
            </div>
        `;
        questionBox.querySelectorAll(".option-btn").forEach(button => {
            button.addEventListener("click", () => {
                state.answers[question.id] = button.dataset.option;
                saveState();
                renderQuestion();
            });
        });
        progressBar.style.width = `${((state.index + 1) / questions.length) * 100}%`;
        prevBtn.disabled = state.index === 0;
        prevBtn.classList.toggle("opacity-50", state.index === 0);
        nextBtn.textContent = state.index === questions.length - 1 ? "Submit" : "Next";
    }

    function renderTimer() {
        const minutes = Math.floor(state.remaining / 60).toString().padStart(2, "0");
        const seconds = (state.remaining % 60).toString().padStart(2, "0");
        timer.textContent = `${minutes}:${seconds}`;
    }

    function getCookie(name) {
        return document.cookie
            .split(";")
            .map(cookie => cookie.trim())
            .find(cookie => cookie.startsWith(`${name}=`))
            ?.split("=")[1] || "";
    }

    async function submitTest() {
        nextBtn.disabled = true;
        nextBtn.textContent = "Submitting...";
        const timeTaken = Math.max(0, config.durationSeconds - state.remaining);
        const response = await fetch(config.submitUrl, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken") || config.csrfToken
            },
            body: JSON.stringify({
                role_id: config.roleId,
                answers: state.answers,
                time_taken: timeTaken
            })
        });
        const data = await response.json();
        localStorage.removeItem(storageKey);
        window.location.href = data.redirect_url;
    }

    prevBtn.addEventListener("click", () => {
        state.index = Math.max(0, state.index - 1);
        saveState();
        renderQuestion();
    });

    nextBtn.addEventListener("click", () => {
        if (state.index === questions.length - 1) {
            submitTest();
            return;
        }
        state.index += 1;
        saveState();
        renderQuestion();
    });

    renderQuestion();
    renderTimer();
    setInterval(() => {
        state.remaining -= 1;
        saveState();
        renderTimer();
        if (state.remaining <= 0) {
            submitTest();
        }
    }, 1000);
})();
