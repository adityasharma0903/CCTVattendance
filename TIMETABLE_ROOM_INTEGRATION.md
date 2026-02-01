# Timetable Room Integration for Exam Mode

## Overview
Room details are now managed centrally through the timetable instead of manual prompts. This ensures consistency across normal attendance and exam mode.

## Changes Made

### 1. **Timetable Data Structure** (`data/timetable.json`)
- Added `"room"` field to all timetable entries
- Format: `"room": "Exam Room 1"`
- Examples: "Classroom A", "Exam Hall B", "Room 301", etc.

### 2. **Backend Camera Service** (`camera_service/attendance_service.py`)
- Modified `save_violation_to_backend()` function:
  - Now extracts room from `schedule.get("room")`
  - Passes `camera_location` with room name to violation API
  - Includes room in violation notes for better logging

### 3. **Frontend Camera Manager** (`frontend/src/components/CameraManager.js`)
- Removed manual room prompt on Exam Mode
- Changed to: "Room details will be fetched from timetable"
- Simplified `updateCameraMode()` function
- No more duplicate manual entry needed

### 4. **Frontend Exam Violation Report** (`frontend/src/components/ExamViolationReport.js`)
- Added `fetchTimetable()` function to load timetable data
- Enhanced `getCameraRoom()` to check multiple sources in priority:
  1. `violation.camera_location` (from timetable via camera service)
  2. `violation.camera_name` (fallback)
  3. `timetable.room` (matched by subject_id)
  4. `camera.location` (camera default)
- Ensures room displays correctly in violation report

## Data Flow

```
┌─────────────────────────┐
│   Timetable Entry       │
│  (with room field)      │
└───────────┬─────────────┘
            │
     ┌──────▼──────┐
     │ Camera Start │ ◄── Exam Mode Enabled
     │ Exam Session │
     └──────┬───────┘
            │
      ┌─────▼──────────┐
      │ Phone Detected │
      │  in Frame      │
      └─────┬──────────┘
            │
    ┌───────▼────────────┐
    │ Save Violation to  │
    │ Backend with Room  │
    │ (from timetable)   │
    └───────┬────────────┘
            │
     ┌──────▼─────────────┐
     │ Frontend Displays  │
     │ Violation + Room   │
     │ in Dashboard       │
     └────────────────────┘
```

## Usage Flow

### Before Starting Exam
1. Create timetable entry with:
   - Subject ID
   - Teacher ID
   - Batch ID
   - **Room/Location** (new)
   - Mark as `is_exam: true`

### During Exam
1. Click "Exam Mode" on camera
2. System automatically uses room from timetable
3. No manual prompt needed
4. Room persists in all violation records

### Viewing Reports
1. Open "📱 Exam Violations" dashboard
2. Room displays automatically from:
   - Violation's `camera_location` field (primary)
   - Timetable matched by subject_id (secondary)
3. Filter by camera/room as needed

## Key Benefits

✅ **No Manual Entry** - Room is already in timetable  
✅ **Consistency** - Same room for all violations in that session  
✅ **Automatic Sync** - Camera service fetches from active schedule  
✅ **Better UX** - One less prompt to manage  
✅ **Easy Updates** - Change room in timetable, applies everywhere  
✅ **Both Modes** - Works for normal attendance and exam mode  

## Testing Checklist

- [ ] Create exam timetable with room field
- [ ] Start exam session (Exam Mode)
- [ ] Detect phone in frame
- [ ] Check violation shows correct room in dashboard
- [ ] Filter by room/camera works correctly
- [ ] Room persists in violation records (JSON)
- [ ] Works with both normal and exam classes

## API Endpoints Used

| Endpoint | Purpose | Data |
|----------|---------|------|
| `GET /api/timetable` | Fetch all timetable entries | Array with room field |
| `GET /api/exam-violations` | Fetch violations | Includes camera_location |
| `POST /api/camera-mode` | Set camera mode | No room parameter needed |

## Files Modified

1. ✅ `data/timetable.json` - Added room field
2. ✅ `camera_service/attendance_service.py` - Extract room from schedule
3. ✅ `frontend/src/components/CameraManager.js` - Removed prompt
4. ✅ `frontend/src/components/ExamViolationReport.js` - Fetch & display room

## Next Steps

1. Restart backend service
2. Restart frontend service
3. Restart camera service
4. Test end-to-end flow
5. Verify room displays in violations dashboard

