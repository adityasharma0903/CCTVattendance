import React, { useState, useEffect } from 'react';

function TimetableManager({ apiBase }) {
  const [timetables, setTimetables] = useState([]);
  const [batches, setBatches] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [formData, setFormData] = useState({
    timetable_id: '',
    batch_id: '',
    day: 'Monday',
    period: '',
    start_time: '',
    end_time: '',
    subject_id: '',
    teacher_id: '',
    is_exam: false
  });
  const [showForm, setShowForm] = useState(false);

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  useEffect(() => {
    fetchTimetables();
    fetchBatches();
    fetchSubjects();
    fetchTeachers();
    fetchCameras();
  }, []);

  const fetchTimetables = async () => {
    try {
      const response = await fetch(`${apiBase}/timetable`);
      const data = await response.json();
      setTimetables(data);
    } catch (error) {
      console.error('Error fetching timetables:', error);
    }
  };

  const fetchBatches = async () => {
    try {
      const response = await fetch(`${apiBase}/batches`);
      const data = await response.json();
      setBatches(data);
    } catch (error) {
      console.error('Error fetching batches:', error);
    }
  };

  const fetchSubjects = async () => {
    try {
      const response = await fetch(`${apiBase}/subjects`);
      const data = await response.json();
      setSubjects(data);
    } catch (error) {
      console.error('Error fetching subjects:', error);
    }
  };

  const fetchTeachers = async () => {
    try {
      const response = await fetch(`${apiBase}/teachers`);
      const data = await response.json();
      setTeachers(data);
    } catch (error) {
      console.error('Error fetching teachers:', error);
    }
  };

  const fetchCameras = async () => {
    try {
      const response = await fetch(`${apiBase}/cameras`);
      const data = await response.json();
      setCameras(data);
    } catch (error) {
      console.error('Error fetching cameras:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiBase}/timetable`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        // Auto-link timetable to first available camera
        if (cameras.length > 0) {
          const cameraId = cameras[0].camera_id;
          const schedulePayload = {
            schedule_id: `CS_${Date.now()}`,
            camera_id: cameraId,
            timetable_id: formData.timetable_id,
            is_active: true
          };
          await fetch(`${apiBase}/camera-schedule`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(schedulePayload)
          });
        }

        fetchTimetables();
        setFormData({
          timetable_id: '',
          batch_id: '',
          day: 'Monday',
          period: '',
          start_time: '',
          end_time: '',
          subject_id: '',
          teacher_id: '',
          is_exam: false
        });
        setShowForm(false);
        alert('✅ Timetable entry added successfully!');
      }
    } catch (error) {
      console.error('Error adding timetable:', error);
    }
  };

  return (
    <div className="page">
      <h2>Timetable Management</h2>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add Timetable Entry'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Timetable ID (e.g., TT001)"
            value={formData.timetable_id}
            onChange={(e) => setFormData({...formData, timetable_id: e.target.value})}
            required
          />
          <select
            value={formData.batch_id}
            onChange={(e) => setFormData({...formData, batch_id: e.target.value})}
            required
          >
            <option value="">Select Batch</option>
            {batches.map(batch => (
              <option key={batch.batch_id} value={batch.batch_id}>
                {batch.batch_name}
              </option>
            ))}
          </select>
          <select
            value={formData.day}
            onChange={(e) => setFormData({...formData, day: e.target.value})}
            required
          >
            {days.map(day => (
              <option key={day} value={day}>{day}</option>
            ))}
          </select>
          <input
            type="number"
            placeholder="Period"
            value={formData.period}
            onChange={(e) => setFormData({...formData, period: e.target.value})}
            required
          />
          <input
            type="time"
            value={formData.start_time}
            onChange={(e) => setFormData({...formData, start_time: e.target.value})}
            required
          />
          <input
            type="time"
            value={formData.end_time}
            onChange={(e) => setFormData({...formData, end_time: e.target.value})}
            required
          />
          <select
            value={formData.subject_id}
            onChange={(e) => setFormData({...formData, subject_id: e.target.value})}
            required
          >
            <option value="">Select Subject</option>
            {subjects.map(subject => (
              <option key={subject.subject_id} value={subject.subject_id}>
                {subject.subject_name}
              </option>
            ))}
          </select>
          <select
            value={formData.teacher_id}
            onChange={(e) => setFormData({...formData, teacher_id: e.target.value})}
            required
          >
            <option value="">Select Teacher</option>
            {teachers.map(teacher => (
              <option key={teacher.teacher_id} value={teacher.teacher_id}>
                {teacher.name}
              </option>
            ))}
          </select>
          <label>
            <input
              type="checkbox"
              checked={formData.is_exam}
              onChange={(e) => setFormData({...formData, is_exam: e.target.checked})}
            />
            Exam Time Slot
          </label>
          <button type="submit" className="btn btn-success">Save Timetable Entry</button>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Batch</th>
            <th>Day</th>
            <th>Period</th>
            <th>Time</th>
            <th>Subject</th>
            <th>Teacher</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {timetables.map((tt) => {
            const subject = subjects.find(s => s.subject_id === tt.subject_id);
            const teacher = teachers.find(t => t.teacher_id === tt.teacher_id);
            return (
              <tr key={tt.timetable_id}>
                <td>{tt.batch_id}</td>
                <td>{tt.day}</td>
                <td>{tt.period}</td>
                <td>{tt.start_time} - {tt.end_time}</td>
                <td>{subject?.subject_name || 'N/A'}</td>
                <td>{teacher?.name || 'N/A'}</td>
                <td>{tt.is_exam ? 'EXAM' : 'CLASS'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {timetables.length === 0 && <p className="empty-message">No timetable entries added yet</p>}
    </div>
  );
}

export default TimetableManager;
