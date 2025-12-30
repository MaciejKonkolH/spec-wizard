const API_URL = '/api';
console.log('App v2 Loaded - Object Fix Applied');
let projectData = null;
let currentModuleId = 'global';
let currentLang = 'en';

const TRANSLATIONS = {
    en: {
        settings: "Settings",
        connecting: "Connecting...",
        save: "Save Changes",
        generate: "Generate Next Phase",
        settings_title: "Settings",
        settings_language: "Language:",
        settings_mode: "Mode:",
        settings_provider: "API Provider:",
        settings_key: "API Key:",
        close: "Close",
        save_settings: "Save Settings",
        mode_agent: "Agent Mode (Manual)",
        mode_api: "API Mode (Automatic)",
        phase: "Phase",
        type_answer: "Type your answer or extra details here...",
        saved_ok: "Saved successfully.",
        settings_saved: "Settings saved.",
        add_comment: "Add Comment",
        comment_placeholder: "Write your comment here...",
        recommended: "AI Recommended"
    },
    pl: {
        settings: "Ustawienia",
        connecting: "Łączenie...",
        save: "Zapisz Zmiany",
        generate: "Generuj Kolejną Fazę",
        settings_title: "Ustawienia",
        settings_language: "Język:",
        settings_mode: "Tryb:",
        settings_provider: "Dostawca API:",
        settings_key: "Klucz API:",
        close: "Zamknij",
        save_settings: "Zapisz Ustawienia",
        mode_agent: "Tryb Agenta (Manualny)",
        mode_api: "Tryb API (Automatyczny)",
        phase: "Faza",
        type_answer: "Wpisz tutaj swoją odpowiedź lub szczegóły...",
        saved_ok: "Zapisano pomyślnie.",
        settings_saved: "Ustawienia zapisane.",
        add_comment: "Dodaj Komentarz",
        comment_placeholder: "Wpisz swój komentarz...",
        recommended: "Sugerowane przez AI"
    }
};

// DOM Elements
const app = document.getElementById('app');
const saveBtn = document.getElementById('saveBtn');
const generateBtn = document.getElementById('generateBtn');
const statusMsg = document.getElementById('status-msg');

// Helper: Translate
function t(key) {
    return TRANSLATIONS[currentLang] ? (TRANSLATIONS[currentLang][key] || key) : key;
}

// Helper: Update UI Text
function updateUIText() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        // Only translate if we have a translation for this key
        const val = t(key);
        if (val !== key) el.textContent = val;
    });

    // Explicit IDs update
    const configBtn = document.querySelector('#configBtn span');
    if (configBtn) configBtn.textContent = t('settings');

    const saveBtnEl = document.querySelector('#saveBtn span');
    // Keep dirty state indicator logic if needed, but for now just text
    if (saveBtnEl) {
        saveBtnEl.textContent = t('save');
    }

    const generateBtnEl = document.querySelector('#generateBtn span');
    if (generateBtnEl) generateBtnEl.textContent = t('generate');

    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    if (closeSettingsBtn) closeSettingsBtn.textContent = t('close');

    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    if (saveSettingsBtn) saveSettingsBtn.textContent = t('save_settings');

    // Update Select Options (Manual way)
    const apiModeSelect = document.getElementById('apiModeSelect');
    if (apiModeSelect) {
        apiModeSelect.options[0].textContent = t('mode_agent');
        apiModeSelect.options[1].textContent = t('mode_api');
    }
}

// Initialization
async function init() {
    try {
        await loadConfig();
        await loadData();
    } catch (err) {
        showStatus('Error loading data: ' + err.message, 'error');
    }
}

async function loadData() {
    const res = await fetch(`${API_URL}/data`);
    projectData = await res.json();
    renderApp();
    const statusEl = document.getElementById('connectionStatus');
    if (statusEl) {
        statusEl.textContent = currentLang === 'pl' ? 'Połączono' : 'Connected';
        statusEl.style.color = '#4ec9b0';
    }
    showStatus(currentLang === 'pl' ? 'Dane wczytane.' : 'Data loaded.', 'info');
}

