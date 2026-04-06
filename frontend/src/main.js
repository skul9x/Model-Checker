import './app.css';
import {ScanKeys, TestModel} from '../wailsjs/go/main/App';

const app = document.getElementById('app');

app.innerHTML = `
    <header>
        <div class="logo-wrapper">
            <div class="logo-icon">G</div>
            <h1>Gemini Key Inspector <span style="font-weight: 300; opacity: 0.5;">PRO</span></h1>
        </div>
        <div id="top-status" style="font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 15px;">
            <span>Sẵn sàng</span>
            <span style="opacity: 0.5;">© 2026 Nguyễn Duy Trường</span>
        </div>
    </header>
    
    <main>
        <section class="panel panel-input">
            <div class="panel-header">
                <span>Dữ liệu đầu vào (Logs / Text)</span>
                <button id="btn-clear" style="padding: 2px 10px; font-size: 0.7rem; background: rgba(255,255,255,0.1);">Xóa hết</button>
            </div>
            <textarea id="input-text" placeholder="Dán nội dung log, JSON hoặc văn bản chứa key AIza... vào đây"></textarea>
        </section>
        
        <section class="panel panel-results">
            <div class="panel-header">
                <span>Kết quả tìm thấy</span>
                <div id="active-count" style="font-size: 0.75rem; color: var(--success-color);"></div>
            </div>
            <div class="results-container" id="results-list">
                <div style="text-align: center; color: var(--text-muted); margin-top: 50px;">
                    <p>Nhập key và nhấn quét để bắt đầu</p>
                </div>
            </div>
        </section>
    </main>
    
    <div class="controls">
        <div class="stats" id="stats-line">Tổng số Key: 0 | Đã kiểm tra: 0 | Hoạt động: 0</div>
        <button id="btn-test-all" disabled>⚡ KIỂM TRA TẤT CẢ</button>
        <button id="btn-scan">QUÉT & KIỂM TRA KEY</button>
    </div>

    <div id="test-all-overlay" class="test-all-overlay hidden">
        <div class="test-all-panel">
            <div class="test-all-header">
                <h2>⚡ Kết quả kiểm tra Models</h2>
                <button id="btn-close-panel" class="btn-close-panel">✕</button>
            </div>
            <div id="test-all-progress" class="test-all-progress hidden">
                <div class="progress-bar-track">
                    <div id="progress-bar-fill" class="progress-bar-fill"></div>
                </div>
                <span id="progress-text">Đang kiểm tra...</span>
            </div>
            <div id="test-all-results" class="test-all-results"></div>
            <div id="test-all-footer" class="test-all-footer hidden">
                <div id="test-all-summary" class="test-all-summary"></div>
                <button id="btn-copy-working" class="btn-copy-working">📋 Copy danh sách Model hoạt động</button>
            </div>
        </div>
    </div>
`;

const inputText = document.getElementById('input-text');
const btnScan = document.getElementById('btn-scan');
const btnClear = document.getElementById('btn-clear');
const btnTestAll = document.getElementById('btn-test-all');
const resultsList = document.getElementById('results-list');
const statsLine = document.getElementById('stats-line');

// Test All panel elements
const testAllOverlay = document.getElementById('test-all-overlay');
const testAllProgress = document.getElementById('test-all-progress');
const progressBarFill = document.getElementById('progress-bar-fill');
const progressText = document.getElementById('progress-text');
const testAllResults = document.getElementById('test-all-results');
const testAllFooter = document.getElementById('test-all-footer');
const testAllSummary = document.getElementById('test-all-summary');
const btnClosePanel = document.getElementById('btn-close-panel');
const btnCopyWorking = document.getElementById('btn-copy-working');

let lastScanResults = null; // Store scan results for Test All
let isTestingAll = false;

btnClear.onclick = () => inputText.value = '';

