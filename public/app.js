const API_URL = '/api';
console.log('App v2 Loaded - Object Fix Applied');
let projectData = null;
let currentModuleId = 'global';
let currentPhaseId = null;
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
        phase_label: "Phase",
        type_answer: "Type your answer or extra details here...",
        saved_ok: "Saved successfully.",
        settings_saved: "Settings saved.",
        add_comment: "Add Comment",
        comment_placeholder: "Write your comment here...",
        recommended: "AI Recommended",
        project_context: "Project Context"
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
        phase_label: "Faza",
        type_answer: "Wpisz tutaj swoją odpowiedź lub szczegóły...",
        saved_ok: "Zapisano pomyślnie.",
        settings_saved: "Ustawienia zapisane.",
        add_comment: "Dodaj Komentarz",
        comment_placeholder: "Wpisz swój komentarz...",
        recommended: "Sugerowane przez AI",
        project_context: "Kontekst Projektu"
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
    console.log('Initializing Spec Wizard...');
    try {
        await loadConfig();
        await loadProjects();
        await loadData();
        console.log('Init successful. Project:', projectData.projectInfo.name);
    } catch (err) {
        console.error('INIT ERROR:', err);
        showStatus('Error loading data: ' + err.message, 'error');
        displayErrorOnPage('Initialization Error: ' + err.message);
    }
}

function displayErrorOnPage(msg) {
    const errorDiv = document.createElement('div');
    errorDiv.style.background = '#ff4d4d';
    errorDiv.style.color = 'white';
    errorDiv.style.padding = '15px';
    errorDiv.style.margin = '10px';
    errorDiv.style.borderRadius = '8px';
    errorDiv.style.fontWeight = 'bold';
    errorDiv.textContent = msg;
    document.body.prepend(errorDiv);
}

async function loadData() {
    try {
        const res = await fetch(`${API_URL}/data`);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.error || err.message || `Server returned ${res.status}`);
        }
        projectData = await res.json();

        if (!projectData || !projectData.modules) {
            throw new Error("Invalid project data received");
        }

        renderApp();
        const statusEl = document.getElementById('connectionStatus');
        if (statusEl) {
            statusEl.textContent = currentLang === 'pl' ? 'Połączono' : 'Connected';
            statusEl.style.color = '#4ec9b0';
        }
        showStatus(currentLang === 'pl' ? 'Dane wczytane.' : 'Data loaded.', 'info');
    } catch (err) {
        console.error('LOAD DATA ERROR:', err);
        displayErrorOnPage('Data Loading Error: ' + err.message);
        throw err;
    }
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

    const apiProviderSelect = document.getElementById('apiProviderSelect');
    if (apiProviderSelect) apiProviderSelect.value = config.api_provider || 'openai';

    const apiKeyInput = document.getElementById('apiKeyInput');
    if (apiKeyInput) apiKeyInput.value = config.api_key || '';

    const apiModelSelect = document.getElementById('apiModelSelect');
    if (apiModelSelect) {
        apiModelSelect.dataset.savedValue = config.api_model || '';
    }

    // Update Generate Button State
    const hasKey = config.api_key && config.api_key.length > 0;
    const isApiMode = config.api_mode === true;

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

async function loadProjects() {
    const res = await fetch(`${API_URL}/projects`);
    const data = await res.json();
    const select = document.getElementById('projectSelect');
    if (!select) return;

    select.innerHTML = '';
    if (data && data.projects && Array.isArray(data.projects)) {
        data.projects.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.id;
            opt.textContent = p.name;
            // Robust path comparison for Windows/Unix
            const cleanPath = (path) => path.replace(/\\/g, '/');
            if (cleanPath(p.id) === cleanPath(data.active)) opt.selected = true;
            select.appendChild(opt);
        });
    }

    select.onchange = async () => {
        const projectId = select.value;
        await fetch(`${API_URL}/projects/select`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: projectId })
        });
        await init(); // Reload app with new project
    };
}