async function loadConfig() {
    const res = await fetch(`${API_URL}/config`);
    const config = await res.json();

    currentLang = config.language || 'en';

    // Update settings modal inputs
    const langSelect = document.getElementById('langSelect');
    if (langSelect) langSelect.value = currentLang;

    const apiModeSelect = document.getElementById('apiModeSelect');
    if (apiModeSelect) apiModeSelect.value = config.api_mode;

    const apiKeyInput = document.getElementById('apiKeyInput');
    if (apiKeyInput) apiKeyInput.value = config.api_key || '';

    // Update Generate Button State
    const hasKey = config.api_key && config.api_key.length > 0;
    const isApiMode = config.api_mode === true;

    // User requested: inactive if no external API key.
    // We assume this applies primarily to API mode, or generally if no key is present.
    // If Agent Mode, we might want to disable it too if the user considers 'Generate' = 'API Call'.
    // Let's implement: Active ONLY if API Mode is ON AND Key is present.
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
        if (isApiMode && hasKey) {
            generateBtn.disabled = false;
        } else {
            generateBtn.disabled = true;
        }
    }

    toggleApiSettings(config.api_mode);

    // Apply translations
    updateUIText();
}

// Rendering
function renderApp() {
    // Project Info
    document.getElementById('project-name').textContent = projectData.projectInfo.name;
    document.getElementById('project-desc').textContent = projectData.projectInfo.description;

    // Modules Tabs
    const tabsContainer = document.getElementById('modules-nav');
    tabsContainer.innerHTML = '';

    projectData.modules.forEach(mod => {
        const btn = document.createElement('button');
        btn.className = `tab-btn ${mod.id === currentModuleId ? 'active' : ''}`;
        btn.textContent = mod.name;
        btn.onclick = () => {
            currentModuleId = mod.id;
            renderApp();
        };
        tabsContainer.appendChild(btn);
    });

    // Content
    const activeModule = projectData.modules.find(m => m.id === currentModuleId);
    if (activeModule) {
        renderModule(activeModule);
    }
}

function renderModule(module) {
    const container = document.getElementById('module-content');
    container.innerHTML = '';

    module.phases.forEach(phase => {
        const phaseDiv = document.createElement('div');
        phaseDiv.className = 'phase-block';

        const title = document.createElement('div');
        title.className = 'phase-title';
        title.textContent = `${t('phase')} ${phase.id}: ${phase.name}`;
        phaseDiv.appendChild(title);

        phase.questions.forEach(q => {
            phaseDiv.appendChild(renderQuestion(q, phase.id));
        });

        container.appendChild(phaseDiv);
    });
}

