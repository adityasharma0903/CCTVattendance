# ✅ Installation & Setup Checklist

## 📋 Pre-Setup Checklist

- [ ] You have the entire project folder
- [ ] You have Python 3.8+ installed
- [ ] You have Node.js installed (for npm)
- [ ] You have a webcam or camera connected
- [ ] You have student photos in `iotproject/student_images/`
- [ ] You have read `START_HERE.md`

---

## 🔧 Installation Phase (10 minutes)

- [ ] Navigate to project root folder
- [ ] Run: `install_all.bat`
  - [ ] Backend dependencies installing
  - [ ] Camera service dependencies installing
  - [ ] Frontend dependencies installing
  - [ ] All completed successfully
- [ ] Wait for prompt to continue

---

## 🚀 Startup Phase (5 minutes)

### Terminal 1 - Backend API
- [ ] Open new command prompt
- [ ] Run: `start_backend.bat`
- [ ] Wait for: "Application startup complete"
- [ ] Keep terminal open

### Terminal 2 - Frontend Website
- [ ] Open new command prompt
- [ ] Run: `start_frontend.bat`
- [ ] Wait for: "Compiled successfully!"
- [ ] Keep terminal open

### Terminal 3 - Camera Service
- [ ] Open new command prompt
- [ ] Run: `start_camera_service.bat`
- [ ] Wait for: "Scheduler started successfully"
- [ ] Keep terminal open

### Verification
- [ ] All 3 terminals show success messages
- [ ] No error messages in any terminal
- [ ] All still running (not exited)

---

## 🌐 Web Access Verification (2 minutes)

- [ ] Open browser
- [ ] Visit: http://localhost:3000
  - [ ] Website loads
  - [ ] See purple header
  - [ ] See navigation menu on left
  - [ ] See "Dashboard" page
- [ ] Visit: http://localhost:8000
  - [ ] See: {"status": "running", ...}
- [ ] Visit: http://localhost:8000/docs
  - [ ] See Swagger API documentation
  - [ ] See all endpoints listed

---

## 📊 Setup Data Entry (20 minutes)

### 1. Add Batches
- [ ] Click: "📚 Batches" in navigation
- [ ] Click: "+ Add New Batch"
- [ ] Enter:
  - [ ] Batch ID: `B001`
  - [ ] Batch Name: `CSE Batch A`
  - [ ] Semester: `4`
- [ ] Click: "Save Batch"
- [ ] Verify: Batch appears in table

### 2. Add Teachers
- [ ] Click: "👨‍🏫 Teachers" in navigation
- [ ] Click: "+ Add New Teacher"
- [ ] Enter:
  - [ ] Teacher ID: `T001`
  - [ ] Name: `Dr. Sharma`
  - [ ] Email: `sharma@college.edu`
  - [ ] Phone: `9999999999`
- [ ] Click: "Save Teacher"
- [ ] Repeat for at least 2 more teachers

### 3. Add Subjects
- [ ] Click: "📖 Subjects" in navigation
- [ ] Click: "+ Add New Subject"
- [ ] Enter:
  - [ ] Subject ID: `S001`
  - [ ] Subject Name: `Data Structures`
  - [ ] Subject Code: `CS201`
  - [ ] Teacher: `Dr. Sharma`
- [ ] Click: "Save Subject"
- [ ] Add 2 more subjects

### 4. Add Camera
- [ ] Click: "🎥 Cameras" in navigation
- [ ] Click: "+ Add New Camera"
- [ ] Enter:
  - [ ] Camera ID: `CAM_001`
  - [ ] Camera Name: `Classroom A Main`
  - [ ] Location: `Room 101`
  - [ ] IP Address: `192.168.1.100`
  - [ ] Select Batch: `CSE Batch A`
  - [ ] Active: ✓ checked
- [ ] Click: "Save Camera"

### 5. Create Timetable
- [ ] Click: "⏰ Timetable" in navigation
- [ ] Click: "+ Add Timetable Entry"
- [ ] Enter:
  - [ ] Timetable ID: `TT001`
  - [ ] Batch: `CSE Batch A`
  - [ ] Day: `Monday`
  - [ ] Period: `1`
  - [ ] Start Time: `09:00`
  - [ ] End Time: `10:30`
  - [ ] Subject: `Data Structures`
  - [ ] Teacher: `Dr. Sharma`
