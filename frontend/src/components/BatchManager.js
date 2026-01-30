import React, { useState, useEffect } from 'react';

function BatchManager({ apiBase }) {
  const [batches, setBatches] = useState([]);
  const [formData, setFormData] = useState({
    batch_id: '',
    batch_name: '',
    semester: ''
  });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchBatches();
  }, []);

  const fetchBatches = async () => {
    try {
      const response = await fetch(`${apiBase}/batches`);
      const data = await response.json();
      setBatches(data);
    } catch (error) {
      console.error('Error fetching batches:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiBase}/batches`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        fetchBatches();
        setFormData({ batch_id: '', batch_name: '', semester: '' });
        setShowForm(false);
        alert('✅ Batch added successfully!');
      }
    } catch (error) {
      console.error('Error adding batch:', error);
    }
  };

  return (
    <div className="page">
      <h2>Batch Management</h2>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add New Batch'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Batch ID (e.g., B001)"
            value={formData.batch_id}
            onChange={(e) => setFormData({...formData, batch_id: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Batch Name (e.g., CSE Batch A)"
            value={formData.batch_name}
            onChange={(e) => setFormData({...formData, batch_name: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Semester"
            value={formData.semester}
            onChange={(e) => setFormData({...formData, semester: e.target.value})}
            required
          />
          <button type="submit" className="btn btn-success">Save Batch</button>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Batch ID</th>
            <th>Name</th>
            <th>Semester</th>
          </tr>
        </thead>
        <tbody>
          {batches.map((batch) => (
            <tr key={batch.batch_id}>
              <td>{batch.batch_id}</td>
              <td>{batch.batch_name}</td>
              <td>{batch.semester}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {batches.length === 0 && <p className="empty-message">No batches added yet</p>}
    </div>
  );
}

export default BatchManager;
