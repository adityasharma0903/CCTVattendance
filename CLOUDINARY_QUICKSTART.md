# 🚀 Quick Start - Cloudinary Setup

## 30-Second Setup

### 1. Get Cloudinary Credentials (2 minutes)
1. Open: https://cloudinary.com/users/register/free
2. Sign up (free forever)
3. Copy your credentials from Dashboard:
   - Cloud Name
   - API Key
   - API Secret

### 2. Configure .env File (1 minute)
```bash
# Copy example file
copy .env.example .env

# Edit .env and add your Cloudinary credentials
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Keep your MongoDB URL as is
MONGODB_URL=mongodb+srv://...
```

### 3. Install Dependencies (2 minutes)
```bash
# Backend
cd backend
pip install -r requirements.txt

# Camera Service
cd ..\camera_service
pip install -r requirements.txt
```

### 4. Test Configuration (30 seconds)
```bash
cd backend
python cloudinary_utils.py
```

Expected output:
```
✅ Cloudinary is properly configured!
```

### 5. Start Your System
```bash
# Start backend
.\start_backend_venv.bat

# Start frontend (new terminal)
.\start_frontend.bat
```

### 6. Add Your First Student
1. Open http://localhost:3000
2. Go to "Student Management"
3. Click "+ Add New Student"
4. Fill form and upload a clear face photo
5. Click "Register Student"

**Done! 🎉** Your images are now on Cloudinary!

---

## Migrate Existing Images (Optional)

If you already have students with local images:

```bash
python migrate_to_cloudinary.py
```

This will:
- ✅ Upload all local images to Cloudinary
- ✅ Update database with cloud URLs
- ✅ Keep backups of your data

---

## Troubleshooting

### "Cloudinary credentials missing"
→ Check your `.env` file has all three values

### "Face detection failed"  
→ Use clear, frontal face photo with good lighting

### Need help?
→ Read [CLOUDINARY_SETUP.md](CLOUDINARY_SETUP.md) for detailed guide

---

**You're all set! Enjoy cloud-powered face recognition! ☁️✨**