- [ ] Click: "Save Timetable Entry"
- [ ] Verify: Entry appears in table

### 6. Assign Camera to Schedule
- [ ] Check `data/camera_schedule.json` or use API
- [ ] Add entry linking:
  - [ ] Camera ID: `CAM_001`
  - [ ] Timetable ID: `TT001`
  - [ ] Active: `true`

---

## 👥 Student Registration (Variable Time)

### Option A: Using Website
- [ ] Click: "👥 Students" in navigation
- [ ] Click: "+ Add New Student"
- [ ] For each student:
  - [ ] Roll Number: `2410990250`
  - [ ] Name: `Aditya`
  - [ ] Batch: `CSE Batch A`
  - [ ] Email: `student@college.edu`
  - [ ] Image Path: `student_images/aditya.jpg`
  - [ ] Click: "Save Student"
- [ ] Verify: Student appears in list

### Option B: Using Python Script
- [ ] Open command prompt in `iotproject/` folder
- [ ] Run: `python setup_students.py`
- [ ] Follow prompts to register students
- [ ] This will:
  - [ ] Load student photos
  - [ ] Extract face encodings (embeddings)
  - [ ] Save to `students_database.json`
- [ ] Verify: students_database.json has new entries

---

## 🎬 Test Face Recognition (5 minutes)

### Before Testing
- [ ] Ensure good lighting
- [ ] Camera is working (test with Camera app first)
- [ ] At least 1 student registered with face
- [ ] Timetable has entry for NOW or soon
- [ ] All 3 services still running

### Testing Steps
- [ ] Check Calendar - what time/day is it?
- [ ] Go to "⏰ Timetable" page
- [ ] Make sure there's a class NOW or starting in 5 minutes
  - [ ] If not, add a test timetable entry for current time
  - [ ] Set end time 1 hour from now
  
- [ ] Go to "🎥 Cameras" page
- [ ] Verify camera is linked to current timetable
  - [ ] Check `data/camera_schedule.json` or use API
  - [ ] Ensure the link is enabled

