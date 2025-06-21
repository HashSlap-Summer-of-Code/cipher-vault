const express = require('express');
const multer = require('multer');
const session = require('express-session');
const path = require('path');
const fs = require('fs').promises;
const crypto = require('./config/crypto');
const auth = require('./middleware/auth');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Ensure uploads directory exists
const uploadsDir = path.join(__dirname, 'uploads');
fs.mkdir(uploadsDir, { recursive: true }).catch(console.error);

// Session configuration
app.use(session({
    secret: process.env.SESSION_SECRET || 'vault-secret-key-change-in-production',
    resave: false,
    saveUninitialized: false,
    cookie: { 
        secure: false, // Set to true in production with HTTPS
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
}));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// File upload configuration
const upload = multer({
    dest: 'temp/',
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB limit
    },
    fileFilter: (req, file, cb) => {
        // Basic file type validation
        const allowedTypes = /jpeg|jpg|png|gif|pdf|txt|doc|docx|zip/;
        const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = allowedTypes.test(file.mimetype);
        
        if (mimetype && extname) {
            return cb(null, true);
        } else {
            cb(new Error('Invalid file type'));
        }
    }
});

// In-memory storage for file metadata and users
const fileMetadata = new Map();
const users = new Map([
    ['admin', { password: '$2b$10$K5Z1qKz.example.hash', files: [] }], // Password: 'admin123'
    ['user', { password: '$2b$10$K5Z1qKz.example.hash', files: [] }]   // Password: 'user123'
]);

// Routes
app.get('/', (req, res) => {
    if (!req.session.userId) {
        return res.redirect('/login');
    }
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post('/login', auth.login);
app.post('/logout', auth.logout);

// Upload route with authentication
app.post('/upload', auth.authenticate, upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const fileId = uuidv4();
        const originalName = req.file.originalname;
        const tempPath = req.file.path;
        
        // Read file content
        const fileBuffer = await fs.readFile(tempPath);
        
        // Encrypt file content
        const encryptedData = crypto.encrypt(fileBuffer);
        
        // Generate encrypted filename
        const encryptedFilename = crypto.hashString(fileId) + '.enc';
        const encryptedPath = path.join(uploadsDir, encryptedFilename);
        
        // Save encrypted file
        await fs.writeFile(encryptedPath, JSON.stringify(encryptedData));
        
        // Store metadata
        fileMetadata.set(fileId, {
            id: fileId,
            originalName,
            encryptedFilename,
            uploadDate: new Date().toISOString(),
            userId: req.session.userId,
            size: fileBuffer.length
        });
        
        // Add to user's file list
        users.get(req.session.userId).files.push(fileId);
        
        // Clean up temp file
        await fs.unlink(tempPath);
        
        res.json({ 
            success: true, 
            fileId, 
            message: 'File uploaded and encrypted successfully' 
        });
        
    } catch (error) {
        console.error('Upload error:', error);
        res.status(500).json({ error: 'Upload failed' });
    }
});

// Download route with authentication
app.get('/download/:id', auth.authenticate, async (req, res) => {
    try {
        const fileId = req.params.id;
        const metadata = fileMetadata.get(fileId);
        
        if (!metadata) {
            return res.status(404).json({ error: 'File not found' });
        }
        
        // Check if user owns this file
        if (metadata.userId !== req.session.userId) {
            return res.status(403).json({ error: 'Access denied' });
        }
        
        const encryptedPath = path.join(uploadsDir, metadata.encryptedFilename);
        
        // Read and decrypt file
        const encryptedData = JSON.parse(await fs.readFile(encryptedPath, 'utf8'));
        const decryptedBuffer = crypto.decrypt(encryptedData);
        
        // Set appropriate headers
        res.setHeader('Content-Disposition', `attachment; filename="${metadata.originalName}"`);
        res.setHeader('Content-Type', 'application/octet-stream');
        
        res.send(decryptedBuffer);
        
    } catch (error) {
        console.error('Download error:', error);
        res.status(500).json({ error: 'Download failed' });
    }
});

// List user's files
app.get('/files', auth.authenticate, (req, res) => {
    const userFiles = users.get(req.session.userId).files.map(fileId => {
        const metadata = fileMetadata.get(fileId);
        return metadata ? {
            id: metadata.id,
            name: metadata.originalName,
            size: metadata.size,
            uploadDate: metadata.uploadDate
        } : null;
    }).filter(Boolean);
    
    res.json(userFiles);
});

// Delete file
app.delete('/files/:id', auth.authenticate, async (req, res) => {
    try {
        const fileId = req.params.id;
        const metadata = fileMetadata.get(fileId);
        
        if (!metadata || metadata.userId !== req.session.userId) {
            return res.status(404).json({ error: 'File not found' });
        }
        
        // Delete encrypted file
        const encryptedPath = path.join(uploadsDir, metadata.encryptedFilename);
        await fs.unlink(encryptedPath);
        
        // Remove from metadata
        fileMetadata.delete(fileId);
        
        // Remove from user's file list
        const userFiles = users.get(req.session.userId).files;
        const index = userFiles.indexOf(fileId);
        if (index > -1) {
            userFiles.splice(index, 1);
        }
        
        res.json({ success: true, message: 'File deleted successfully' });
        
    } catch (error) {
        console.error('Delete error:', error);
        res.status(500).json({ error: 'Delete failed' });
    }
});

app.listen(PORT, () => {
    console.log(`🔒 Secure File Vault running on http://localhost:${PORT}`);
    console.log(`📁 Files will be stored in: ${uploadsDir}`);
    console.log(`🔑 Default login: admin/admin123 or user/user123`);
});