btnScan.onclick = async () => {
    const text = inputText.value;
    if (!text.trim()) return;

    btnScan.disabled = true;
    btnScan.innerHTML = '<span class="loading">ĐANG QUÉT...</span>';
    resultsList.innerHTML = '';
    
    try {
        const results = await ScanKeys(text);
        lastScanResults = results;
        renderResults(results);
        // Enable Test All button if there are active keys with models
        const hasModels = results.some(r => r.status === 'ACTIVE' && r.models && r.models.length > 0);
        btnTestAll.disabled = !hasModels;
    } catch (e) {
        resultsList.innerHTML = `<div class="status-error" style="padding: 1rem;">Lỗi hệ thống: ${e}</div>`;
    } finally {
        btnScan.disabled = false;
        btnScan.innerHTML = 'QUÉT & KIỂM TRA KEY';
    }
};

function renderResults(results) {
    if (results.length === 0) {
        resultsList.innerHTML = '<div style="text-align: center; color: var(--text-muted); margin-top: 50px;">Không tìm thấy API Key nào trong dữ liệu.</div>';
        statsLine.innerText = `Tổng số Key: 0 | Đã kiểm tra: 0 | Hoạt động: 0`;
        return;
    }

    const activeCount = results.filter(r => r.status === 'ACTIVE').length;
    statsLine.innerText = `Tổng số Key: ${results.length} | Đã kiểm tra: ${results.length} | Hoạt động: ${activeCount}`;

    resultsList.innerHTML = '';
    results.forEach(res => {
        const keyItem = document.createElement('div');
        keyItem.className = 'key-item';
        
        const maskedKey = res.key.substring(0, 6) + '...' + res.key.substring(res.key.length - 4);
        const statusText = res.status === 'ACTIVE' ? 'HOẠT ĐỘNG' : 'LỖI/CHẾT';
        
        keyItem.innerHTML = `
            <div class="key-summary">
                <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                <span class="key-name">${maskedKey}</span>
                <span class="status-badge status-${res.status.toLowerCase()}">${statusText}</span>
            </div>
            <div class="model-list">
                ${res.status === 'ACTIVE' 
                    ? res.models.map(m => `
                        <div class="model-item" data-key="${res.key}" data-model="${m.name}">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="model-name">${m.name}</span>
                                <button class="btn-ping">Kiểm tra</button>
                            </div>
                            <p class="model-desc">${m.description}</p>
                            <div class="ping-result"></div>
                        </div>
                    `).join('')
                    : `<div style="color: var(--error-color); font-size: 0.8rem;">${res.error}</div>`
                }
            </div>
        `;

        const summary = keyItem.querySelector('.key-summary');
        summary.onclick = () => keyItem.classList.toggle('expanded');
        
        summary.oncontextmenu = (e) => {
            e.preventDefault();
            navigator.clipboard.writeText(res.key);
            showToast('Đã sao chép API Key');
        };

        // Ping logic
        keyItem.querySelectorAll('.btn-ping').forEach(btn => {
            btn.onclick = async (e) => {
                e.stopPropagation();
                const item = btn.closest('.model-item');
                const key = item.dataset.key;
                const model = item.dataset.model;
                const resDiv = item.querySelector('.ping-result');

                btn.disabled = true;
                btn.innerText = '...';
                resDiv.innerHTML = '';

                try {
                    const response = await TestModel(key, model);
                    resDiv.innerHTML = `<span style="color: var(--success-color); font-size: 0.75rem;">✅ Model phản hồi: "${response.substring(0, 30)}..."</span>`;
                } catch (err) {
                    resDiv.innerHTML = `<span style="color: var(--error-color); font-size: 0.75rem;">❌ Lỗi: ${err}</span>`;
                } finally {
                    btn.disabled = false;
                    btn.innerText = 'Kiểm tra';
                }
            };
        });

        resultsList.appendChild(keyItem);
    });
}

// ========================
// TEST ALL MODELS LOGIC
// ========================

btnTestAll.onclick = () => {
    if (!lastScanResults || isTestingAll) return;
    runTestAll(lastScanResults);
};

btnClosePanel.onclick = () => {
    if (!isTestingAll) {
        testAllOverlay.classList.add('hidden');
    }
};

