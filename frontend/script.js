const API_URL = 'http://127.0.0.1:8000/upload';

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorDiv = document.getElementById('error');
const preview = document.getElementById('preview');
const docStyle = document.getElementById('docStyle');
const fileMeta = document.getElementById('fileMeta');

const generateBtn = document.getElementById('generateBtn');
const previewBtn = document.getElementById('previewBtn');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');
const downloadBtnTop = document.getElementById('downloadBtnTop');
const copyBtnTop = document.getElementById('copyBtnTop');

const statsSection = document.getElementById('statsSection');
const filenameEl = document.getElementById('filename');
const classesCountEl = document.getElementById('classesCount');
const functionsCountEl = document.getElementById('functionsCount');
const linesAddedEl = document.getElementById('linesAdded');

const originalCodeEl = document.getElementById('originalCode');
const generatedCodeEl = document.getElementById('generatedCode');
const docstringsList = document.getElementById('docstringsList');

let currentFile = null;
let currentFileText = '';
let currentResult = null;
let currentGeneratedText = '';

const allowedExtensions = ['.py', '.js', '.java', '.ts'];

uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    fileInput.click();
  }
});

fileInput.addEventListener('change', handleFile);
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);

generateBtn.addEventListener('click', handleGenerate);
previewBtn.addEventListener('click', togglePreview);
downloadBtn.addEventListener('click', handleDownload);
downloadBtnTop.addEventListener('click', handleDownload);
copyBtn.addEventListener('click', handleCopy);
copyBtnTop.addEventListener('click', handleCopy);

function handleDragOver(e) {
  e.preventDefault();
  uploadArea.classList.add('dragover');
}

function handleDragLeave() {
  uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) handleFileSelect(files[0]);
}

function handleFile(e) {
  const file = e.target.files[0];
  if (file) handleFileSelect(file);
}

async function handleFileSelect(file) {
  const isValid = allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
  if (!isValid) {
    showError('Please upload a supported file (.py, .js, .java, .ts)');
    return;
  }

  currentFile = file;
  currentResult = null;
  currentGeneratedText = '';
  currentFileText = '';

  resetUI();
  hideMessages();

  fileMeta.textContent = `${file.name} · ${formatSize(file.size)}`;
  generateBtn.disabled = false;

  try {
    currentFileText = await file.text();
    originalCodeEl.textContent = currentFileText || 'This file appears to be empty.';
    resultsSection.classList.remove('d-none');
    statsSection.classList.remove('d-none');
    filenameEl.textContent = file.name;
    functionsCountEl.textContent = '0';
    classesCountEl.textContent = countClasses(currentFileText).toString();
    linesAddedEl.textContent = '0';
    generatedCodeEl.textContent = 'Click “Generate Docstrings” to create documented code.';
  } catch {
    originalCodeEl.textContent = 'Could not read file contents.';
    resultsSection.classList.remove('d-none');
    statsSection.classList.remove('d-none');
  }
}

async function handleGenerate() {
  if (!currentFile) {
    showError('Please upload a file first.');
    return;
  }

  hideMessages();
  showLoading();

  const formData = new FormData();
  formData.append('file', currentFile);
  formData.append('style', docStyle.value);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.detail || 'Processing failed!');
      return;
    }

    currentResult = data;
    currentGeneratedText = data.documented_code || '';
    renderResults(data);
  } catch (error) {
    showError('Server error. Make sure backend is running on port 8000.');
  } finally {
    loading.classList.add('d-none');
  }
}

function renderResults(data) {
  resultsSection.classList.remove('d-none');
  statsSection.classList.remove('d-none');

  filenameEl.textContent = data.filename || currentFile?.name || '—';
  classesCountEl.textContent = countClasses(currentFileText).toString();
  functionsCountEl.textContent = (data.functions_found?.length || 0).toString();
  linesAddedEl.textContent = data.quality_check?.lines_added ?? '0';

  generatedCodeEl.textContent = data.documented_code || 'No documented code returned.';
  previewBtn.disabled = false;
  downloadBtn.disabled = !data.documented_code;
  downloadBtnTop.disabled = !data.documented_code;
  copyBtn.disabled = !data.documented_code;
  copyBtnTop.disabled = !data.documented_code;
}

