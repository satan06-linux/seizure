# 🎨 Frontend Setup Guide - React + Vite

## Overview

Modern, professional frontend with stunning UI/UX featuring:
- ⚡ React 18 + Vite for blazing fast development
- 🎨 Tailwind CSS for beautiful, responsive design
- ✨ Framer Motion for smooth animations
- 📊 Recharts for data visualization
- 🎯 Lucide React for modern icons
- 🔥 React Hot Toast for notifications

---

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start Backend Server

```bash
# From backend directory
python api.py
```

Backend will run on: `http://localhost:5000`

### 4. Start Frontend Development Server

```bash
# From frontend directory
npm run dev
```

Frontend will run on: `http://localhost:3000`

---

## 📁 Project Structure

```
seizureguard_ai/
├── backend/
│   ├── api.py                 # Flask REST API
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx    # Navigation component
│   │   ├── pages/
│   │   │   ├── Home.jsx      # Landing page
│   │   │   ├── Upload.jsx    # File upload & analysis
│   │   │   ├── Symptoms.jsx  # Symptom checker
│   │   │   ├── Chat.jsx      # AI chatbot
│   │   │   └── Doctors.jsx   # Doctor finder
│   │   ├── App.jsx           # Main app component
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── public/               # Static assets
│   ├── index.html            # HTML template
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── tailwind.config.js    # Tailwind configuration
│   └── postcss.config.js     # PostCSS configuration
│
└── modules/                   # Shared AI modules
```

---

## 🎨 Features

### Home Page
- Animated hero section with gradient text
- Feature cards with hover effects
- Statistics dashboard
- How it works section
- Call-to-action sections

### Upload Page
- Drag & drop file upload
- Support for CSV, PDF, Image, EDF
- Real-time file processing
- Beautiful result visualization
- Probability distribution charts

### Symptoms Page
- Text area for symptom description
- AI-powered risk assessment
- Detected symptoms display
- Personalized recommendations
- Risk level indicators

### Chat Page
- Real-time AI chatbot
- Message history
- Quick question buttons
- Typing indicators
- Smooth animations

### Doctors Page
- Advanced filtering (location, specialization, emergency)
- Doctor cards with ratings
- Contact information
- Experience display
- Emergency care indicators

---

## 🛠️ Development

### Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create `.env` file in frontend directory:

```env
VITE_API_URL=http://localhost:5000
```

---

## 🎨 Customization

### Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### Animations

Edit `tailwind.config.js` for custom animations:

```javascript
animation: {
  'custom': 'custom 2s ease-in-out infinite',
}
```

---

## 📦 Production Build

### Build Frontend

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

### Serve with Backend

Update Flask to serve static files:

```python
from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(f"../frontend/dist/{path}"):
        return send_from_directory('../frontend/dist', path)
    return send_from_directory('../frontend/dist', 'index.html')
```

---

## 🚀 Deployment

### Option 1: Vercel (Frontend) + Heroku (Backend)

**Frontend (Vercel):**
```bash
cd frontend
vercel
```

**Backend (Heroku):**
```bash
cd backend
heroku create seizureguard-api
git push heroku main
```

### Option 2: Docker

Create `Dockerfile`:

```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "backend/api.py"]
```

```dockerfile
# Frontend
FROM node:18-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Option 3: Single Server

Build frontend and serve with Flask:

```bash
cd frontend
npm run build
cd ../backend
python api.py
```

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
npm run dev -- --port 3001
```

### CORS Issues

Ensure Flask-CORS is installed:

```bash
pip install flask-cors
```

### Module Not Found

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 🎯 API Endpoints

### Health Check
```
GET /api/health
```

### Upload File
```
POST /api/upload
Content-Type: multipart/form-data
Body: { file: File }
```

### Analyze Symptoms
```
POST /api/symptoms/analyze
Body: { symptoms: string }
```

### Chat
```
POST /api/chat
Body: { message: string }
```

### Get Doctors
```
GET /api/doctors?location=&specialization=&emergency=true
```

---

## 📱 Responsive Design

The UI is fully responsive:
- Mobile: Single column layout
- Tablet: 2-column grid
- Desktop: Multi-column with sidebars

---

## ✨ UI/UX Features

- Glass morphism effects
- Gradient backgrounds
- Smooth page transitions
- Hover animations
- Loading states
- Toast notifications
- Skeleton loaders
- Error boundaries

---

## 🎨 Design System

### Typography
- Headings: Bold, gradient text
- Body: Gray-700
- Links: Blue-600

### Spacing
- Sections: 8rem (space-y-20)
- Cards: 2rem padding
- Elements: 1rem gap

### Shadows
- Cards: shadow-xl
- Hover: shadow-2xl
- Buttons: shadow-lg

---

## 🔐 Security

- CORS configured
- Input validation
- File type checking
- Size limits
- XSS protection

---

## 📊 Performance

- Code splitting
- Lazy loading
- Image optimization
- Minification
- Gzip compression

---

## 🎉 You're Ready!

Your modern frontend is ready to use!

**Start developing:**
```bash
cd frontend && npm run dev
```

**Access at:** http://localhost:3000

---

*Built with ❤️ using React, Vite, and Tailwind CSS*
