import React, { useState, useEffect } from 'react';

function AttendanceReport({ apiBase }) {
  const [attendance, setAttendance] = useState([]);
  const [batches, setBatches] = useState([]);
  const [selectedBatch, setSelectedBatch] = useState('');
  const [report, setReport] = useState(null);

  useEffect(() => {
    fetchBatches();
    fetchAllAttendance();
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

  const fetchAllAttendance = async () => {
    try {
      const response = await fetch(`${apiBase}/attendance`);
      const data = await response.json();
      setAttendance(data);
    } catch (error) {
      console.error('Error fetching attendance:', error);
    }
  };

  const handleBatchChange = async (batchId) => {
    setSelectedBatch(batchId);
    if (batchId) {
      try {
        const response = await fetch(`${apiBase}/attendance/report/${batchId}`);
        const data = await response.json();
        setReport(data);
      } catch (error) {
        console.error('Error fetching report:', error);
      }
    }
  };

  return (
    <div className="page">
      <h2>Attendance Report</h2>
      
      <div className="form">
        <label>Select Batch:</label>
        <select 
          value={selectedBatch}
          onChange={(e) => handleBatchChange(e.target.value)}
        >
          <option value="">-- Select Batch --</option>
          {batches.map(batch => (
            <option key={batch.batch_id} value={batch.batch_id}>
              {batch.batch_name}
            </option>
          ))}
        </select>
      </div>

      {report && (
        <div className="report-summary">
          <h3>{report.batch_id} Attendance Summary</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <p>Total Records: <strong>{report.total_records}</strong></p>
            </div>
            <div className="stat-item">
              <p>Present: <strong>{report.present}</strong></p>
            </div>
            <div className="stat-item">
              <p>Absent: <strong>{report.absent}</strong></p>
            </div>
            <div className="stat-item">
              <p>Late: <strong>{report.late}</strong></p>
            </div>
            <div className="stat-item">
              <p>Attendance %: <strong>{report.attendance_percentage.toFixed(2)}%</strong></p>
            </div>
          </div>
        </div>
      )}

      <h3>Attendance Records</h3>
      <table className="data-table">
        <thead>
          <tr>
            <th>Roll Number</th>
            <th>Name</th>
            <th>Camera ID</th>
            <th>Timestamp</th>
            <th>Status</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {(selectedBatch ? attendance.filter(a => a.batch_id === selectedBatch) : attendance).map((record) => (
            <tr key={record.attendance_id}>
              <td>{record.roll_number}</td>
              <td>{record.student_id}</td>
              <td>{record.camera_id}</td>
              <td>{new Date(record.timestamp).toLocaleString()}</td>
              <td>
                <span className={`status-badge ${record.status.toLowerCase()}`}>
                  {record.status}
                </span>
              </td>
              <td>{(record.confidence_score * 100).toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>

      {attendance.length === 0 && <p className="empty-message">No attendance records yet</p>}
    </div>
  );
}

export default AttendanceReport;
