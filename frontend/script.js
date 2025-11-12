document.addEventListener('DOMContentLoaded', () => {
    // Backend base URL: prefer an explicit override, fall back to localhost during dev,
    // otherwise use the production Render URL. Must not include the `/api/simplify` path
    // because fetch calls below append `/api/simplify`.
    // const BACKEND_BASE = (function() {
    //     // Allow a page-level override (useful when deploying static site with env injection)
    //     if (window.__BACKEND_BASE__) return window.__BACKEND_BASE__;
    //     const host = window.location.hostname;
    //     if (host === 'localhost' || host === '127.0.0.1') return 'http://localhost:5001';
    //     // Production default (adjust if your backend URL differs)
    //     return 'https://aisimplifier.onrender.com';
    // })();
    // const BACKEND_BASE = 'http://127.0.0.1:5001';

    const BACKEND_BASE = 'https://aisimplifier.onrender.com';
    let currentResult = '';
    let uploadedFile = null;

    // DOM elements (query after DOMContentLoaded to avoid null refs)
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');
    const textInput = document.getElementById('textInput');
    const simplifyBtn = document.getElementById('simplifyBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultContent = document.getElementById('resultContent');
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    // Defensive: ensure elements exist
    if (!uploadBox || !fileInput || !textInput || !simplifyBtn) {
        console.error('Frontend initialization failed: missing DOM elements');
        return;
    }

    // Ensure the simplify button behaves as a clickable button
    simplifyBtn.type = simplifyBtn.getAttribute('type') || 'button';
    simplifyBtn.style.zIndex = '1000';
    simplifyBtn.style.pointerEvents = 'auto';

    // Drag and drop events
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');

        const file = e.dataTransfer.files && e.dataTransfer.files[0];
        if (file && file.name && file.name.toLowerCase().endsWith('.txt')) {
            uploadedFile = file;
            readFile(file);
        } else {
            showError('Please upload a .txt file');
        }
    });

    // Make entire upload box clickable to open file chooser
    uploadBox.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const f = e.target.files && e.target.files[0];
        if (f) {
            uploadedFile = f;
            readFile(f);
        }
    });

    function readFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            textInput.value = e.target.result || '';
            // Ensure input event logic runs when we set value programmatically
            textInput.dispatchEvent(new Event('input', { bubbles: true }));
            // Mark simplify button enabled when a file was read
            simplifyBtn.disabled = false;
            simplifyBtn.style.pointerEvents = 'auto';
            console.log('File read and textarea populated. simplifyBtn.disabled =', simplifyBtn.disabled);
        };
        reader.onerror = (err) => {
            console.error('File read error', err);
            showError('Failed to read file');
        };
        reader.readAsText(file);
    }

    let userSession = localStorage.getItem('userSession') || generateSessionId();

    function generateSessionId() {
        const sessionId = 'user_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('userSession', sessionId);
        return sessionId;
    }

    async function simplifyDocument() {
        const file = uploadedFile || fileInput.files[0];
        const text = textInput.value.trim();

        if (!file && !text) {
            showError('Please upload a file or paste some text');
            return;
        }

        if (text && text.length < 50) {
            showError('Text is too short. Please provide a proper legal document.');
            return;
        }

        hideError();
        showLoading();
        simplifyBtn.disabled = true;
        simplifyBtn.style.pointerEvents = 'none';

        try {
            let body;
            let headers = {};

            if (file) {
                console.log("📤 Sending file to backend:", file.name);
                const formData = new FormData();
                formData.append('file', file);
                body = formData;
                // ❌ Don't set Content-Type manually — browser will handle it automatically.
                headers = {}; 
            } else if (text) {
                console.log("📤 Sending raw text to backend (JSON)");
                body = JSON.stringify({ text });
                headers['Content-Type'] = 'application/json';
            } else {
                showError('No valid input found.');
                return;
            }


            // Add a timeout to avoid hanging forever
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 180000); // 180s = 3 mins

            let response;
            try {
                response = await fetch(`${BACKEND_BASE}/api/simplify`, {
                    method: 'POST',
                    headers,
                    body,
                    signal: controller.signal,
                    credentials: 'omit'
                });
            } catch (err) {
                if (err.name === 'AbortError') throw new Error('Request timed out (180s)');
                throw err;
            } finally {
                clearTimeout(timeout);
            }

            // Prefer JSON response, but handle non-JSON error bodies too
            const contentType = response.headers.get('content-type') || '';
            if (!response.ok) {
                const bodyMsg = contentType.includes('application/json')
                    ? JSON.stringify(await response.json().catch(() => null))
                    : await response.text().catch(() => '(no body)');
                showError(`Server error ${response.status}: ${bodyMsg}`);
                return;
            }

            let data = null;
            if (contentType.includes('application/json')) {
                data = await response.json().catch(() => null);
            } else {
                const txt = await response.text().catch(() => '');
                if (txt) {
                    // Backend returned plain successful text (treat as simplified text)
                    displayResult(txt);
                    currentResult = txt;
                    return;
                }
            }

            if (!data) {
                showError('Empty or invalid response from backend');
                return;
            }

            if (data.success) {
                currentResult = data.simplified_text || data.result || '';
                displayResult(currentResult);
            } else {
                showError(data.error || 'Failed to simplify document');
            }
        } catch (error) {
            console.error('Simplify request failed:', error);
            showError(error.message || 'Connection error. Make sure the backend server is running on port 5000.');
        } finally {
            hideLoading();
            simplifyBtn.disabled = false;
            simplifyBtn.style.pointerEvents = 'auto';
        }
    }

    function displayResult(text) {
        const formattedText = (text || '').replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        resultContent.innerHTML = formattedText;
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function copyToClipboard() {
        navigator.clipboard.writeText(currentResult).then(() => {
            alert('Result copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
            showError('Failed to copy to clipboard');
        });
    }

    function downloadResult() {
        const blob = new Blob([currentResult], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'simplified-legal-document.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function resetForm() {
        fileInput.value = '';
        textInput.value = '';
        resultsSection.style.display = 'none';
        currentResult = '';
        uploadedFile = null;
        hideError();
        simplifyBtn.disabled = true;
        simplifyBtn.style.pointerEvents = 'auto';
    }

    function showLoading() {
        loading.style.display = 'block';
    }

    function hideLoading() {
        loading.style.display = 'none';
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function hideError() {
        errorDiv.style.display = 'none';
    }

    // Enable simplify button when there's input or a file
    textInput.addEventListener('input', () => {
        const hasText = textInput.value.trim().length >= 10;
        const hasFile = !!uploadedFile || !!fileInput.files[0];
        simplifyBtn.disabled = !(hasText || hasFile);
        simplifyBtn.style.pointerEvents = simplifyBtn.disabled ? 'none' : 'auto';
        console.log('Input event: text length', textInput.value.trim().length, 'uploadedFile?', !!uploadedFile, 'fileInput.files[0]?', !!fileInput.files[0], 'simplifyBtn.disabled=', simplifyBtn.disabled);
    });

    // Initialize
    simplifyBtn.disabled = true;
    simplifyBtn.style.pointerEvents = 'auto';

    // Defensive click listener to ensure clicks are handled (and for debugging)
    simplifyBtn.addEventListener('click', (e) => {
        console.log('Simplify button clicked', { disabled: simplifyBtn.disabled });
        if (!simplifyBtn.disabled) simplifyDocument();
    });

    // Expose a couple helpers to the global scope for debug and HTML buttons
    window.copyToClipboard = copyToClipboard;
    window.downloadResult = downloadResult;
    window.resetForm = resetForm;
});