- [ ] Check Terminal 3 (Camera Service)
- [ ] Look for logs starting with current time
- [ ] Should see:
  - [ ] "✅ Camera initialized: Classroom A Main"
  - [ ] "Camera checking schedule..."
  - [ ] (May show: "No active class right now" if time doesn't match)

### If Class Period is Active
- [ ] Walk in front of camera
- [ ] Should see output:
  - [ ] "⏳ Processing face..."
  - [ ] "✅ Marked Aditya (2410990250) - PRESENT"

- [ ] Check Terminal 3 again
- [ ] Should show attendance marking logs

- [ ] Check Website: "📋 Attendance Report"
- [ ] Select your batch
- [ ] Should see your name with:
  - [ ] Status: "PRESENT" (green)
  - [ ] Timestamp: current time
  - [ ] Confidence: 95-99%

---

## 📊 Dashboard Verification (2 minutes)

- [ ] Click: "📊 Dashboard"
- [ ] Verify you see:
  - [ ] Total Students: (should match what you added)
  - [ ] Total Batches: (should match)
  - [ ] Total Teachers: (should match)
  - [ ] Total Cameras: (should match)
  - [ ] Attendance Records: (should show 1+ if tested)

---

## 🔍 Data File Verification (5 minutes)

- [ ] Open File Explorer
- [ ] Navigate to: `data/` folder
- [ ] Verify these files exist:
  - [ ] `batches.json` (has your batch)
  - [ ] `teachers.json` (has your teachers)
  - [ ] `subjects.json` (has your subjects)
  - [ ] `cameras.json` (has your camera)
  - [ ] `timetable.json` (has your timetable)
  - [ ] `camera_schedule.json` (has the link)
  - [ ] `attendance.json` (has entries if tested)
  - [ ] `students_database.json` (in data/ or iotproject/)

- [ ] Open each JSON file in text editor
- [ ] Verify data looks correct (valid JSON format)

---

## 🧪 API Testing (Optional, 5 minutes)

Open this in browser:

- [ ] Get All Students:
  `http://localhost:8000/api/students`
  - [ ] Should return JSON array of students

- [ ] Get All Batches:
  `http://localhost:8000/api/batches`
  - [ ] Should return JSON array of batches

- [ ] Get Dashboard Summary:
  `http://localhost:8000/api/dashboard/summary`
  - [ ] Should return JSON with counts

- [ ] Get Attendance:
  `http://localhost:8000/api/attendance`
  - [ ] Should return JSON array (empty or with records)

---

## ✅ Final Verification Checklist

### System Status
- [ ] Backend running (Terminal 1 active)
- [ ] Frontend running (Terminal 2 active)
- [ ] Camera service running (Terminal 3 active)
- [ ] No error messages in any terminal
- [ ] Website accessible at localhost:3000
- [ ] API accessible at localhost:8000

### Data Status
- [ ] At least 1 batch created
- [ ] At least 2 teachers created
- [ ] At least 2 subjects created
- [ ] At least 1 camera created
- [ ] At least 1 timetable entry created
- [ ] At least 2 students registered with faces
- [ ] Camera linked to timetable (schedule)

### Functionality Status
- [ ] Can navigate all pages in website
- [ ] Can add new students
- [ ] Can view all master data
- [ ] Can create new timetable entries
- [ ] Camera service initializes without errors
- [ ] Face detection working (if period is active)
- [ ] Attendance being marked (if face detected)
- [ ] Reports show correct data

### Logging Status
- [ ] Backend logs show API requests
- [ ] Frontend logs show no critical errors
- [ ] Camera logs show face detection attempts
- [ ] attendance.json being updated

---

## 🎉 Congratulations!

If you've completed all checks above:

✅ Your system is **FULLY OPERATIONAL**! 🚀

You can now:
- Add unlimited students
- Create complex timetables
- Mark attendance automatically
- View attendance reports
- Scale to multiple cameras

---

## 🆘 Troubleshooting Guide

### If Terminal 1 (Backend) shows errors:

```
ERROR: ModuleNotFoundError: No module named 'fastapi'
→ Solution: 
  1. Close terminal
  2. Run: pip install -r requirements.txt
  3. Run: python main.py
```

### If Terminal 2 (Frontend) shows errors:

```
ERROR: Cannot find module 'react'
→ Solution:
  1. Close terminal
  2. Run: npm install
  3. Run: npm start
```

### If Terminal 3 (Camera) shows errors:

```
ERROR: No camera detected
→ Solution:
  1. Verify camera is connected
  2. Test with Windows Camera app first
  3. Check camera index (change 0 to 1 or 2)
```

### If Website won't load:

```
Connection refused at localhost:3000
→ Solution:
  1. Check if Terminal 2 is still running
  2. Check for "Compiled successfully" message
  3. Restart: close terminal and run start_frontend.bat again
```

### If API won't respond:

```
Cannot reach http://localhost:8000
→ Solution:
  1. Check if Terminal 1 is still running
  2. Check for "Application startup complete" message
  3. Restart: close terminal and run start_backend.bat again
```

---

## 📞 Support

If you're stuck:

1. Check **QUICK_START.md** for common issues
2. Check **README.md** troubleshooting section
3. Check **ARCHITECTURE.md** for system understanding
4. Check error messages in terminals carefully
5. Check JSON files are valid (no syntax errors)

---

## 📈 Next Steps After Verification

1. **Add More Data**
   - Register all students
   - Create full weekly timetable
   - Add all cameras

2. **Test Thoroughly**
   - Test with different students
   - Test during different periods
   - Verify attendance accuracy

3. **Deploy**
   - Run system during actual classes
   - Monitor logs for issues
   - Keep backups of data/ folder

4. **Enhance**
   - Add reports & analytics
   - Improve UI/UX
   - Add notifications

---

**✅ You're all set! Your face recognition attendance system is ready for use!**

**Time to see it in action! 🎬✅**
