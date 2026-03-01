const API_URL = 'http://127.0.0.1:8000/upload';
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const errorDiv = document.getElementById('error');
const downloadBtn = document.getElementById('downloadBtn');
const previewBtn = document.getElementById('previewBtn');
const preview = document.getElementById('preview');
let currentResult = null;

uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFile);
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
downloadBtn.addEventListener('click', handleDownload);
previewBtn.addEventListener('click', togglePreview);

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
}

function handleFile(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
}

async function handleFileSelect(file) {
    if (!file.name.endsWith('.py')) {
        showError('Please upload a .py file only!');
        return;
    }
    
    hideAll();
    showLoading();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentResult = data;
            showResults(data);
        } else {
            showError(data.detail || 'Processing failed!');
        }
    } catch (error) {
        showError('Server error. Make sure backend is running on port 8000');
    }
}

function showResults(data) {
    hideAll();
    results.classList.remove('hidden');
    
    document.getElementById('filename').textContent = data.filename;
    document.getElementById('functionsCount').textContent = 
        `${data.functions_found.length} functions documented`;
    document.getElementById('linesAdded').textContent = 
        `${data.quality_check.lines_added} lines added`;
    
    preview.classList.add('hidden');
}

function togglePreview() {
    preview.classList.toggle('hidden');
    if (!preview.classList.contains('hidden')) {
        showDocstringsPreview();
    }
}

function showDocstringsPreview() {
    const docstringsList = document.getElementById('docstringsList');
    docstringsList.innerHTML = '';
    
    currentResult.functions_found.forEach(func => {
        const funcDiv = document.createElement('div');
        funcDiv.className = 'function-preview';
        funcDiv.innerHTML = `
            <div class="function-name">${func.function_name}</div>
            <div class="docstring">${func.docstring}</div>
        `;
        docstringsList.appendChild(funcDiv);
    });
}

function handleDownload() {
    if (!currentResult || !currentResult.documented_code) {
        showError('No documented code available!');
        return;
    }
    
    // Create downloadable file
    const blob = new Blob([currentResult.documented_code], { type: 'text/x-python' });
    const url = URL.createObjectURL(blob);
    
    // Create download link
    const a = document.createElement('a');
    a.href = url;
    a.download = `documented_${currentResult.filename}`;
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Success feedback
    downloadBtn.textContent = '✅ Downloaded!';
    setTimeout(() => {
        downloadBtn.textContent = '📥 Download Documented File';
    }, 2000);
}

function showLoading() {
    loading.classList.remove('hidden');
}

function showError(message) {
    hideAll();
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideAll() {
    loading.classList.add('hidden');
    results.classList.add('hidden');
    errorDiv.classList.add('hidden');
    preview.classList.add('hidden');
}
