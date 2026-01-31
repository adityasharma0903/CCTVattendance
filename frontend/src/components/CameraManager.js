import React, { useState, useEffect } from 'react';

function CameraManager({ apiBase }) {
  const [cameras, setCameras] = useState([]);
  const [batches, setBatches] = useState([]);
  const [cameraModes, setCameraModes] = useState({});
  const [formData, setFormData] = useState({
    camera_id: '',
    camera_name: '',
    location: '',
    ip_address: '',
    batch_id: '',
    is_active: true
  });
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchCameras();
    fetchBatches();
  }, []);

  const fetchCameras = async () => {
    try {
      const response = await fetch(`${apiBase}/cameras`);
      const data = await response.json();
      setCameras(data);
      fetchCameraModes(data);
    } catch (error) {
      console.error('Error fetching cameras:', error);
    }
  };

  const fetchCameraModes = async (cameraList) => {
    try {
      const modeEntries = await Promise.all(
        cameraList.map(async (camera) => {
          const response = await fetch(`${apiBase}/camera-mode/${camera.camera_id}`);
          const data = await response.json();
          return [camera.camera_id, data.mode || 'NORMAL'];
        })
      );
      setCameraModes(Object.fromEntries(modeEntries));
    } catch (error) {
      console.error('Error fetching camera modes:', error);
    }
  };

  const updateCameraMode = async (cameraId, mode) => {
    try {
      const response = await fetch(`${apiBase}/camera-mode`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ camera_id: cameraId, mode })
      });
      if (response.ok) {
        setCameraModes(prev => ({ ...prev, [cameraId]: mode }));
      }
    } catch (error) {
      console.error('Error updating camera mode:', error);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiBase}/cameras`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        fetchCameras();
        setFormData({
          camera_id: '',
          camera_name: '',
          location: '',
          ip_address: '',
          batch_id: '',
          is_active: true
        });
        setShowForm(false);
        alert('✅ Camera added successfully!');
      }
    } catch (error) {
      console.error('Error adding camera:', error);
    }
  };

  return (
    <div className="page">
      <h2>Camera Management</h2>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add New Camera'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Camera ID (e.g., CAM_001)"
            value={formData.camera_id}
            onChange={(e) => setFormData({...formData, camera_id: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Camera Name"
            value={formData.camera_name}
            onChange={(e) => setFormData({...formData, camera_name: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Location"
            value={formData.location}
            onChange={(e) => setFormData({...formData, location: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="IP Address"
            value={formData.ip_address}
            onChange={(e) => setFormData({...formData, ip_address: e.target.value})}
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
          <label>
            <input
              type="checkbox"
              checked={formData.is_active}
              onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
            />
            Active
          </label>
          <button type="submit" className="btn btn-success">Save Camera</button>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Camera ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>IP Address</th>
            <th>Batch</th>
            <th>Status</th>
            <th>Mode</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {cameras.map((camera) => (
            <tr key={camera.camera_id}>
              <td>{camera.camera_id}</td>
              <td>{camera.camera_name}</td>
              <td>{camera.location}</td>
              <td>{camera.ip_address}</td>
              <td>{camera.batch_id}</td>
              <td>{camera.is_active ? '✅ Active' : '❌ Inactive'}</td>
              <td>{cameraModes[camera.camera_id] || 'NORMAL'}</td>
              <td>
                <button
                  className="btn btn-secondary"
                  onClick={() => updateCameraMode(camera.camera_id, 'NORMAL')}
                >
                  Normal Mode
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => updateCameraMode(camera.camera_id, 'EXAM')}
                >
                  Exam Mode
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {cameras.length === 0 && <p className="empty-message">No cameras added yet</p>}
    </div>
  );
}

export default CameraManager;
