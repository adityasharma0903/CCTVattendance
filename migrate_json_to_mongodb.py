"""
Migration Script: Import JSON data to MongoDB
Run this script to migrate all existing JSON data to MongoDB

Usage: python migrate_json_to_mongodb.py
"""

import json
import os
import sys
from pathlib import Path

# Add backend directory to path to import db module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from db import (
    get_db, add_student, add_batch, add_teacher, add_subject, add_camera,
    set_camera_mode, add_timetable_entry, add_camera_schedule, add_attendance,
    add_exam_violation
)

DATA_DIR = "data"

def load_json_file(filename):
    """Load JSON file"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return {}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return {}

def migrate_students():
    """Migrate students from JSON to MongoDB"""
    print("\n📚 Migrating Students...")
    students_data = load_json_file("students_database.json")
    
    if not students_data:
        print("✅ No students to migrate")
        return
    
    count = 0
    for roll_number, student in students_data.items():
        try:
            add_student({
                "student_id": student.get("student_id"),
                "roll_number": student.get("roll_number"),
                "name": student.get("name"),
                "batch_id": student.get("batch_id"),
                "email": student.get("email"),
                "image_path": student.get("image_path"),
                "embedding": student.get("embedding")
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating student {roll_number}: {e}")
    
    print(f"✅ Migrated {count} students")

def migrate_batches():
    """Migrate batches from JSON to MongoDB"""
    print("\n📚 Migrating Batches...")
    batches_data = load_json_file("batches.json")
    
    if not batches_data or not batches_data.get("batches"):
        print("✅ No batches to migrate")
        return
    
    count = 0
    for batch in batches_data.get("batches", []):
        try:
            add_batch({
                "batch_id": batch.get("batch_id"),
                "batch_name": batch.get("batch_name"),
                "semester": batch.get("semester")
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating batch {batch.get('batch_id')}: {e}")
    
    print(f"✅ Migrated {count} batches")

def migrate_teachers():
    """Migrate teachers from JSON to MongoDB"""
    print("\n👨‍🏫 Migrating Teachers...")
    teachers_data = load_json_file("teachers.json")
    
    if not teachers_data or not teachers_data.get("teachers"):
        print("✅ No teachers to migrate")
        return
    
    count = 0
    for teacher in teachers_data.get("teachers", []):
        try:
            add_teacher({
                "teacher_id": teacher.get("teacher_id"),
                "name": teacher.get("name"),
                "email": teacher.get("email"),
                "phone": teacher.get("phone")
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating teacher {teacher.get('teacher_id')}: {e}")
    
    print(f"✅ Migrated {count} teachers")

def migrate_subjects():
    """Migrate subjects from JSON to MongoDB"""
    print("\n📖 Migrating Subjects...")
    subjects_data = load_json_file("subjects.json")
    
    if not subjects_data or not subjects_data.get("subjects"):
        print("✅ No subjects to migrate")
        return
    
    count = 0
    for subject in subjects_data.get("subjects", []):
        try:
            add_subject({
                "subject_id": subject.get("subject_id"),
                "subject_name": subject.get("subject_name"),
                "subject_code": subject.get("subject_code"),
                "teacher_id": subject.get("teacher_id")
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating subject {subject.get('subject_id')}: {e}")
    
    print(f"✅ Migrated {count} subjects")

def migrate_cameras():
    """Migrate cameras from JSON to MongoDB"""
    print("\n📹 Migrating Cameras...")
    cameras_data = load_json_file("cameras.json")
    
    if not cameras_data or not cameras_data.get("cameras"):
        print("✅ No cameras to migrate")
        return
    
    count = 0
    for camera in cameras_data.get("cameras", []):
        try:
            add_camera({
                "camera_id": camera.get("camera_id"),
                "camera_name": camera.get("camera_name"),
                "location": camera.get("location"),
                "ip_address": camera.get("ip_address"),
                "batch_id": camera.get("batch_id"),
                "is_active": camera.get("is_active", True)
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating camera {camera.get('camera_id')}: {e}")
    
    print(f"✅ Migrated {count} cameras")

def migrate_camera_modes():
    """Migrate camera modes from JSON to MongoDB"""
    print("\n🎬 Migrating Camera Modes...")
    mode_data = load_json_file("camera_mode.json")
    
    if not mode_data or not mode_data.get("camera_modes"):
        print("✅ No camera modes to migrate")
        return
    
    count = 0
    for mode_entry in mode_data.get("camera_modes", []):
        try:
            set_camera_mode(
                mode_entry.get("camera_id"),
                mode_entry.get("mode", "NORMAL")
            )
            count += 1
        except Exception as e:
            print(f"❌ Error migrating camera mode {mode_entry.get('camera_id')}: {e}")
    
    print(f"✅ Migrated {count} camera modes")

def migrate_timetable():
    """Migrate timetable from JSON to MongoDB"""
    print("\n📅 Migrating Timetable...")
    timetable_data = load_json_file("timetable.json")
    
    if not timetable_data or not timetable_data.get("timetable"):
        print("✅ No timetable entries to migrate")
        return
    
    count = 0
    for entry in timetable_data.get("timetable", []):
        try:
            add_timetable_entry({
                "timetable_id": entry.get("timetable_id"),
                "batch_id": entry.get("batch_id"),
                "day": entry.get("day"),
                "period": entry.get("period"),
                "start_time": entry.get("start_time"),
                "end_time": entry.get("end_time"),
                "subject_id": entry.get("subject_id"),
                "teacher_id": entry.get("teacher_id"),
                "room": entry.get("room", "Unknown Room"),
                "is_exam": entry.get("is_exam", False)
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating timetable entry {entry.get('timetable_id')}: {e}")
    
    print(f"✅ Migrated {count} timetable entries")

def migrate_camera_schedules():
    """Migrate camera schedules from JSON to MongoDB"""
    print("\n📆 Migrating Camera Schedules...")
    schedule_data = load_json_file("camera_schedule.json")
    
    if not schedule_data or not schedule_data.get("camera_schedule"):
        print("✅ No camera schedules to migrate")
        return
    
    count = 0
    for schedule in schedule_data.get("camera_schedule", []):
        try:
            add_camera_schedule({
                "schedule_id": schedule.get("schedule_id"),
                "camera_id": schedule.get("camera_id"),
                "timetable_id": schedule.get("timetable_id"),
                "is_active": schedule.get("is_active", True)
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating schedule {schedule.get('schedule_id')}: {e}")
    
    print(f"✅ Migrated {count} camera schedules")

def migrate_attendance():
    """Migrate attendance from JSON to MongoDB"""
    print("\n✅ Migrating Attendance Records...")
    attendance_data = load_json_file("attendance.json")
    
    if not attendance_data or not attendance_data.get("attendance"):
        print("✅ No attendance records to migrate")
        return
    
    count = 0
    for record in attendance_data.get("attendance", []):
        try:
            add_attendance({
                "attendance_id": record.get("attendance_id"),
                "student_id": record.get("student_id"),
                "roll_number": record.get("roll_number"),
                "camera_id": record.get("camera_id"),
                "timestamp": record.get("timestamp"),
                "subject_id": record.get("subject_id"),
                "batch_id": record.get("batch_id"),
                "status": record.get("status", "PRESENT"),
                "confidence_score": record.get("confidence_score", 0.0)
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating attendance {record.get('attendance_id')}: {e}")
    
    print(f"✅ Migrated {count} attendance records")

def migrate_exam_violations():
    """Migrate exam violations from JSON to MongoDB"""
    print("\n⚠️  Migrating Exam Violations...")
    violations_data = load_json_file("exam_violations.json")
    
    if not violations_data or not violations_data.get("violations"):
        print("✅ No exam violations to migrate")
        return
    
    count = 0
    for violation in violations_data.get("violations", []):
        try:
            add_exam_violation({
                "violation_id": violation.get("violation_id"),
                "timestamp": violation.get("timestamp"),
                "student_id": violation.get("student_id"),
                "student_name": violation.get("student_name"),
                "teacher_id": violation.get("teacher_id"),
                "subject_id": violation.get("subject_id"),
                "camera_id": violation.get("camera_id"),
                "camera_name": violation.get("camera_name"),
                "camera_location": violation.get("camera_location"),
                "confidence": violation.get("confidence", 0.0),
                "duration_seconds": violation.get("duration_seconds"),
                "notes": violation.get("notes"),
                "severity": violation.get("severity", "high")
            })
            count += 1
        except Exception as e:
            print(f"❌ Error migrating violation {violation.get('violation_id')}: {e}")
    
    print(f"✅ Migrated {count} exam violations")

def main():
    """Run all migrations"""
    print("=" * 60)
    print("🚀 Starting JSON to MongoDB Migration")
    print("=" * 60)
    
    try:
        # Initialize database connection
        db = get_db()
        print("✅ Connected to MongoDB")
        
        # Run migrations
        migrate_students()
        migrate_batches()
        migrate_teachers()
        migrate_subjects()
        migrate_cameras()
        migrate_camera_modes()
        migrate_timetable()
        migrate_camera_schedules()
        migrate_attendance()
        migrate_exam_violations()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
