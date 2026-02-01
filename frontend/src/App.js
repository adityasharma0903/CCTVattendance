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
import ExamViolationReport from './components/ExamViolationReport';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const apiBase = 'http://localhost:8000/api';

  const renderPage = () => {
    switch(currentPage) {
      case 'dashboard':
        return <Dashboard apiBase={apiBase} />;
      case 'students':
        return <StudentManager apiBase={apiBase} />;
      case 'batches':
        return <BatchManager apiBase={apiBase} />;
      case 'teachers':
        return <TeacherManager apiBase={apiBase} />;
      case 'subjects':
        return <SubjectManager apiBase={apiBase} />;
      case 'cameras':
        return <CameraManager apiBase={apiBase} />;
      case 'timetable':
        return <TimetableManager apiBase={apiBase} />;
      case 'attendance':
        return <AttendanceReport apiBase={apiBase} />;
      case 'exam-violations':
        return <ExamViolationReport apiBase={apiBase} />;
      default:
        return <Dashboard apiBase={apiBase} />;
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>📸 Face Recognition Attendance System</h1>
          <p>Automated Attendance Tracking with Face Recognition</p>
        </div>
      </header>

      <div className="main-content">
        <aside className="sidebar">
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
            🕐 Timetable
          </button>
          
          <button 
            className={`nav-btn ${currentPage === 'attendance' ? 'active' : ''}`}
            onClick={() => setCurrentPage('attendance')}
          >
            📋 Attendance Report
          </button>
          
          <button 
            className={`nav-btn ${currentPage === 'exam-violations' ? 'active' : ''}`}
            onClick={() => setCurrentPage('exam-violations')}
          >
            📱 Exam Violations
          </button>
        </aside>

        <main className="content">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

export default App;