# QR Code Generator - Professional Edition

A modern, professional QR Code generator web application with history tracking and download functionality.

## Features

- ✨ **Professional UI** - Enterprise-grade design with modern aesthetics
- 📱 **Side-by-side Layout** - Input on left, QR code display on right
- 💾 **History Tracking** - All generated QR codes are automatically saved
- 📥 **Download Option** - Download individual QR codes
- 🔍 **Search Functionality** - Filter history by content or date
- 🐳 **Docker Support** - Easy deployment with Docker Compose

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Ayman-ilias/qr_code_generator.git
cd qr_code_generator
```

2. Start the service:
```bash
docker compose up -d
```

3. Access the application:
```
http://localhost:3997
```

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

## Configuration

### Port Configuration

The default port is **3997**. To change it, edit `docker-compose.yml`:

```yaml
ports:
  - "YOUR_PORT:5000"
```

## Usage

1. **Generate QR Code**:
   - Enter text or JSON data in the left panel
   - Click "Generate QR Code"
   - View the QR code on the right panel
   - Click "Download QR Code" to save it

2. **View History**:
   - Click the "History" tab
   - Browse all previously generated QR codes
   - Use the search box to filter results
   - Download any QR code from history

## Technology Stack

- **Backend**: Flask (Python)
- **QR Generation**: qrcode library with Pillow
- **Frontend**: HTML5, CSS3, JavaScript
- **Fonts**: Google Inter
- **Containerization**: Docker

## File Structure

```
qr_code_generator/
├── app.py                  # Main Flask application
├── generate_qr.py          # Original QR generator script
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
├── qr_history/            # Generated QR codes storage
│   └── metadata.json      # QR code metadata
└── README.md              # This file
```

## Features in Detail

### Professional Design
- Navy blue color scheme
- Google Inter font family
- Refined shadows and spacing
- Responsive design for all devices

### History Management
- Stores last 100 QR codes
- Metadata tracking (timestamp, content preview)
- Persistent storage across container restarts
- Search and filter capabilities

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/generate` | POST | Generate new QR code |
| `/api/history` | GET | Get QR code history |
| `/api/download/<filename>` | GET | Download specific QR code |
| `/health` | GET | Health check endpoint |

## Development

To modify the application:

1. Edit `app.py` for backend changes
2. Rebuild the Docker container:
```bash
docker compose down
docker compose up --build -d
```

## License

MIT License - Feel free to use this project for any purpose.

## Author

Ayman Ilias

## Acknowledgments

- Flask framework
- qrcode library
- Google Fonts (Inter)
