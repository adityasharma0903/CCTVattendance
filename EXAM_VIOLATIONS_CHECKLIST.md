# ✅ Exam Violations Feature - Setup Checklist

## Pre-Deployment Checklist

- [ ] All services are running:
  - [ ] Backend: `./start_backend_venv.bat`
  - [ ] Frontend: `./start_frontend.bat`  
  - [ ] Camera Service: `./start_camera_service_venv.bat`

- [ ] Frontend can access backend:
  - [ ] Open http://localhost:3000
  - [ ] Check console (F12) - no CORS errors
  - [ ] API responds at http://localhost:8000/api

- [ ] New component files exist:
  - [ ] `frontend/src/components/ExamViolationReport.js`
  - [ ] `frontend/src/components/ExamViolationReport.css`

- [ ] Backend API updated:
  - [ ] `backend/main.py` has ExamViolation model
  - [ ] 4 new endpoints added
  - [ ] `exam_violations.json` exists

- [ ] Camera service enhanced:
  - [ ] `attendance_service.py` updated
  - [ ] PHONE_CONFIDENCE_THRESHOLD = 0.3
  - [ ] PHONE_CONSEC_FRAMES = 1
  - [ ] `save_violation_to_backend()` method exists

## First-Time Setup (5 minutes)

### 1. Create Exam Timetable
```
[ ] Go to 🕐 Timetable
[ ] Click "Add New Timetable"
[ ] Fill details:
    [ ] Day: Saturday
    [ ] Start: 14:00
    [ ] End: 15:30
    [ ] Subject: Select one
    [ ] Teacher: Select one
[ ] CHECK ✓ "Exam Time Slot"
[ ] Click Save
[ ] Verify in table
```

### 2. Set Camera to Exam Mode
```
[ ] Go to 🎥 Cameras
[ ] Find your camera row
[ ] Click "Exam Mode" button
[ ] Verify button turns active/red
```

### 3. View Violations Dashboard
```
[ ] Go to 📱 Exam Violations (new menu item!)
[ ] See 4 statistics cards
[ ] See filter options
[ ] See violations table (empty initially)
[ ] See "No phone detections found" message
```

### 4. Test Detection
```
[ ] During exam time (14:00-15:30):
    [ ] Show your phone to camera
    [ ] Even edge/corner counts
    [ ] Wait 1-2 seconds
[ ] Check dashboard
[ ] Should see new violation with:
    [ ] Timestamp
    [ ] Confidence ~95%
    [ ] Subject name
    [ ] Room/Camera ID
```

## Daily Usage Checklist

### Before Exam Session
```
[ ] Create exam timetable
[ ] Set correct day and time
[ ] Set camera to EXAM mode (not NORMAL)
[ ] Test: Point phone at camera briefly
[ ] Confirm detection on dashboard
[ ] Verify teacher name is correct
[ ] Check camera location/room name
```

### During Exam
```
[ ] Monitor violations in real-time
[ ] Check dashboard periodically
[ ] Note any unexpected detections
[ ] Consult with teacher if needed
[ ] Keep dashboard window open
```

### After Exam
```
[ ] Review all violations
[ ] Filter by teacher/room if multi-exam
[ ] Screenshot important violations
[ ] Contact students as needed
[ ] Document actions taken
[ ] Archive for records
```

## Troubleshooting Checklist

### Violations Not Showing Up
```
[ ] Check camera is in EXAM mode (not NORMAL)
    If not: Go to 🎥 Cameras → Click "Exam Mode"

[ ] Check exam timetable exists and is correct
    If not: Go to 🕐 Timetable → Create new

[ ] Check current time is within exam time
    If not: Create timetable covering current time
    If yes: Wait, timing is correct

[ ] Check camera is on and working
    If not: Restart camera service

[ ] Test manually:
    [ ] Show phone to camera
    [ ] Wait 1-2 seconds
    [ ] Refresh dashboard (button in top right)
    [ ] Look for new violation
```

### Dashboard Not Loading
```
[ ] Check frontend is running
    If not: ./start_frontend.bat

[ ] Check backend is running  
    If not: ./start_backend_venv.bat

[ ] Clear browser cache
    [ ] Press Ctrl+Shift+Del
    [ ] Select "Cookies and Cache"
    [ ] Click "Clear"

[ ] Check browser console (F12 → Console tab)
    [ ] Look for red errors
    [ ] Note the error message
    [ ] Fix or restart services

[ ] Try hard refresh: Ctrl+F5
```

## Feature Verification Checklist

### Dashboard Components
```
[ ] Statistics cards visible
[ ] Filter section works
[ ] Violations table displays
[ ] Detail cards show info
[ ] Responsive on mobile
```

### Functionality
```
[ ] Filtering works correctly
[ ] Refresh button loads data
[ ] Data persists after reload
[ ] Responsive on all devices
```

---

**Status:** ✅ Ready to Use
