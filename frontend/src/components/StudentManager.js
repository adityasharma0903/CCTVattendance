import React, { useState, useEffect } from 'react';

function StudentManager({ apiBase }) {
  const [students, setStudents] = useState([]);
  const [batches, setBatches] = useState([]);
  const [formData, setFormData] = useState({
    roll_number: '',
    name: '',
    batch_id: '',
    email: '',
    image_path: ''
  });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchStudents();
    fetchBatches();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await fetch(`${apiBase}/students`);
      const data = await response.json();
      setStudents(data);
    } catch (error) {
      console.error('Error fetching students:', error);
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiBase}/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        fetchStudents();
        setFormData({
          roll_number: '',
          name: '',
          batch_id: '',
          email: '',
          image_path: ''
        });
        setShowForm(false);
        alert('✅ Student added successfully!');
      }
    } catch (error) {
      console.error('Error adding student:', error);
      alert('❌ Error adding student');
    }
  };

  const handleDelete = async (rollNumber) => {
    if (window.confirm('Are you sure?')) {
      try {
        const response = await fetch(`${apiBase}/students/${rollNumber}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          fetchStudents();
          alert('✅ Student deleted successfully!');
        }
      } catch (error) {
        console.error('Error deleting student:', error);
      }
    }
  };

  return (
    <div className="page">
      <h2>Student Management</h2>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add New Student'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="roll_number"
            placeholder="Roll Number"
            value={formData.roll_number}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="name"
            placeholder="Student Name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />
          <select
            name="batch_id"
            value={formData.batch_id}
            onChange={handleInputChange}
            required
          >
            <option value="">Select Batch</option>
            {batches.map(batch => (
              <option key={batch.batch_id} value={batch.batch_id}>
                {batch.batch_name}
              </option>
            ))}
          </select>
          <input
            type="email"
            name="email"
            placeholder="Email (optional)"
            value={formData.email}
            onChange={handleInputChange}
          />
          <input
            type="text"
            name="image_path"
            placeholder="Image Path (e.g., student_images/name.jpg)"
            value={formData.image_path}
            onChange={handleInputChange}
          />
          <button type="submit" className="btn btn-success">Save Student</button>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Roll Number</th>
            <th>Name</th>
            <th>Batch</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.roll_number}>
              <td>{student.roll_number}</td>
              <td>{student.name}</td>
              <td>{student.batch_id || 'N/A'}</td>
              <td>{student.email || 'N/A'}</td>
              <td>
                <button 
                  className="btn btn-danger" 
                  onClick={() => handleDelete(student.roll_number)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {students.length === 0 && <p className="empty-message">No students added yet</p>}
    </div>
  );
}

export default StudentManager;