// Rendering
function renderApp() {
    console.log('Rendering app... Active Module ID:', currentModuleId);
    try {
        // Project Info
        document.getElementById('project-name').textContent = projectData.projectInfo.name;
        document.getElementById('project-desc').textContent = projectData.projectInfo.description;

        // Modules Tabs
        const tabsContainer = document.getElementById('modules-nav');
        tabsContainer.innerHTML = '';

        // If currentModuleId is not in the data, default to the first module
        if (!projectData.modules.find(m => m.id === currentModuleId)) {
            if (projectData.modules.length > 0) {
                currentModuleId = projectData.modules[0].id;
                console.log('Fallback to first module:', currentModuleId);
            }
        }

        if (projectData && projectData.modules && Array.isArray(projectData.modules)) {
            console.dir(projectData); // Debug modular structure
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
        }

        // Content
        const activeModule = projectData.modules.find(m => m.id === currentModuleId);
        if (activeModule) {
            console.log('Rendering active module:', activeModule.name);

            // Phase Tabs
            const phaseNav = document.getElementById('phases-nav');
            phaseNav.innerHTML = '';

            if (activeModule.phases && activeModule.phases.length > 0) {
                // Defensive check: if server didn't merge phases, handle it gracefully
                const isMerged = typeof activeModule.phases[0] === 'object';

                if (isMerged && currentPhaseId === null) {
                    const unanswered = activeModule.phases.find(p => p.questions && p.questions.some(q => !q.userResponse.selected?.length && !q.userResponse.customText?.trim()));
                    currentPhaseId = unanswered ? unanswered.id : activeModule.phases[0].id;
                }
                if (isMerged && !activeModule.phases.find(p => p.id === currentPhaseId)) {
                    currentPhaseId = activeModule.phases[0].id;
                } else if (!isMerged) {
                    currentPhaseId = null;
                }

                activeModule.phases.forEach((phase, index) => {
                    const pBtn = document.createElement('button');
                    const phaseId = (isMerged && phase) ? phase.id : (index + 1);
                    const phaseName = (isMerged && phase && phase.name) ? phase.name : `Phase ${phaseId}`;
                    const isCompleted = isMerged && phase && phase.status === 'completed';

                    pBtn.className = `phase-tab-btn ${phaseId === currentPhaseId ? 'active' : ''} ${isCompleted ? 'completed' : ''}`;
                    pBtn.textContent = phaseName;

                    if (isMerged) {
                        pBtn.onclick = () => {
                            currentPhaseId = phase.id;
                            renderApp();
                        };
                    } else {
                        pBtn.title = "Please restart your server to enable modular loading.";
                        pBtn.style.opacity = '0.5';
                    }
                    phaseNav.appendChild(pBtn);
                });

                if (!isMerged) {
                    const warn = document.createElement('div');
                    warn.style.color = 'var(--warning)';
                    warn.style.fontSize = '0.8rem';
                    warn.style.marginTop = '0.5rem';
                    warn.textContent = currentLang === 'pl' ? '⚠️ Zrestartuj serwer (server.py), aby aktywować nową strukturę plików.' : '⚠️ Restart server.py to activate new modular structure.';
                    phaseNav.appendChild(warn);
                }
            }

            renderModuleInfo(activeModule);
            renderModule(activeModule);
            updateContextPanel(activeModule);
        } else {
            console.warn('No active module found for ID:', currentModuleId);
        }
    } catch (err) {
        console.error('RENDER ERROR:', err);
        displayErrorOnPage('Render Error: ' + err.message);
    }
}

function updateContextPanel(module) {
    const globalEl = document.getElementById('global-context-text');
    const moduleEl = document.getElementById('module-context-text');

    const formatContext = (ctx) => {
        if (!ctx) return null;
        if (typeof ctx === 'string') return ctx;
        if (typeof ctx === 'object') {
            // Priority: vision or first property or join all values
            if (ctx.vision) return ctx.vision;
            return Object.values(ctx).join(' ');
        }
        return String(ctx);
    };

    if (globalEl) {
        const ctxText = formatContext(projectData.projectInfo.contextSummary);
        globalEl.textContent = ctxText || (currentLang === 'pl' ? 'Brak globalnych ustaleń.' : 'No global context yet.');
    }

    if (moduleEl) {
        const ctxText = formatContext(module.contextSummary);
        moduleEl.textContent = ctxText || (currentLang === 'pl' ? 'Brak ustaleń dla tego modułu.' : 'No module context yet.');
    }
}

function renderModuleInfo(module) {
    const container = document.getElementById('module-info');
    if (!container) return;
    container.innerHTML = '';

    const modHeader = document.createElement('div');
    modHeader.className = 'module-header';
    modHeader.innerHTML = `
        <h2>
            <span class="id-badge">${module.id}</span>
            ${module.name}
        </h2>
        ${module.description ? `<div class="module-desc">${module.description}</div>` : ''}
    `;
    container.appendChild(modHeader);
}

