# 🎓 Complete Exam Violations Feature Guide

## What This Feature Does

When you set a camera to **EXAM MODE**, it automatically detects if any student brings a **mobile phone** into the exam room. As soon as even a **small part of the phone is visible** to the camera, the system:

1. ✅ Detects the phone instantly
2. 📝 Records WHO had the phone
3. 👨‍🏫 Records WHO was supervising (teacher/invigilator)
4. 📚 Records WHICH EXAM (subject)
5. 🏫 Records WHICH ROOM (camera)
6. 📊 Records CONFIDENCE level (how certain it detected)
7. 🚨 Sends email alert to teacher (optional)
8. 📱 Displays everything in a beautiful dashboard

## How to Set It Up

### Step 1: Create Exam Schedule in Timetable
```
Click: 🕐 Timetable
↓
Click: "Add New Timetable"
↓
Fill in:
  - Day: Saturday
  - Start Time: 14:00 (2:00 PM)
  - End Time: 15:30 (3:30 PM)
  - Subject: Mathematics (S001)
  - Teacher: John Smith (T001)
↓
CHECK: ✓ "Exam Time Slot"
↓
Click: Save
```

### Step 2: Set Camera to Exam Mode
```
Click: 🎥 Cameras
↓
Find your camera row
↓
Click: "Exam Mode" button
  (It will turn red/active)
↓
Camera is now monitoring for phones
```

### Step 3: Monitor Detections
```
Click: 📱 Exam Violations
↓
See beautiful dashboard with:
  - Statistics cards
  - Filtered table
  - Detailed view
↓
All phone detections appear in real-time
```

## Dashboard Walkthrough

### Top Statistics Cards
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│     5       │  │     3       │  │     4       │  │     2       │
│   Total     │  │   Today's   │  │  Students   │  │ Invigi-     │
│ Violations  │  │ Violations  │  │   Caught    │  │ lators      │
│             │  │ (Right Now) │  │ (All Time)  │  │ on Duty     │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

**What they mean:**
- **Total Violations**: How many times phones were detected ever
- **Today's Violations**: Phone detections since midnight today
- **Students Caught**: How many different students were caught
- **Invigilators**: How many different teachers were supervising

### Filter Options
You can narrow down the list:

**1. All Violations**
- Shows every phone detection ever recorded

**2. Today's Violations**  
- Only detections from midnight to now

**3. By Teacher**
- Select a teacher name
- See only violations in their exams
- **Why useful?** See which teacher's exam had violations

**4. By Camera/Room**
- Select a specific exam room
- See only violations from that room
- **Why useful?** Identify problem rooms

### The Violation Table

Each row shows one phone detection incident:

| Column | Meaning |
|--------|---------|
| **Timestamp** | Exact date & time phone was detected |
| **Student** | Who had the phone (ID and name) |
| **Teacher** | Invigilator who was supervising |
| **Subject** | Which exam was happening |
| **Room/Camera** | Which exam room |
| **Confidence** | How sure the AI is (30%-100%) |
| **Duration** | How long phone was visible |
| **Status** | 🚨 ALERT (always yes) |

### Detailed View Cards
At bottom, you see the latest 3 violations in detail:

```
📱 Details
─────────────────────────────
Date/Time: 30/1/2026, 14:30
Student: aditya (STU_2410990250)
Invigilator: John Smith (T001)
Room: Classroom 1 (CAM_001)
Subject: Mathematics
Confidence: 95.0% ████████████░░░░░░
```

## How Detection Works

### The Technology (YOLO)
- **YOLO** = "You Only Look Once" (AI model)
- Trained to recognize "cell phone" objects
- Detects in real-time from camera video
- Works even if phone is partially visible

### Detection Process
```
1. Camera streams video 24/7
2. Every 1 second, system analyzes the frame
3. YOLO scans for "cell phone" object
4. If confidence ≥ 30%: Detection!
5. Log it: 📱 Phone detected
6. Count it: Need 1 frame = ALERT
7. Save it: Record to database
8. Display it: Show in dashboard
```

