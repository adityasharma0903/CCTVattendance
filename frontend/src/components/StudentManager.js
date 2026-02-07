import React, { useState, useEffect } from 'react';

function StudentManager({ apiBase }) {
  const [students, setStudents] = useState([]);
  const [batches, setBatches] = useState([]);
  const [formData, setFormData] = useState({
    roll_number: '',
    name: '',
    batch_id: '',
    email: ''
  });
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [uploading, setUploading] = useState(false);
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

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('❌ Please select an image file');
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('❌ Image size should be less than 5MB');
        return;
      }
      
      setSelectedImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedImage) {
      alert('❌ Please select a student image');
      return;
    }
    
    setUploading(true);
    
    try {
      // Create FormData for multipart/form-data upload
      const uploadData = new FormData();
      uploadData.append('file', selectedImage);
      uploadData.append('student_id', `STU_${formData.roll_number}`);
      uploadData.append('roll_number', formData.roll_number);
      uploadData.append('name', formData.name);
      uploadData.append('batch_id', formData.batch_id);
      if (formData.email) {
        uploadData.append('email', formData.email);
      }
      
      const response = await fetch(`${apiBase}/students/upload-image`, {
        method: 'POST',
        body: uploadData
        // Don't set Content-Type header - browser will set it with boundary
      });
      
      const result = await response.json();
      
      if (response.ok) {
        fetchStudents();
        setFormData({
          roll_number: '',
          name: '',
          batch_id: '',
          email: ''
        });
        setSelectedImage(null);
        setImagePreview(null);
        setShowForm(false);
        alert(`✅ ${result.message}\n\nImage uploaded to Cloudinary!\nStudent registered with face recognition.`);
      } else {
        alert(`❌ Error: ${result.detail || 'Failed to upload image'}`);
      }
    } catch (error) {
      console.error('Error adding student:', error);
      alert('❌ Error uploading student image. Make sure backend is running.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (rollNumber) => {
    if (window.confirm('Are you sure you want to delete this student?')) {
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
      <h2>📚 Student Management</h2>
      <p style={{color: '#666', marginBottom: '20px'}}>
        Upload student images with face recognition powered by Cloudinary
      </p>
      
      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? '✕ Cancel' : '+ Add New Student'}
      </button>

      {showForm && (
        <form className="form" onSubmit={handleSubmit}>
          <h3>Register New Student</h3>
          
          <div style={{marginBottom: '15px'}}>
            <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>
              Roll Number *
            </label>
            <input
              type="text"
              name="roll_number"
              placeholder="e.g., 101, 102, 2021001"
              value={formData.roll_number}
              onChange={handleInputChange}
              required
              style={{width: '100%'}}
            />
          </div>

          <div style={{marginBottom: '15px'}}>
            <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>
              Student Name *
            </label>
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleInputChange}
              required
              style={{width: '100%'}}
            />
          </div>

          <div style={{marginBottom: '15px'}}>
            <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>
              Batch *
            </label>
            <select
              name="batch_id"
              value={formData.batch_id}
              onChange={handleInputChange}
              required
              style={{width: '100%'}}
            >
              <option value="">Select Batch</option>
              {batches.map(batch => (
                <option key={batch.batch_id} value={batch.batch_id}>
                  {batch.batch_name} - Semester {batch.semester}
                </option>
              ))}
            </select>
          </div>

          <div style={{marginBottom: '15px'}}>
            <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>
              Email (Optional)
            </label>
            <input
              type="email"
              name="email"
              placeholder="student@example.com"
              value={formData.email}
              onChange={handleInputChange}
              style={{width: '100%'}}
            />
          </div>

          <div style={{marginBottom: '15px'}}>
            <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>
              Student Photo * (Face Recognition)
            </label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              required
              style={{width: '100%', padding: '10px'}}
            />
            <small style={{color: '#666'}}>
              📸 Please upload a clear frontal face photo (JPEG/PNG, max 5MB)
            </small>
          </div>

          {imagePreview && (
            <div style={{marginBottom: '15px', textAlign: 'center'}}>
              <p style={{fontWeight: 'bold', marginBottom: '10px'}}>Preview:</p>
              <img 
                src={imagePreview} 
                alt="Preview" 
                style={{
                  maxWidth: '200px', 
                  maxHeight: '200px', 
                  border: '2px solid #007bff',
                  borderRadius: '8px',
                  objectFit: 'cover'
                }}
              />
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-success" 
            disabled={uploading}
            style={{width: '100%', padding: '12px', fontSize: '16px'}}
          >
            {uploading ? '⏳ Uploading & Processing...' : '✅ Register Student with Face Recognition'}
          </button>

          {uploading && (
            <p style={{textAlign: 'center', color: '#007bff', marginTop: '10px'}}>
              🔄 Processing face recognition and uploading to cloud...
            </p>
          )}
        </form>
      )}

      <h3 style={{marginTop: '30px'}}>Registered Students</h3>
      
      <table className="data-table">
        <thead>
          <tr>
            <th>Roll Number</th>
            <th>Name</th>
            <th>Batch</th>
            <th>Email</th>
            <th>Image</th>
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
                {student.image_url ? (
                  <img 
                    src={student.image_url} 
                    alt={student.name}
                    style={{
                      width: '50px',
                      height: '50px',
                      borderRadius: '50%',
                      objectFit: 'cover',
                      border: '2px solid #007bff'
                    }}
                  />
                ) : (
                  <span>No Image</span>
                )}
              </td>
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

      {students.length === 0 && (
        <p className="empty-message">
          No students registered yet. Click "Add New Student" to get started.
        </p>
      )}
    </div>
  );
}

export default StudentManager;
