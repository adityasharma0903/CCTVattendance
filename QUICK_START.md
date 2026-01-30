# ⚡ QUICK START GUIDE

## 🎯 Get Started in 5 Minutes

### **Windows Users**

1. **Install All Dependencies** (Run once)
   ```
   Double-click: install_all.bat
   Wait for completion (5-10 minutes)
   ```

2. **Start System** (3 terminals needed)
   
   **Terminal 1 - Backend API**
   ```
   Double-click: start_backend.bat
   Wait for: "Application startup complete"
   ```
   
   **Terminal 2 - Frontend Website**
   ```
   Double-click: start_frontend.bat
   Wait for: "Compiled successfully!"
   ```
   
   **Terminal 3 - Camera Service**
   ```
   Double-click: start_camera_service.bat
   Wait for: "Scheduler started successfully"
   ```

3. **Access System**
   - **Website**: Open `http://localhost:3000` in browser
   - **API Docs**: Open `http://localhost:8000/docs`
   - **Camera Feed**: Shows in Terminal 3

---

## 📝 Setup Order

### **Step 1: Add Master Data** (Using Website)

1. **Batches** (5 min)
   - Add your class batches
   - Example: CSE Batch A, B, C

2. **Teachers** (5 min)
   - Add all teachers
   - Include email/phone

3. **Subjects** (5 min)
   - Create subjects
   - Assign teachers

4. **Students** (10-15 min)
   - Add all students (roll number, name, batch)
   - **IMPORTANT**: Use setup script to add face encodings

5. **Cameras** (5 min)
   - Add cameras for each classroom
   - Configure IP addresses

6. **Timetable** (15 min)
   - Create day-wise schedule
   - Assign time periods, subjects, teachers

7. **Camera Schedule** (5 min)
   - Link cameras to timetable entries
   - Enable/disable as needed

---

## 🎬 First Run Test

### **Test Setup:**

1. **Create Test Batch**
   - Name: "Test Batch"
   - Semester: "1"

2. **Create Test Teacher**
   - Name: "Test Teacher"
   - Email: "test@college.edu"

3. **Create Test Subject**
   - Name: "Test Subject"
   - Code: "TST101"
   - Assign to Test Teacher

4. **Add Test Student**
   - Roll: "TEST001"
   - Name: "Test Student"
   - Batch: "Test Batch"
   - Image: Use your own photo

5. **Create Timetable**
   - Batch: "Test Batch"
   - Day: Today's day
   - Time: Current time to 1 hour from now
   - Subject: "Test Subject"
   - Teacher: "Test Teacher"

6. **Add Camera**
   - Name: "Test Camera"
   - Batch: "Test Batch"
   - Location: "Test Room"

7. **Assign Camera to Schedule**
   - Camera: "Test Camera"
   - Timetable: (the one created above)
   - Active: Yes

8. **View Attendance**
   - Go to "Attendance Report"
   - Select "Test Batch"
   - Camera should start recording in 30 seconds
   - Your face should be marked PRESENT automatically!

---

## 🔌 Ports Used

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| Frontend Website | 3000 | http://localhost:3000 |
| API Docs | 8000 | http://localhost:8000/docs |

---

## 📖 Important Commands

### **To Stop Services**
- Press `Ctrl + C` in each terminal

### **To Restart Services**
- Close terminal
- Double-click the start script again

### **To Check Backend Status**
```
Open: http://localhost:8000/
Should see: {"status": "running"}
```

### **To Check Student Data**
```
Open: http://localhost:8000/api/students
Should see JSON with all students
```

---

## ❌ Common Issues & Fixes

### **"Cannot find module" error in Frontend**
```
Solution:
1. Open Terminal 2 (Frontend terminal)
2. Press Ctrl+C
3. Run: npm install
4. Run: npm start
```

### **"Port 3000 already in use"**
```
Solution:
Close other React apps or:
1. Open Terminal 2
2. Press Ctrl+C
3. Run: npm start
```

### **"ModuleNotFoundError" in Backend**
```
Solution:
1. Open Terminal 1
2. Run: pip install -r requirements.txt
3. Run: python main.py
```

### **Camera shows empty/black frames**
```
Solution:
- Check lighting
- Check camera is accessible (try: Camera app)
- Use: cv2.VideoCapture(0) for default camera
```

### **Face not being detected**
```
Solution:
- Better lighting
- Clear frontal face image
- Lower SIMILARITY_THRESHOLD in attendance_service.py
```

---

## 📱 Test Attendance Marking

### **How to Verify It's Working:**

1. **Timetable Shows Active Period** ✅
   - Check: Terminal 3 logs
   - Should say: "Camera checking schedule..."

2. **Camera Detects Face** ✅
   - Check: Terminal 3 logs
   - Should say: "⏳ Processing face..."

3. **Attendance Marked** ✅
   - Check: Website "Attendance Report"
   - Should show: PRESENT with timestamp

4. **In JSON File** ✅
   - Check: `data/attendance.json`
   - Should have new entry

---

## 🎓 Example Workflow

### **Monday Morning, 9:00 AM**

```
1. Camera Service starts
   ↓
2. Checks: Is there a period now?
   (Looks at timetable and current time)
   ↓
3. YES - Data Structures class is scheduled 9:00-10:30
   ↓
4. Activates Camera
   ↓
5. Starts detecting faces
   ↓
6. Student enters class
   ↓
7. Face detected → Compared with database
   ↓
8. Match found → Aditya (Roll: 2410990250)
   ↓
9. Marked PRESENT
   ↓
10. Updates in website immediately
    (If you open Attendance Report, you see "Aditya - PRESENT")
    ↓
11. Class ends at 10:30
    ↓
12. Camera stops (period ended)
```

---

## 🚀 Going Live

Once you're comfortable:

1. **Register All Students**
   - Use setup script from iotproject/

2. **Create Full Timetable**
   - All periods for all days
   - All batches

3. **Add All Cameras**
   - One per classroom

4. **Assign Cameras to Schedule**
   - Link each camera to periods

5. **Run 24/7**
   - Keep all 3 services running during class hours

---

## 💡 Pro Tips

✅ **Best Practices:**
- Good lighting for face detection
- Clear frontal face photos for students
- Keep camera angle fixed
- Test with small batch first
- Backup `data/` folder regularly

❌ **Avoid:**
- Sunlight directly on camera
- Blurry student photos
- Changing camera angle during class
- Running without API running
- Close windows for warmth (camera needs cool)

---

## 📞 Support Commands

### **Check if Backend is Working**
```
curl http://localhost:8000/
```

### **Check API Health**
```
curl http://localhost:8000/api/dashboard/summary
```

### **View All Students (from API)**
```
http://localhost:8000/api/students
(Copy-paste in browser)
```

### **View All Attendance**
```
http://localhost:8000/api/attendance
```

---

## 🎉 Success Checklist

- [ ] All 3 services running without errors
- [ ] Website loads at localhost:3000
- [ ] Can add students/batches/teachers
- [ ] Can create timetable
- [ ] Can see live camera feed in Terminal 3
- [ ] Attendance being marked in real-time
- [ ] Can view attendance report
- [ ] JSON files being updated

---

**Ready to start? Run `install_all.bat` now! 🚀**

Questions? Check `README.md` for detailed documentation.