function togglePreview() {
  if (!currentResult || !currentResult.functions_found) {
    showError('Generate docstrings first, then preview them.');
    return;
  }

  preview.classList.toggle('d-none');
  if (!preview.classList.contains('d-none')) {
    renderDocstrings();
  }
}

function renderDocstrings() {
  docstringsList.innerHTML = '';

  if (!currentResult?.functions_found?.length) {
    docstringsList.innerHTML = '<div class="text-muted">No functions found.</div>';
    return;
  }

  currentResult.functions_found.forEach(func => {
    const item = document.createElement('div');
    item.className = 'docstring-item';
    item.innerHTML = `
      <div class="docstring-name">${escapeHtml(func.function_name || 'Unnamed function')}</div>
      <div class="docstring-text">${escapeHtml(func.docstring || 'No docstring returned.')}</div>
    `;
    docstringsList.appendChild(item);
  });
}

async function handleCopy() {
  if (!currentGeneratedText) {
    showError('No generated code available to copy.');
    return;
  }

  try {
    await navigator.clipboard.writeText(currentGeneratedText);
    setCopyFeedback('Copied!');
  } catch {
    showError('Copy failed. Your browser may block clipboard access.');
  }
}

function handleDownload() {
  if (!currentGeneratedText) {
    showError('No documented code available!');
    return;
  }

  const extension = getFileExtension(currentFile?.name || '');
  const mime = getMimeType(extension);
  const baseName = currentFile?.name ? currentFile.name.replace(/\.[^/.]+$/, '') : 'documented_code';
  const blob = new Blob([currentGeneratedText], { type: mime });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = `documented_${baseName}${extension || '.txt'}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  setDownloadFeedback('Downloaded!');
}

function showLoading() {
  loading.classList.remove('d-none');
  resultsSection.classList.remove('d-none');
}

function showError(message) {
  hideMessages();
  errorDiv.textContent = message;
  errorDiv.classList.remove('d-none');
}

function hideMessages() {
  loading.classList.add('d-none');
  errorDiv.classList.add('d-none');
}

function resetUI() {
  preview.classList.add('d-none');
  downloadBtn.disabled = true;
  downloadBtnTop.disabled = true;
  copyBtn.disabled = true;
  copyBtnTop.disabled = true;
  previewBtn.disabled = true;
  generateBtn.disabled = !currentFile;
  generatedCodeEl.textContent = 'Generated code will appear here after processing.';
}

function setDownloadFeedback(text) {
  const original = downloadBtn.textContent;
  const originalTop = downloadBtnTop.textContent;
  downloadBtn.textContent = text;
  downloadBtnTop.textContent = text;

  setTimeout(() => {
    downloadBtn.textContent = original;
    downloadBtnTop.textContent = originalTop;
  }, 1800);
}

function setCopyFeedback(text) {
  const original = copyBtn.textContent;
  const originalTop = copyBtnTop.textContent;
  copyBtn.textContent = text;
  copyBtnTop.textContent = text;

  setTimeout(() => {
    copyBtn.textContent = original;
    copyBtnTop.textContent = originalTop;
  }, 1800);
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  return `${(kb / 1024).toFixed(1)} MB`;
}

function getFileExtension(name) {
  const match = name.match(/\.[^.]+$/);
  return match ? match[0].toLowerCase() : '';
}

function getMimeType(ext) {
  switch (ext) {
    case '.py': return 'text/x-python';
    case '.js': return 'text/javascript';
    case '.ts': return 'text/typescript';
    case '.java': return 'text/x-java-source';
    default: return 'text/plain';
  }
}

function countClasses(code) {
  if (!code) return 0;
  const patterns = [
    /\bclass\s+[A-Za-z_][A-Za-z0-9_]*\s*[:(]/g,
    /\bclass\s+[A-Za-z_][A-Za-z0-9_]*/g
  ];
  const seen = new Set();
  patterns.forEach(pattern => {
    const matches = code.match(pattern) || [];
    matches.forEach(m => seen.add(m));
  });
  return seen.size;
}

function escapeHtml(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}