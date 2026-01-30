import React, { useState, useEffect } from 'react';

function TeacherManager({ apiBase }) {
  const [teachers, setTeachers] = useState([]);
  const [formData, setFormData] = useState({
    teacher_id: '',
    name: '',
    email: '',
    phone: ''
  });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchTeachers();
  }, []);

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
      const response = await fetch(`${apiBase}/teachers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        fetchTeachers();
        setFormData({ teacher_id: '', name: '', email: '', phone: '' });
        setShowForm(false);
        alert('✅ Teacher added successfully!');
      }
    } catch (error) {
      console.error('Error adding teacher:', error);
    }
  };

  return (
    <div className="page">
      <h2>Teacher Management</h2>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add New Teacher'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Teacher ID (e.g., T001)"
            value={formData.teacher_id}
            onChange={(e) => setFormData({...formData, teacher_id: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Full Name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Phone"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            required
          />
          <button type="submit" className="btn btn-success">Save Teacher</button>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Teacher ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
          </tr>
        </thead>
        <tbody>
          {teachers.map((teacher) => (
            <tr key={teacher.teacher_id}>
              <td>{teacher.teacher_id}</td>
              <td>{teacher.name}</td>
              <td>{teacher.email}</td>
              <td>{teacher.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {teachers.length === 0 && <p className="empty-message">No teachers added yet</p>}
    </div>
  );
}

export default TeacherManager;