function renderQuestion(q, phaseId) {
    const card = document.createElement('div');
    card.className = 'question-card';

    const text = document.createElement('div');
    text.className = 'question-text';
    text.textContent = q.text;
    card.appendChild(text);

    // Options
    if (q.type === 'single_choice' || q.type === 'multi_choice') {
        const optionsList = document.createElement('div');
        optionsList.className = 'options-list';

        q.options.forEach(optData => {
            // Support both string and object options
            const isObject = typeof optData === 'object' && optData !== null;
            const optId = isObject ? optData.id : optData;
            const optLabel = isObject ? optData.label : optData;

            const label = document.createElement('label');
            label.className = 'option-label';

            const input = document.createElement('input');
            input.type = q.type === 'single_choice' ? 'radio' : 'checkbox';
            input.name = `q_${q.id}`;
            input.value = optId;

            // Allow checking based on userResponse
            if (q.userResponse.selected && q.userResponse.selected.includes(optId)) {
                input.checked = true;
            }

            input.onchange = () => updateSelection(q, input.value, input.checked);

            label.appendChild(input);
            label.appendChild(document.createTextNode(optLabel));

            // Recommendation Check (Robust)
            let isRecommended = false;
            if (q.recommendation) {
                // Check new schemas: optionId, id. Fallback to option (string match)
                const recId = q.recommendation.optionId || q.recommendation.id || q.recommendation.option;
                if (recId === optId) isRecommended = true;
            }

            if (isRecommended) {
                label.classList.add('recommended');

                const badge = document.createElement('div');
                badge.className = 'rec-badge';
                badge.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg> ${t('recommended')}`;

                if (q.recommendation.reason) {
                    badge.title = q.recommendation.reason;
                }
                label.appendChild(badge);
            }

            optionsList.appendChild(label);
        });
        card.appendChild(optionsList);
    }

    // Custom / Open Input
    const customDiv = document.createElement('div');
    customDiv.style.marginTop = '10px';
    const customInput = document.createElement('textarea');
    customInput.className = 'custom-input';
    customInput.placeholder = t('type_answer');
    customInput.value = q.userResponse.customText || '';
    customInput.oninput = (e) => { q.userResponse.customText = e.target.value; markDirty(); };
    customDiv.appendChild(customInput);
    card.appendChild(customDiv);

    // Comment Section
    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment-section';

    const hasComment = q.userResponse.comment && q.userResponse.comment.length > 0;

    // Toggle Button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'comment-toggle';
    toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg> ${t('add_comment')}`;

    // Comment Input
    const commentInput = document.createElement('textarea');
    commentInput.className = `comment-input ${hasComment ? '' : 'hidden'}`;
    commentInput.placeholder = t('comment_placeholder');
    commentInput.value = q.userResponse.comment || '';
    commentInput.oninput = (e) => { q.userResponse.comment = e.target.value; markDirty(); };

    toggleBtn.onclick = () => {
        commentInput.classList.toggle('hidden');
        if (!commentInput.classList.contains('hidden')) {
            commentInput.focus();
        }
    };

    commentDiv.appendChild(toggleBtn);
    commentDiv.appendChild(commentInput);
    card.appendChild(commentDiv);

    return card;
}

function updateSelection(question, value, isChecked) {
    if (question.type === 'single_choice') {
        question.userResponse.selected = [value];
    } else {
        // Multi choice
        if (!question.userResponse.selected) question.userResponse.selected = [];
        if (isChecked) {
            question.userResponse.selected.push(value);
        } else {
            question.userResponse.selected = question.userResponse.selected.filter(v => v !== value);
        }
    }
    markDirty();
}

function markDirty() {
    const span = saveBtn.querySelector('span');
    if (span) {
        // Just append * if not present, or set text to translation + *
        // To be safe and handle language switches:
        span.textContent = t('save') + '*';
    }
    saveBtn.classList.add('dirty');
}

// Logic
async function saveData() {
    showStatus(currentLang === 'pl' ? 'Zapisywanie...' : 'Saving...', 'info');
    try {
        const res = await fetch(`${API_URL}/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });
        const result = await res.json();
        if (result.status === 'ok') {
            showStatus(t('saved_ok'), 'success');
            const span = saveBtn.querySelector('span');
            if (span) span.textContent = t('save');
            saveBtn.classList.remove('dirty');
        } else {
            throw new Error(result.message);
        }
    } catch (err) {
        showStatus('Error saving: ' + err.message, 'error');
    }
}

async function generateNext() {
    showStatus(currentLang === 'pl' ? 'Żądanie generowania...' : 'Requesting generation...', 'info');
    await saveData(); // Always save first

    try {
        const res = await fetch(`${API_URL}/generate`, { method: 'POST' });
        const result = await res.json();

        if (result.status === 'agent_mode') {
            alert(result.message);
        } else if (result.status === 'simulated') {
            alert(result.message);
            // In real app, we would reload data here
            await loadData();
        }
    } catch (err) {
        showStatus('Generation error: ' + err.message, 'error');
    }
}

// Settings Modal Logic
const modal = document.getElementById('settingsModal');
document.getElementById('configBtn').onclick = () => modal.classList.remove('hidden');
document.getElementById('closeSettingsBtn').onclick = () => modal.classList.add('hidden');
document.getElementById('apiModeSelect').onchange = (e) => toggleApiSettings(e.target.value === 'true');

function toggleApiSettings(isApiMode) {
    const els = document.querySelectorAll('.api-only');
    els.forEach(el => isApiMode ? el.classList.remove('hidden') : el.classList.add('hidden'));
}

document.getElementById('saveSettingsBtn').onclick = async () => {
    // 1. Get values
    const lang = document.getElementById('langSelect').value;
    const mode = document.getElementById('apiModeSelect').value === 'true';
    const provider = document.getElementById('apiProviderSelect').value;
    const key = document.getElementById('apiKeyInput').value;

    const newConfig = {
        language: lang,
        api_mode: mode,
        api_provider: provider,
        api_key: key
    };

    // 2. Save to backend
    await fetch(`${API_URL}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
    });

    // 3. UI Updates
    modal.classList.add('hidden');
    await loadConfig(); // Reloads config & applies translations
    showStatus(t('settings_saved'), 'success');
};

function showStatus(msg, type) {
    const toast = document.getElementById('status-toast');
    if (!toast) return;

    toast.textContent = msg;
    toast.className = 'toast show';
    if (type === 'success') toast.classList.add('success');
    if (type === 'error') toast.classList.add('error');

    setTimeout(() => {
        toast.className = 'toast hidden'; // Hide after 3s
    }, 3000);
}

// Listeners
saveBtn.onclick = saveData;
generateBtn.onclick = generateNext;

// Start
init();
