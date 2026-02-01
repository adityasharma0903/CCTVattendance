import React, { useState, useEffect } from 'react';
import './ExamViolationReport.css';

function ExamViolationReport({ apiBase }) {
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterBy, setFilterBy] = useState('all'); // all, today, teacher, camera
  const [selectedFilter, setSelectedFilter] = useState('');
  const [teachers, setTeachers] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [timetable, setTimetable] = useState([]);
  const [stats, setStats] = useState({
    totalViolations: 0,
    todayViolations: 0,
    uniqueStudents: 0,
    uniqueTeachers: 0
  });

  useEffect(() => {
    fetchViolations();
    fetchTeachers();
    fetchCameras();
    fetchSubjects();
    fetchTimetable();
  }, []);

  const fetchViolations = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${apiBase}/exam-violations`);
      const data = await response.json();
      // Handle both array and object responses
      const violationsArray = Array.isArray(data) ? data : (data.violations || []);
      setViolations(violationsArray);
      calculateStats(violationsArray);
    } catch (error) {
      console.error('Error fetching violations:', error);
      setViolations([]);
    } finally {
      setLoading(false);
    }
  };;

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

  const fetchSubjects = async () => {
    try {
      const response = await fetch(`${apiBase}/subjects`);
      const data = await response.json();
      setSubjects(data);
    } catch (error) {
      console.error('Error fetching subjects:', error);
    }
  };

  const fetchTimetable = async () => {
    try {
      const response = await fetch(`${apiBase}/timetable`);
      const data = await response.json();
      setTimetable(Array.isArray(data) ? data : (data.timetable || []));
    } catch (error) {
      console.error('Error fetching timetable:', error);
    }
  };

  const calculateStats = (data) => {
    // Ensure data is an array
    const dataArray = Array.isArray(data) ? data : [];
    
    const today = new Date().toISOString().split('T')[0];
    const todayViolations = dataArray.filter(v => v.timestamp && v.timestamp.startsWith(today)).length;
    const uniqueStudents = new Set(dataArray.map(v => v.student_id)).size;
    const uniqueTeachers = new Set(dataArray.map(v => v.teacher_id)).size;

    setStats({
      totalViolations: dataArray.length,
      todayViolations,
      uniqueStudents,
      uniqueTeachers
    });
  };

  const getFilteredViolations = () => {
    // Ensure violations is an array
    if (!Array.isArray(violations)) {
      return [];
    }

    let filtered = violations;

    if (filterBy === 'today') {
      const today = new Date().toISOString().split('T')[0];
      filtered = filtered.filter(v => v.timestamp.startsWith(today));
    } else if (filterBy === 'teacher' && selectedFilter) {
      filtered = filtered.filter(v => v.teacher_id === selectedFilter);
    } else if (filterBy === 'camera' && selectedFilter) {
      filtered = filtered.filter(v => v.camera_id === selectedFilter);
    }

    return filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  };

  const getTeacherName = (teacherId) => {
    const teacher = teachers.find(t => t.teacher_id === teacherId);
    return teacher ? teacher.name : `Teacher ${teacherId}`;
  };

  const getCameraName = (cameraId) => {
    const camera = cameras.find(c => c.camera_id === cameraId);
    return camera ? (camera.camera_name || camera.name || `Camera ${cameraId}`) : `Camera ${cameraId}`;
  };

  const getCameraRoom = (violation) => {
    // First check if violation has camera_location (from timetable)
    if (violation?.camera_location) {
      return violation.camera_location;
    }
    
    // Then check if violation has camera_name
    if (violation?.camera_name) {
      return violation.camera_name;
    }
    
    // Try to find room from timetable using subject_id
    if (violation?.subject_id) {
      const tt = timetable.find(t => t.subject_id === violation.subject_id);
      if (tt?.room) {
        return tt.room;
      }
    }
    
    // Fallback to camera location
    const cameraId = violation?.camera_id;
    const camera = cameras.find(c => c.camera_id === cameraId);
    if (!camera) {
      return cameraId ? `Room: ${cameraId}` : "Room: Unknown";
    }
    return camera.location || camera.camera_name || camera.name || `Room: ${cameraId}`;
  };

  const getSubjectName = (subjectId) => {
    const subject = subjects.find(s => s.subject_id === subjectId);
    return subject ? subject.subject_name : subjectId;
  };

  const filteredData = getFilteredViolations();

  return (
    <div className="exam-violation-report">
      <div className="report-header">
        <h2>📱 Exam Mode Phone Detection Report</h2>
        <p>Monitor all phone detections during exam sessions</p>
      </div>

      {/* Statistics Cards */}
      <div className="stats-container">
        <div className="stat-card">
          <div className="stat-value">{stats.totalViolations}</div>
          <div className="stat-label">Total Violations</div>
        </div>
        <div className="stat-card highlight">
          <div className="stat-value">{stats.todayViolations}</div>
          <div className="stat-label">Today's Violations</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.uniqueStudents}</div>
          <div className="stat-label">Students Caught</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.uniqueTeachers}</div>
          <div className="stat-label">Invigilators</div>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-section">
        <div className="filter-group">
          <label>Filter by:</label>
          <select 
            value={filterBy} 
            onChange={(e) => {
              setFilterBy(e.target.value);
              setSelectedFilter('');
            }}
          >
            <option value="all">All Violations</option>
            <option value="today">Today's Violations</option>
            <option value="teacher">By Teacher</option>
            <option value="camera">By Camera/Room</option>
          </select>
        </div>

        {filterBy === 'teacher' && (
          <div className="filter-group">
            <label>Select Teacher:</label>
            <select value={selectedFilter} onChange={(e) => setSelectedFilter(e.target.value)}>
              <option value="">-- All Teachers --</option>
              {teachers.map(teacher => (
                <option key={teacher.teacher_id} value={teacher.teacher_id}>
                  {teacher.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {filterBy === 'camera' && (
          <div className="filter-group">
            <label>Select Camera/Room:</label>
            <select value={selectedFilter} onChange={(e) => setSelectedFilter(e.target.value)}>
              <option value="">-- All Cameras --</option>
              {cameras.map(camera => (
                <option key={camera.camera_id} value={camera.camera_id}>
                  {(camera.camera_name || camera.name || camera.camera_id)} ({camera.location || 'Room'})
                </option>
              ))}
            </select>
          </div>
        )}

        <button className="refresh-btn" onClick={fetchViolations}>
          🔄 Refresh
        </button>
      </div>

      {/* Violations Table */}
      <div className="violations-container">
        {loading ? (
          <div className="loading">Loading violations...</div>
        ) : filteredData.length === 0 ? (
          <div className="no-data">No phone detections found</div>
        ) : (
          <div className="table-wrapper">
            <table className="violations-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Student</th>
                  <th>Teacher (Invigilator)</th>
                  <th>Subject</th>
                  <th>Room/Camera</th>
                  <th>Confidence</th>
                  <th>Duration</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((violation, index) => (
                  <tr key={index} className={`violation-row severity-${violation.severity || 'high'}`}>
                    <td className="timestamp">
                      <div className="date">
                        {new Date(violation.timestamp).toLocaleDateString()}
                      </div>
                      <div className="time">
                        {new Date(violation.timestamp).toLocaleTimeString()}
                      </div>
                    </td>
                    <td className="student">
                      <div className="student-id">{violation.student_id}</div>
                      <div className="student-name">{violation.student_name || 'Unknown'}</div>
                    </td>
                    <td className="teacher">
                      <div className="teacher-name">{getTeacherName(violation.teacher_id)}</div>
                      <div className="teacher-id">{violation.teacher_id}</div>
                    </td>
                    <td className="subject">
                      <span className="subject-badge">
                        {getSubjectName(violation.subject_id)}
                      </span>
                    </td>
                    <td className="camera">
                      <div className="camera-name">{getCameraRoom(violation)}</div>
                      <div className="camera-id">{violation.camera_id}</div>
                    </td>
                    <td className="confidence">
                      <div className="confidence-bar">
                        <div 
                          className="confidence-fill" 
                          style={{ width: `${(violation.confidence || 0) * 100}%` }}
                        ></div>
                      </div>
                      <div className="confidence-text">
                        {((violation.confidence || 0) * 100).toFixed(0)}%
                      </div>
                    </td>
                    <td className="duration">
                      {violation.duration_seconds ? `${violation.duration_seconds}s` : 'N/A'}
                    </td>
                    <td className="status">
                      <span className="status-badge alert">
                        🚨 ALERT
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Detailed View */}
      <div className="details-section">
        <h3>📋 Violation Details</h3>
        {filteredData.length === 0 ? (
          <p className="no-details">Select violations to view details</p>
        ) : (
          <div className="details-grid">
            {filteredData.map((violation, index) => (
              <div key={index} className="detail-card">
                <div className="detail-header">
                  <span className="detail-icon">📱</span>
                  <span className="detail-time">
                    {new Date(violation.timestamp).toLocaleString()}
                  </span>
                </div>
                <div className="detail-content">
                  <div className="detail-row">
                    <span className="detail-label">Student:</span>
                    <span className="detail-value">{violation.student_name} ({violation.student_id})</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Invigilator:</span>
                    <span className="detail-value">{getTeacherName(violation.teacher_id)}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Exam Room:</span>
                    <span className="detail-value">{getCameraRoom(violation)}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Subject:</span>
                    <span className="detail-value">{getSubjectName(violation.subject_id)}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Phone Detection Confidence:</span>
                    <span className="detail-value font-bold">
                      {((violation.confidence || 0) * 100).toFixed(1)}%
                    </span>
                  </div>
                  {violation.notes && (
                    <div className="detail-row">
                      <span className="detail-label">Notes:</span>
                      <span className="detail-value">{violation.notes}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ExamViolationReport;