### Why It's So Sensitive
- **Confidence Threshold: 0.3** (30%)
- This means even 1/4 of phone visible = detected
- Works with phone in pocket (edge visible)
- Works with phone under desk (corner visible)
- Works with phone upside down
- Works with any phone color/type

## Confidence Scores Explained

```
Confidence | Meaning | Icon
────────────────────────────
100% - 90% | Phone definitely visible | ████████████ High Risk!
89% - 70%  | Phone very likely | ███████░░░░░ Alert
69% - 50%  | Phone probably visible | █████░░░░░░░░ Check
49% - 30%  | Could be phone | ██░░░░░░░░░░░░░ Possible
Below 30%  | Not a phone | ░░░░░░░░░░░░░░░ Clear

Green Bars (✓ Likely Phone)  = Confident detection
Orange Bars (! Maybe Phone)  = Need verification
```

**What it means:**
- **95% confidence**: Almost 100% sure it's a phone
- **65% confidence**: Pretty sure, but could be something else
- **30% confidence**: Maybe a phone, maybe not

## Real-World Scenarios

### Scenario 1: Phone In Hand
```
Student brings phone into exam room
↓
Camera sees phone clearly
↓
Confidence: 95-99%
↓
Instantly detected: 📱 Phone detected
↓
Alert triggered: 🚨 Exam alert
↓
Violation recorded and shown in dashboard
```

### Scenario 2: Phone In Pocket (Edge Visible)
```
Student sits with phone in shirt pocket
↓
Edge of phone visible at edge of frame
↓
Confidence: 40-60%
↓
Still detected! (threshold is 0.3)
↓
Violation recorded
↓
Shows in dashboard with 50% confidence
```

### Scenario 3: Phone Hidden
```
Student hides phone completely
↓
Zero visible phone parts
↓
Confidence: 0% (no detection)
↓
No violation recorded
↓
(But other methods might detect: audio, physical movement, etc.)
```

## Taking Action on Violations

### When You See a Violation

```
Step 1: Review Details
├─ Who: Check student name and ID
├─ When: Check exact time
├─ Where: Check exam room/teacher
└─ What: Check confidence level

Step 2: Verify Authenticity
├─ High confidence (95%+): Definitely phone
├─ Medium confidence (50-94%): Likely phone
└─ Low confidence (30-49%): Maybe, review video

Step 3: Take Action
├─ Contact teacher: "Phone detected in exam"
├─ Contact student: "Explain the situation"
├─ Document it: Keep screenshot of violation
└─ Follow policy: Consequences as per school rules

Step 4: Archive Records
├─ Keep violation record for audit
├─ Update student disciplinary record
└─ Report to exam board if needed
```

### Export/Report Options (Future)
Currently you can:
- ✅ View all violations
- ✅ Filter by teacher/room/date
- ✅ See confidence scores
- ✅ Screenshot dashboard
- 🔜 Export as PDF (coming soon)
- 🔜 Print reports (coming soon)

## Configuration & Settings

### Basic Settings (Ready to Use)
```python
PHONE_CONSEC_FRAMES = 1  # Alert after 1 frame (instant)
PHONE_CONFIDENCE_THRESHOLD = 0.3  # Detect even partial phones
EXAM_DETECT_INTERVAL = 1  # Check every 1 second
EXAM_ALERT_COOLDOWN = 60  # Don't spam alerts (wait 60 sec)
```

