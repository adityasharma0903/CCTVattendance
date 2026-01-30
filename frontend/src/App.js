import React, { useState, useEffect } from 'react';
import './styles/App.css';
import Dashboard from './components/Dashboard';
import StudentManager from './components/StudentManager';
import BatchManager from './components/BatchManager';
import TeacherManager from './components/TeacherManager';
import SubjectManager from './components/SubjectManager';
import CameraManager from './components/CameraManager';
import TimetableManager from './components/TimetableManager';
import AttendanceReport from './components/AttendanceReport';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [apiBase] = useState('http://localhost:8000/api');

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>📸 Face Recognition Attendance System</h1>
          <p>Automated Attendance Tracking with Face Recognition</p>
        </div>
      </header>

      <nav className="sidebar">
        <button 
          className={`nav-btn ${currentPage === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentPage('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={`nav-btn ${currentPage === 'students' ? 'active' : ''}`}
          onClick={() => setCurrentPage('students')}
        >
          👥 Students
        </button>
        <button 
          className={`nav-btn ${currentPage === 'batches' ? 'active' : ''}`}
          onClick={() => setCurrentPage('batches')}
        >
          📚 Batches
        </button>
        <button 
          className={`nav-btn ${currentPage === 'teachers' ? 'active' : ''}`}
          onClick={() => setCurrentPage('teachers')}
        >
          👨‍🏫 Teachers
        </button>
        <button 
          className={`nav-btn ${currentPage === 'subjects' ? 'active' : ''}`}
          onClick={() => setCurrentPage('subjects')}
        >
          📖 Subjects
        </button>
        <button 
          className={`nav-btn ${currentPage === 'cameras' ? 'active' : ''}`}
          onClick={() => setCurrentPage('cameras')}
        >
          🎥 Cameras
        </button>
        <button 
          className={`nav-btn ${currentPage === 'timetable' ? 'active' : ''}`}
          onClick={() => setCurrentPage('timetable')}
        >
          ⏰ Timetable
        </button>
        <button 
          className={`nav-btn ${currentPage === 'attendance' ? 'active' : ''}`}
          onClick={() => setCurrentPage('attendance')}
        >
          📋 Attendance Report
        </button>
      </nav>

      <main className="content">
        {currentPage === 'dashboard' && <Dashboard apiBase={apiBase} />}
        {currentPage === 'students' && <StudentManager apiBase={apiBase} />}
        {currentPage === 'batches' && <BatchManager apiBase={apiBase} />}
        {currentPage === 'teachers' && <TeacherManager apiBase={apiBase} />}
        {currentPage === 'subjects' && <SubjectManager apiBase={apiBase} />}
        {currentPage === 'cameras' && <CameraManager apiBase={apiBase} />}
        {currentPage === 'timetable' && <TimetableManager apiBase={apiBase} />}
        {currentPage === 'attendance' && <AttendanceReport apiBase={apiBase} />}
      </main>
    </div>
  );
}

export default App;