function renderModule(module) {
    const container = document.getElementById('module-content');
    container.innerHTML = '';

    if (!module || !module.phases || !Array.isArray(module.phases)) return;

    // Filter to current active phase
    const phase = module.phases.find(p => p.id === currentPhaseId);
    if (!phase) return;

    let firstUnansweredEl = null;
    let anyAnswered = false;

    const phaseDiv = document.createElement('div');
    phaseDiv.className = 'phase-block';

    const title = document.createElement('div');
    title.className = 'phase-title';
    title.innerHTML = `<span class="phase-id">PHASE ${phase.id}:</span> ${phase.name}`;
    phaseDiv.appendChild(title);

    // Phase Context Display
    if (phase.contextSummary) {
        const ctxDiv = document.createElement('div');
        ctxDiv.className = 'context-text';
        ctxDiv.style.marginBottom = '1.5rem';
        ctxDiv.style.fontSize = '0.8rem';
        ctxDiv.textContent = phase.contextSummary;
        phaseDiv.appendChild(ctxDiv);
    }

    if (phase.questions && Array.isArray(phase.questions)) {
        phase.questions.forEach(q => {
            const card = renderQuestion(q, phase.id);
            phaseDiv.appendChild(card);

            if (!q.userResponse) {
                q.userResponse = { selected: [], customText: "", comment: "" };
            }

            const isAnswered = (q.userResponse.selected && q.userResponse.selected.length > 0) ||
                (q.userResponse.customText && q.userResponse.customText.trim().length > 0);

            if (isAnswered) anyAnswered = true;

            if (!firstUnansweredEl && !isAnswered) {
                firstUnansweredEl = card;
            }
        });
    }

    container.appendChild(phaseDiv);

    // Scroll to first unanswered only if some questions are already answered
    // AND if the first unanswered is NOT the first question (to avoid jump on load)
    if (anyAnswered && firstUnansweredEl) {
        setTimeout(() => {
            firstUnansweredEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}

function renderQuestion(q, phaseId) {
    const card = document.createElement('div');
    card.className = 'question-card';
    card.id = `q-${q.id}`;

    const qIdLabel = document.createElement('span');
    qIdLabel.className = 'question-id';
    qIdLabel.textContent = `ID: ${q.id}`;
    card.appendChild(qIdLabel);

    const text = document.createElement('div');
    text.className = 'question-text';
    text.textContent = q.text;
    card.appendChild(text);

    if (q.description) {
        const desc = document.createElement('div');
        desc.className = 'question-description';
        desc.textContent = q.description;
        card.appendChild(desc);
    }

    // Options
    if (q.type === 'single_choice' || q.type === 'multi_choice') {
        const optionsList = document.createElement('div');
        optionsList.className = 'options-list';

        if (q.options && Array.isArray(q.options)) {
            q.options.forEach(optData => {
                // Support both string and object options
                const isObject = typeof optData === 'object' && optData !== null;
                const optId = isObject ? optData.id : optData;
                const optLabel = isObject ? optData.label : optData;
                const optDesc = isObject ? optData.description : null;

                const label = document.createElement('label');
                label.className = 'option-label';

                const main = document.createElement('div');
                main.className = 'option-main';

                const input = document.createElement('input');
                input.type = q.type === 'single_choice' ? 'radio' : 'checkbox';
                input.name = `q_${q.id}`;
                input.value = optId;

                // Allow checking based on userResponse
                if (q.userResponse && q.userResponse.selected && q.userResponse.selected.includes(optId)) {
                    input.checked = true;
                }

                input.onchange = () => updateSelection(q, input.value, input.checked);

                main.appendChild(input);
                main.appendChild(document.createTextNode(optLabel));

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
                    main.appendChild(badge);
                }

                label.appendChild(main);

                if (optDesc) {
                    const descDiv = document.createElement('div');
                    descDiv.className = 'option-description';
                    descDiv.textContent = optDesc;
                    label.appendChild(descDiv);
                }

                optionsList.appendChild(label);
            });
        }
        card.appendChild(optionsList);
    }

    // Custom / Open Input
    const customDiv = document.createElement('div');
    customDiv.style.marginTop = '10px';
    const customInput = document.createElement('textarea');
    customInput.className = 'custom-input';
    customInput.placeholder = t('type_answer');
    if (!q.userResponse) q.userResponse = { selected: [], customText: "", comment: "" };
    customInput.value = q.userResponse.customText || '';
    customInput.oninput = (e) => {
        if (!q.userResponse) q.userResponse = { selected: [], customText: "", comment: "" };
        q.userResponse.customText = e.target.value;
        markDirty();
    };
    customDiv.appendChild(customInput);
    card.appendChild(customDiv);

    // Comment Section
    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment-section';

    const hasComment = q.userResponse && q.userResponse.comment && q.userResponse.comment.length > 0;

    // Toggle Button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'comment-toggle';
    toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg> ${t('add_comment')}`;

    // Comment Input
    const commentInput = document.createElement('textarea');
    commentInput.className = `comment-input ${hasComment ? '' : 'hidden'}`;
    commentInput.placeholder = t('comment_placeholder');
    commentInput.value = (q.userResponse && q.userResponse.comment) || '';
    commentInput.oninput = (e) => {
        if (!q.userResponse) q.userResponse = { selected: [], customText: "", comment: "" };
        q.userResponse.comment = e.target.value;
        markDirty();
    };

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
    if (!question.userResponse) question.userResponse = { selected: [], customText: "", comment: "" };
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
    const btnText = generateBtn.querySelector('.btn-text-gen');
    const originalText = btnText.textContent;

    try {
        generateBtn.disabled = true;
        generateBtn.classList.add('loading');
        if (btnText) btnText.textContent = (currentLang === 'pl' ? 'Generowanie...' : 'Generating...');

        // Always save first
        await saveData();

        const res = await fetch(`${API_URL}/generate`, { method: 'POST' });
        const data = await res.json();

        if (data.status === 'simulated' || data.status === 'ok') {
            await init(); // Reload data and UI
            showStatus(t('gen_success'), 'success');
        } else {
            showStatus(data.message || 'Error', 'error');
        }
    } catch (err) {
        showStatus(err.message, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.classList.remove('loading');
        if (btnText) btnText.textContent = originalText;
    }
}

async function fetchAndPopulateModels(currentSavedModel = '') {
    const select = document.getElementById('apiModelSelect');
    if (!select) return;

    // Get current provider and key from inputs
    const provider = document.getElementById('apiProviderSelect').value;
    const key = document.getElementById('apiKeyInput').value;

    select.innerHTML = `<option value="">${currentLang === 'pl' ? 'Pobieranie...' : 'Loading...'}</option>`;

    try {
        // Send provider and current key to server for better discovery
        const res = await fetch(`${API_URL}/models?provider=${provider}&key=${encodeURIComponent(key)}`);
        const data = await res.json();

        if (data.error) throw new Error(data.error);

        select.innerHTML = '';
        const rawModels = data.models || data.data || [];

        rawModels.forEach(m => {
            // Gemini uses m.name, OpenAI uses m.id
            const name = (m.id || m.name || m).split('/').pop();
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            if (name === currentSavedModel) opt.selected = true;
            select.appendChild(opt);
        });

        if (select.options.length === 0) {
            select.innerHTML = '<option value="">No models found</option>';
        }
    } catch (err) {
        select.innerHTML = `<option value="">Error: ${err.message}</option>`;
    }
}

// Settings Modal Logic
const modal = document.getElementById('settingsModal');
document.getElementById('configBtn').onclick = () => {
    modal.classList.remove('hidden');
    const apiMode = document.getElementById('apiModeSelect').value === 'true';
    if (apiMode) {
        fetchAndPopulateModels(document.getElementById('apiModelSelect').dataset.savedValue);
    }
};

document.getElementById('closeSettingsBtn').onclick = () => modal.classList.add('hidden');

document.getElementById('apiModeSelect').onchange = (e) => {
    const isApi = e.target.value === 'true';
    toggleApiSettings(isApi);
    if (isApi) fetchAndPopulateModels();
};

document.getElementById('apiProviderSelect').onchange = () => {
    fetchAndPopulateModels();
};

function toggleApiSettings(isApiMode) {
    const els = document.querySelectorAll('.api-only');
    els.forEach(el => isApiMode ? el.classList.remove('hidden') : el.classList.add('hidden'));
}



document.getElementById('saveSettingsBtn').onclick = async () => {
    // 1. Get values
    const lang = document.getElementById('langSelect').value;
    const mode = document.getElementById('apiModeSelect').value === 'true';
    const provider = document.getElementById('apiProviderSelect').value;
    const modelName = document.getElementById('apiModelSelect').value;
    const key = document.getElementById('apiKeyInput').value;

    const newConfig = {
        language: lang,
        api_mode: mode,
        api_provider: provider,
        api_model: modelName,
        api_key: key
    };

    // 2. Save to backend
    await fetch(`${API_URL}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
    });

    // Save current model into dataset
    document.getElementById('apiModelSelect').dataset.savedValue = modelName;

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
