import React, { useState, useEffect } from 'react';

function Dashboard({ apiBase }) {
  const [summary, setSummary] = useState({
    total_students: 0,
    total_batches: 0,
    total_teachers: 0,
    total_cameras: 0,
    total_attendance_records: 0
  });

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const response = await fetch(`${apiBase}/dashboard/summary`);
      const data = await response.json();
      setSummary(data);
    } catch (error) {
      console.error('Error fetching summary:', error);
    }
  };

  return (
    <div className="page">
      <h2>Dashboard</h2>
      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>👥 Total Students</h3>
          <p className="stat-number">{summary.total_students}</p>
        </div>
        <div className="stat-card">
          <h3>📚 Total Batches</h3>
          <p className="stat-number">{summary.total_batches}</p>
        </div>
        <div className="stat-card">
          <h3>👨‍🏫 Total Teachers</h3>
          <p className="stat-number">{summary.total_teachers}</p>
        </div>
        <div className="stat-card">
          <h3>🎥 Total Cameras</h3>
          <p className="stat-number">{summary.total_cameras}</p>
        </div>
        <div className="stat-card">
          <h3>📋 Attendance Records</h3>
          <p className="stat-number">{summary.total_attendance_records}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
