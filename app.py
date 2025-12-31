from flask import Flask, request, send_file, render_template_string, jsonify, send_from_directory
import qrcode
import json
import os
import io
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Directory for storing QR codes
QR_HISTORY_DIR = os.path.join(os.path.dirname(__file__), 'qr_history')
os.makedirs(QR_HISTORY_DIR, exist_ok=True)

# Metadata file
METADATA_FILE = os.path.join(QR_HISTORY_DIR, 'metadata.json')

def load_metadata():
    """Load QR code metadata"""
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_metadata(metadata):
    """Save QR code metadata"""
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator - Professional Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary-color: #1e3a8a;
            --primary-light: #3b82f6;
            --primary-dark: #1e40af;
            --secondary-color: #0891b2;
            --accent-color: #06b6d4;
            --success-color: #10b981;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --text-light: #9ca3af;
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-tertiary: #f3f4f6;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #e0e7ff 0%, #f0f9ff 100%);
            min-height: 100vh;
            color: var(--text-primary);
        }
        
        /* Professional Header */
        .header {
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
            font-weight: 700;
            box-shadow: var(--shadow-md);
        }
        
        .brand-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }
        
        .brand-text p {
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-weight: 400;
        }
        
        .nav-tabs {
            display: flex;
            gap: 0.5rem;
        }
        
        .tab-btn {
            padding: 0.625rem 1.5rem;
            background: transparent;
            color: var(--text-secondary);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9375rem;
            font-weight: 500;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .tab-btn:hover {
            background: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .tab-btn.active {
            background: var(--primary-color);
            color: white;
            box-shadow: var(--shadow-sm);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .container {
            background: var(--bg-primary);
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            padding: 2.5rem;
            max-width: 1400px;
            width: 100%;
            margin: 0 auto 2rem;
            border: 1px solid var(--border-color);
        }
        
        .page-title {
            color: var(--text-primary);
            font-size: 1.875rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .page-subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            font-weight: 400;
            margin-bottom: 2rem;
        }
        
        .two-column-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5rem;
        }
        
        .panel {
            display: flex;
            flex-direction: column;
        }
        
        .panel-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--bg-tertiary);
        }
        
        .panel-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent-color) 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            box-shadow: var(--shadow-sm);
        }
        
        .panel-title {
            color: var(--text-primary);
            font-size: 1.25rem;
            font-weight: 600;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
            font-weight: 500;
            font-size: 0.9375rem;
        }
        
        textarea {
            width: 100%;
            padding: 1rem;
            border: 2px solid var(--border-color);
            border-radius: 10px;
            font-size: 0.9375rem;
            font-family: 'Courier New', 'Monaco', monospace;
            resize: vertical;
            transition: all 0.2s ease;
            min-height: 420px;
            background: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        textarea:focus {
            outline: none;
            border-color: var(--primary-light);
            background: var(--bg-primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .btn {
            padding: 0.875rem 1.75rem;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 0.9375rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
            box-shadow: var(--shadow-md);
            letter-spacing: 0.3px;
        }
        
        .btn-full {
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-download {
            background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%);
            margin-top: 1.5rem;
        }
        
        .qr-display-area {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 420px;
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 2rem;
            border: 2px dashed var(--border-color);
            transition: all 0.3s ease;
        }
        
        .qr-display-area.has-qr {
            border-style: solid;
            border-color: var(--primary-light);
            background: var(--bg-primary);
        }
        
        .qr-placeholder {
            color: var(--text-light);
            text-align: center;
            font-size: 1rem;
        }
        
        .qr-placeholder-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        #qrImage {
            max-width: 100%;
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            background: white;
            padding: 1.5rem;
        }
        
        .info-banner {
            background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
            padding: 1rem 1.25rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
            border-left: 4px solid var(--primary-light);
            display: flex;
            align-items: start;
            gap: 0.75rem;
        }
        
        .info-banner-icon {
            font-size: 1.25rem;
            margin-top: 0.125rem;
        }
        
        .error {
            background: #fee2e2;
            padding: 1rem 1.25rem;
            border-radius: 10px;
            margin-top: 1rem;
            color: #991b1b;
            border-left: 4px solid #dc2626;
            display: none;
        }
        
        .history-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .history-item {
            background: var(--bg-primary);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: all 0.2s ease;
            border: 1px solid var(--border-color);
        }
        
        .history-item:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary-light);
        }
        
        .history-item img {
            width: 100%;
            border-radius: 8px;
            background: var(--bg-secondary);
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .history-meta {
            font-size: 0.8125rem;
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
            font-weight: 500;
        }
        
        .history-data {
            background: var(--bg-secondary);
            padding: 0.875rem;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.8125rem;
            max-height: 100px;
            overflow-y: auto;
            margin-bottom: 1rem;
            word-break: break-all;
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        
        .search-box {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 2px solid var(--border-color);
            border-radius: 10px;
            font-size: 0.9375rem;
            margin-bottom: 1.5rem;
            background: var(--bg-secondary);
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }
        
        .search-box:focus {
            outline: none;
            border-color: var(--primary-light);
            background: var(--bg-primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .no-history {
            text-align: center;
            padding: 4rem 1.5rem;
            color: var(--text-light);
            font-size: 1.125rem;
        }
        
        @media (max-width: 968px) {
            .header-content {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
            
            .logo-section {
                flex-direction: column;
            }
            
            .two-column-layout {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            textarea {
                min-height: 250px;
            }
            
            .qr-display-area {
                min-height: 320px;
            }
            
            .container {
                padding: 1.5rem;
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in {
            animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-tertiary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--text-light);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">QR</div>
                <div class="brand-text">
                    <h1>QR Code Generator</h1>
                    <p>Professional Edition</p>
                </div>
            </div>
            <nav class="nav-tabs">
                <button class="tab-btn active" onclick="switchTab('generate')">Generate</button>
                <button class="tab-btn" onclick="switchTab('history')">History</button>
            </nav>
        </div>
    </header>

    <div id="generateTab" class="tab-content active">
        <div class="container">
            <div class="info-banner">
                <span class="info-banner-icon">ℹ️</span>
                <div>
                    <strong>Quick Start:</strong> Enter your text or JSON data in the left panel and click Generate to create your QR code instantly. All generated codes are automatically saved to your history.
                </div>
            </div>
            
            <div class="two-column-layout">
                <!-- Left Panel: Input -->
                <div class="panel">
                    <div class="panel-header">
                        <div class="panel-icon">📝</div>
                        <h2 class="panel-title">Input Data</h2>
                    </div>
                    <form id="qrForm">
                        <div class="form-group">
                            <label for="qrData">Enter Text or JSON</label>
                            <textarea id="qrData" name="data" placeholder='Enter plain text or valid JSON:
{
  "type": "vCard",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890"
}' required></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-full">Generate QR Code</button>
                    </form>
                    
                    <div id="error" class="error"></div>
                </div>
                
                <!-- Right Panel: QR Code Display -->
                <div class="panel">
                    <div class="panel-header">
                        <div class="panel-icon">📱</div>
                        <h2 class="panel-title">QR Code Output</h2>
                    </div>
                    <div class="qr-display-area" id="qrDisplayArea">
                        <div class="qr-placeholder" id="qrPlaceholder">
                            <div class="qr-placeholder-icon">📱</div>
                            <div style="font-weight: 500;">Your QR code will appear here</div>
                            <div style="font-size: 0.875rem; margin-top: 0.5rem; opacity: 0.7;">Fill in the input and click Generate</div>
                        </div>
                        <img id="qrImage" src="" alt="QR Code" style="display: none;">
                    </div>
                    <button id="downloadBtn" class="btn btn-download btn-full" style="display: none;">
                        <span style="margin-right: 0.5rem;">⬇</span> Download QR Code
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="historyTab" class="tab-content">
        <div class="container">
            <h2 class="page-title">QR Code History</h2>
            <p class="page-subtitle">View and download all your previously generated QR codes</p>
            
            <input type="text" id="searchBox" class="search-box" placeholder="🔍 Search by content or date..." onkeyup="filterHistory()">
            
            <div id="historyGrid" class="history-grid">
                <!-- History items will be loaded here -->
            </div>
        </div>
    </div>
    
    <script>
        let currentQrFilename = '';
        let historyData = [];
        
        function switchTab(tab) {
            // Update tab buttons
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            if (tab === 'generate') {
                document.getElementById('generateTab').classList.add('active');
            } else if (tab === 'history') {
                document.getElementById('historyTab').classList.add('active');
                loadHistory();
            }
        }
        
        document.getElementById('qrForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const data = document.getElementById('qrData').value;
            const errorDiv = document.getElementById('error');
            const qrPlaceholder = document.getElementById('qrPlaceholder');
            const qrImage = document.getElementById('qrImage');
            const downloadBtn = document.getElementById('downloadBtn');
            const qrDisplayArea = document.getElementById('qrDisplayArea');
            
            errorDiv.style.display = 'none';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ data: data })
                });
                
                if (response.ok) {
                    const result = await response.json();
                    currentQrFilename = result.filename;
                    
                    // Hide placeholder and show QR code
                    qrPlaceholder.style.display = 'none';
                    qrImage.src = '/qr_history/' + result.filename;
                    qrImage.style.display = 'block';
                    qrImage.classList.add('fade-in');
                    downloadBtn.style.display = 'block';
                    qrDisplayArea.classList.add('has-qr');
                } else {
                    const error = await response.json();
                    errorDiv.textContent = '❌ Error: ' + (error.error || 'Failed to generate QR code');
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = '❌ Error: ' + error.message;
                errorDiv.style.display = 'block';
            }
        });
        
        document.getElementById('downloadBtn').addEventListener('click', function() {
            if (currentQrFilename) {
                window.location.href = '/api/download/' + currentQrFilename;
            }
        });
        
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                historyData = data;
                displayHistory(data);
            } catch (error) {
                console.error('Failed to load history:', error);
            }
        }
        
        function displayHistory(items) {
            const grid = document.getElementById('historyGrid');
            
            if (items.length === 0) {
                grid.innerHTML = '<div class="no-history">📭 No QR codes generated yet</div>';
                return;
            }
            
            grid.innerHTML = items.map(item => `
                <div class="history-item fade-in">
                    <img src="/qr_history/${item.filename}" alt="QR Code">
                    <div class="history-meta">
                        📅 ${new Date(item.timestamp).toLocaleString()}
                    </div>
                    <div class="history-data">${item.preview}</div>
                    <button class="btn btn-download btn-full" onclick="downloadQR('${item.filename}')">
                        📥 Download
                    </button>
                </div>
            `).join('');
        }
        
        function filterHistory() {
            const search = document.getElementById('searchBox').value.toLowerCase();
            const filtered = historyData.filter(item => 
                item.preview.toLowerCase().includes(search) ||
                new Date(item.timestamp).toLocaleString().toLowerCase().includes(search)
            );
            displayHistory(filtered);
        }
        
        function downloadQR(filename) {
            window.location.href = '/api/download/' + filename;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Render the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def generate_qr():
    """API endpoint to generate QR code and save it"""
    try:
        json_data = request.get_json()
        
        if not json_data or 'data' not in json_data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = json_data['data']
        
        # Try to parse as JSON, if it fails, treat as plain text
        try:
            parsed_data = json.loads(data)
            qr_data = json.dumps(parsed_data, ensure_ascii=False)
        except json.JSONDecodeError:
            qr_data = data
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create an image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Generate filename with timestamp
        timestamp = datetime.now()
        filename = f"qr_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.png"
        filepath = os.path.join(QR_HISTORY_DIR, filename)
        
        # Save the image
        img.save(filepath)
        
        # Update metadata
        metadata = load_metadata()
        metadata.insert(0, {  # Insert at beginning for reverse chronological order
            'filename': filename,
            'timestamp': timestamp.isoformat(),
            'preview': qr_data[:200] if len(qr_data) > 200 else qr_data,
            'full_data': qr_data
        })
        
        # Keep only last 100 items
        metadata = metadata[:100]
        save_metadata(metadata)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'timestamp': timestamp.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get QR code history"""
    try:
        metadata = load_metadata()
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_qr(filename):
    """Download a specific QR code"""
    try:
        return send_from_directory(QR_HISTORY_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/qr_history/<filename>')
def serve_qr(filename):
    """Serve QR code images"""
    try:
        return send_from_directory(QR_HISTORY_DIR, filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/health')
def health():
    """Health check endpoint"""
    metadata = load_metadata()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'QR Code Generator',
        'total_qr_codes': len(metadata)
    })

if __name__ == '__main__':
    # Run on all interfaces so it's accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=False)