testAllOverlay.onclick = (e) => {
    if (e.target === testAllOverlay && !isTestingAll) {
        testAllOverlay.classList.add('hidden');
    }
};

async function runTestAll(results) {
    isTestingAll = true;
    btnTestAll.disabled = true;
    btnTestAll.innerHTML = '<span class="loading">⚡ ĐANG KIỂM TRA...</span>';

    // Show overlay & progress
    testAllOverlay.classList.remove('hidden');
    testAllProgress.classList.remove('hidden');
    testAllFooter.classList.add('hidden');
    testAllResults.innerHTML = '';
    progressBarFill.style.width = '0%';

    // Collect all model-key pairs
    const tasks = [];
    results.forEach(res => {
        if (res.status === 'ACTIVE' && res.models) {
            res.models.forEach(m => {
                tasks.push({ key: res.key, model: m.name, keyMasked: res.key.substring(0, 6) + '...' + res.key.substring(res.key.length - 4) });
            });
        }
    });

    const total = tasks.length;
    let completed = 0;
    const workingModels = [];
    const failedModels = [];

    progressText.innerText = `Đang kiểm tra 0/${total} models...`;

    // Batch concurrent: 5 at a time
    const BATCH_SIZE = 5;
    for (let i = 0; i < tasks.length; i += BATCH_SIZE) {
        const batch = tasks.slice(i, i + BATCH_SIZE);
        const promises = batch.map(async (task) => {
            try {
                const response = await TestModel(task.key, task.model);
                workingModels.push({ ...task, response: response.substring(0, 50) });
                appendTestResult(task, true, response.substring(0, 50));
            } catch (err) {
                failedModels.push({ ...task, error: String(err) });
                appendTestResult(task, false, String(err));
            } finally {
                completed++;
                const pct = Math.round((completed / total) * 100);
                progressBarFill.style.width = pct + '%';
                progressText.innerText = `Đang kiểm tra ${completed}/${total} models...`;
            }
        });
        await Promise.all(promises);
    }

    // Done - show summary
    progressText.innerText = `Hoàn tất! ${completed}/${total} models đã kiểm tra.`;
    testAllFooter.classList.remove('hidden');
    testAllSummary.innerHTML = `
        <span class="summary-ok">✅ ${workingModels.length} hoạt động</span>
        <span class="summary-fail">❌ ${failedModels.length} lỗi</span>
    `;

    // Store for copy
    btnCopyWorking.onclick = () => {
        if (workingModels.length === 0) {
            showToast('Không có model nào hoạt động để copy!');
            return;
        }
        const text = workingModels.map(m => m.model).join('\n');
        navigator.clipboard.writeText(text);
        showToast(`Đã copy ${workingModels.length} models hoạt động!`);
        btnCopyWorking.innerText = '✅ Đã copy!';
        setTimeout(() => { btnCopyWorking.innerText = '📋 Copy danh sách Model hoạt động'; }, 2000);
    };

    isTestingAll = false;
    btnTestAll.disabled = false;
    btnTestAll.innerHTML = '⚡ KIỂM TRA TẤT CẢ';
}

function appendTestResult(task, success, detail) {
    const div = document.createElement('div');
    div.className = `test-result-item ${success ? 'result-ok' : 'result-fail'}`;
    div.innerHTML = `
        <span class="result-icon">${success ? '✅' : '❌'}</span>
        <div class="result-info">
            <span class="result-model">${task.model}</span>
            <span class="result-key">${task.keyMasked}</span>
        </div>
        <span class="result-detail">${success ? '"' + detail + '..."' : detail}</span>
    `;
    testAllResults.appendChild(div);
    // Auto-scroll to bottom
    testAllResults.scrollTop = testAllResults.scrollHeight;
}

function showToast(msg) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
        background: var(--accent-color); color: white; padding: 8px 16px;
        border-radius: 20px; font-size: 0.8rem; z-index: 2000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: fadeIn 0.2s ease-out;
    `;
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.5s';
        setTimeout(() => toast.remove(), 500);
    }, 2000);
}