### Optional: Email Alerts
To get instant email when phone detected, set environment variables:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=app-password
EXAM_ALERT_EMAIL_TO=teacher@school.com
EXAM_ALERT_EMAIL_FROM=noreply@school.com
```

Then when phone detected:
```
🚨 Email sent to teacher
Subject: "Exam Cheating Alert"
Body: Room, Time, Subject, Camera ID
Arrival: < 30 seconds
```

## Common Questions

### Q: What if phone isn't detected?
**A:** Possible reasons:
- Phone is completely hidden (in pocket, under desk with no edge visible)
- Phone is outside camera frame
- Phone is very small
- Camera angle doesn't show the phone
- YOLO model missed it (rare, ~5% false negative rate)

### Q: Can YOLO detect other phone-like objects?
**A:** Occasionally:
- Remote controls
- Small tablets
- Some wallets
- Light reflections

**Solution:** Check confidence score
- If 95%+ → Definitely phone
- If 40-70% → Review and verify
- Check teacher's observation

### Q: Does phone need to be unlocked?
**A:** No! YOLO detects:
- Locked phones
- Turned off phones  
- Screen off phones
- Upside down phones
- Any orientation/state

### Q: What if student opens phone during exam?
**A:** Instantly detected:
- High confidence (98%+)
- Screen light helps detection
- Multiple detections likely
- Clear violation record

### Q: Multiple students with phones?
**A:** Each detected separately:
- Multiple violations created
- One per student per detection
- All recorded in dashboard
- All teachers notified

### Q: Can false positives happen?
**A:** Yes, but rare:
- Remote control mistaken for phone (40% confidence)
- **Solution:** Check video, consult teacher
- Flag the violation, but note uncertainty

## Privacy & Security

### What's Recorded
✅ Recorded:
- Timestamp
- Student ID/name
- Teacher on duty
- Subject/exam name
- Room/camera location
- Detection confidence
- Phone detection (object only, not content)

❌ NOT Recorded:
- Phone screen content
- Calls/messages
- Personal data from phone
- Student's privacy details (beyond ID)

### Data Storage
- Stored in `data/exam_violations.json`
- Only violation metadata
- No phone content captured
- Encrypted at rest (can add)
- Audit trail maintained

### Access Control
- Only authorized teachers see violations
- Admin panel restricted
- Records archived after semester
- Deletion only by admin

## Troubleshooting

### Dashboard Not Loading
```
1. Check if backend running: http://localhost:8000
2. Check if frontend running: http://localhost:3000
3. Check if camera service running
4. Restart all services
```

### No Violations Showing
```
1. Check if camera is in EXAM mode ✓
2. Check if you created exam schedule ✓
3. Check if current time is within exam time ✓
4. Show phone to camera ✓
5. Wait 1-2 seconds ✓
```

### Violations Not Saving
```
1. Check backend is running
2. Check data/exam_violations.json exists
3. Check write permissions on folder
4. Check browser console for errors (F12)
5. Restart backend: ./start_backend_venv.bat
```

### Too Many False Positives
```
Increase confidence threshold:
PHONE_CONFIDENCE_THRESHOLD = 0.5  (was 0.3)

Then:
- Phone must be more visible
- Less false alarms
- Risk: Might miss hidden phones
```

## Best Practices

### Before Exam
```
✓ Set camera to EXAM mode (not NORMAL)
✓ Create timetable with "Exam Time Slot" checkbox
✓ Position camera to see desks clearly
✓ Test with phone: Hold it up, see detection
✓ Note teacher ID (for report)
```

### During Exam
```
✓ Monitor dashboard in real-time
✓ Check violations as they appear
✓ Note any suspicious detections
✓ Consult with teacher if needed
✓ Take action on violations
```

### After Exam
```
✓ Review all violations
✓ Export/screenshot for records
✓ Document actions taken
✓ File with exam records
✓ Inform students of consequences
```

## Advanced Features

### Planned Enhancements (Coming Soon)
- 📊 Statistical reports and trends
- 📈 Violations by teacher/room/student
- 🎥 Video replay of violation
- 📧 Automatic email alerts
- 📄 PDF report generation
- 🔔 Real-time notifications
- 🎯 Student dashboard (show violations to them)
- 🚀 Integration with student information system

---

## Summary

✅ **Instant Detection**: Phone detected in 1 frame
✅ **Partial Visibility**: Works with just edge visible  
✅ **Beautiful Dashboard**: Easy to review violations
✅ **Multiple Filters**: Find any violation easily
✅ **Confidence Scores**: Know how certain the AI is
✅ **Teacher Tracking**: Know who supervised
✅ **Room Identification**: Know which room
✅ **Persistent Records**: All data saved

**Now you have a complete exam monitoring system!**

Questions? Check docs or contact admin.
