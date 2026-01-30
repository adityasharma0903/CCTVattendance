import React, { useState, useEffect } from 'react';

function SubjectManager({ apiBase }) {
  const [subjects, setSubjects] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [formData, setFormData] = useState({
    subject_id: '',
    subject_name: '',
    subject_code: '',
    teacher_id: ''
  });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchSubjects();
    fetchTeachers();
  }, []);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiBase}/subjects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        fetchSubjects();
        setFormData({ subject_id: '', subject_name: '', subject_code: '', teacher_id: '' });
        setShowForm(false);
        alert('✅ Subject added successfully!');
      }
    } catch (error) {
      console.error('Error adding subject:', error);
    }
  };

  return (
    <div className="page">
      <h2>Subject Management</h2>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add New Subject'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Subject ID (e.g., S001)"
            value={formData.subject_id}
            onChange={(e) => setFormData({...formData, subject_id: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Subject Name"
            value={formData.subject_name}
            onChange={(e) => setFormData({...formData, subject_name: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Subject Code"
            value={formData.subject_code}
            onChange={(e) => setFormData({...formData, subject_code: e.target.value})}
            required
          />
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
          <button type="submit" className="btn btn-success">Save Subject</button>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Subject ID</th>
            <th>Name</th>
            <th>Code</th>
            <th>Teacher</th>
          </tr>
        </thead>
        <tbody>
          {subjects.map((subject) => {
            const teacher = teachers.find(t => t.teacher_id === subject.teacher_id);
            return (
              <tr key={subject.subject_id}>
                <td>{subject.subject_id}</td>
                <td>{subject.subject_name}</td>
                <td>{subject.subject_code}</td>
                <td>{teacher?.name || 'N/A'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {subjects.length === 0 && <p className="empty-message">No subjects added yet</p>}
    </div>
  );
}

export default SubjectManager;
