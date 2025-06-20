// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    loadFiles();
    setupEventListeners();
});

function setupEventListeners() {
    // Upload form
    document.getElementById('uploadForm').addEventListener('submit', handleUpload);

    // File input change
    document.getElementById('fileInput').addEventListener('change', updateFileLabel);

    // Logout button (assuming you have one with ID 'logoutButton')
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }
}

function updateFileLabel() {
    const fileInput = document.getElementById('fileInput');
    const label = document.querySelector('.file-label span');

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        label.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
    } else {
        label.textContent = 'Choose File';
    }
}

async function handleUpload(e) {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    const statusDiv = document.getElementById('uploadStatus');

    if (!fileInput.files[0]) {
        showStatus('Please select a file', 'error');
        return;
    }

    formData.append('file', fileInput.files[0]);

    try {
        statusDiv.textContent = 'Encrypting and uploading...';
        statusDiv.className = 'status'; // You might want a specific class for "uploading" state

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showStatus(`✅ ${result.message}`, 'success');
            fileInput.value = ''; // Clear the file input
            updateFileLabel(); // Reset the file label
            loadFiles(); // Refresh file list
        } else {
            showStatus(`❌ ${result.error}`, 'error');
        }

    } catch (error) {
        showStatus('❌ Upload failed', 'error');
        console.error('Upload error:', error);
    }
}

async function loadFiles() {
    const filesList = document.getElementById('filesList');
    // Clear previous content and show a loading indicator
    filesList.innerHTML = '<div class="loading">Loading files...</div>';

    try {
        const response = await fetch('/files');

        if (!response.ok) {
            if (response.status === 401) {
                // Redirect to login if unauthenticated
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to load files');
        }

        const files = await response.json();

        if (files.length === 0) {
            filesList.innerHTML = '<div class="loading">No files uploaded yet</div>';
            return;
        }

        filesList.innerHTML = files.map(file => `
            <div class="file-item">
                <div class="file-info">
                    <h3>📄 ${escapeHtml(file.name)}</h3>
                    <div class="file-meta">
                        Size: ${formatFileSize(file.size)} |
                        Uploaded: ${new Date(file.uploadDate).toLocaleString()}
                    </div>
                </div>
                <div class="file-actions">
                    <button onclick="downloadFile('${file.id}')" class="btn btn-primary">
                        ⬇️ Download
                    </button>
                    <button onclick="deleteFile('${file.id}')" class="btn btn-danger">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `).join('');

    } catch (error) {
        filesList.innerHTML = '<div class="loading">Error loading files</div>';
        console.error('Load files error:', error);
        showStatus('❌ Error loading files', 'error');
    }
}

async function downloadFile(fileId) {
    try {
        const response = await fetch(`/download/${fileId}`);

        if (!response.ok) {
            const error = await response.json();
            showStatus(`❌ ${error.error}`, 'error');
            return;
        }

        // Get filename from Content-Disposition header
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'downloaded-file';

        if (contentDisposition) {
            const matches = contentDisposition.match(/filename="([^"]+)"/);
            if (matches && matches[1]) {
                filename = matches[1];
            }
        }

        // Create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        showStatus('✅ File downloaded successfully', 'success');

    } catch (error) {
        showStatus('❌ Download failed', 'error');
        console.error('Download error:', error);
    }
}

async function deleteFile(fileId) {
    // IMPORTANT: Do NOT use `confirm()` in production code running in an iframe.
    // Replace this with a custom modal or message box for user confirmation.
    if (!confirm('Are you sure you want to delete this file? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`/files/${fileId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok) {
            showStatus('✅ File deleted successfully', 'success');
            loadFiles(); // Refresh file list
        } else {
            showStatus(`❌ ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus('❌ Deletion failed', 'error');
        console.error('Delete error:', error);
    }
}

async function handleLogout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST' // Or 'GET', depending on your backend
        });

        if (response.ok) {
            window.location.href = '/login'; // Redirect to login page
        } else {
            const result = await response.json();
            showStatus(`❌ Logout failed: ${result.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showStatus('❌ Logout failed', 'error');
        console.error('Logout error:', error);
    }
}

// --- Helper Functions ---

/**
 * Formats file size into a human-readable string (e.g., 1.2 MB).
 * @param {number} bytes The size of the file in bytes.
 * @returns {string} The formatted file size.
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Displays a status message to the user.
 * Assumes there's an HTML element with id 'uploadStatus' to display messages.
 * @param {string} message The message to display.
 * @param {'success' | 'error' | 'info'} type The type of message (for styling).
 */
function showStatus(message, type) {
    const statusDiv = document.getElementById('uploadStatus'); // Reusing uploadStatus for general messages
    if (statusDiv) {
        statusDiv.textContent = message;
        statusDiv.className = `status ${type}`; // Apply classes for styling
        // Optionally, hide the message after a few seconds
        setTimeout(() => {
            statusDiv.textContent = '';
            statusDiv.className = 'status';
        }, 5000); // Message disappears after 5 seconds
    } else {
        console.warn('Status div (id="uploadStatus") not found. Message:', message);
    }
}

/**
 * Escapes HTML entities to prevent XSS attacks.
 * @param {string} text The string to escape.
 * @returns {string} The escaped string.
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}
