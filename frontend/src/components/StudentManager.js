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
  const [selectedImages, setSelectedImages] = useState({
    front: null,
    left: null,
    right: null,
    far: null
  });
  const [imagePreviews, setImagePreviews] = useState({
    front: null,
    left: null,
    right: null,
    far: null
  });
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

  const validateImage = (file) => {
    if (!file.type.startsWith('image/')) {
      alert('❌ Please select only image files');
      return false;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert('❌ Each image should be less than 5MB');
      return false;
    }
    return true;
  };

  const handleImageChange = (key) => (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) {
      return;
    }

    if (!validateImage(file)) {
      return;
    }

    if (imagePreviews[key]) {
      URL.revokeObjectURL(imagePreviews[key]);
    }

    setSelectedImages(prev => ({
      ...prev,
      [key]: file
    }));

    setImagePreviews(prev => ({
      ...prev,
      [key]: URL.createObjectURL(file)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedImages.front || !selectedImages.left || !selectedImages.right || !selectedImages.far) {
      alert('❌ Please select all 4 photos: front, left, right, far');
      return;
    }
    
    setUploading(true);
    
    try {
      // Create FormData for multipart/form-data upload
      const uploadData = new FormData();
      uploadData.append('front_image', selectedImages.front);
      uploadData.append('left_image', selectedImages.left);
      uploadData.append('right_image', selectedImages.right);
      uploadData.append('far_image', selectedImages.far);
      uploadData.append('student_id', `STU_${formData.roll_number}`);
      uploadData.append('roll_number', formData.roll_number);
      uploadData.append('name', formData.name);
      uploadData.append('batch_id', formData.batch_id);
      if (formData.email) {
        uploadData.append('email', formData.email);
      }
      
      const response = await fetch(`${apiBase}/students/upload-images`, {
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
        Object.values(imagePreviews).forEach((url) => {
          if (url) {
            URL.revokeObjectURL(url);
          }
        });
        setSelectedImages({
          front: null,
          left: null,
          right: null,
          far: null
        });
        setImagePreviews({
          front: null,
          left: null,
          right: null,
          far: null
        });
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
              Student Photos * (Front, Left, Right, Far)
            </label>
            <div style={{display: 'grid', gap: '10px'}}>
              <div>
                <label style={{display: 'block', marginBottom: '5px'}}>Front *</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange('front')}
                  required
                  style={{width: '100%', padding: '10px'}}
                />
              </div>
              <div>
                <label style={{display: 'block', marginBottom: '5px'}}>Left *</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange('left')}
                  required
                  style={{width: '100%', padding: '10px'}}
                />
              </div>
              <div>
                <label style={{display: 'block', marginBottom: '5px'}}>Right *</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange('right')}
                  required
                  style={{width: '100%', padding: '10px'}}
                />
              </div>
              <div>
                <label style={{display: 'block', marginBottom: '5px'}}>Far *</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange('far')}
                  required
                  style={{width: '100%', padding: '10px'}}
                />
              </div>
            </div>
            <small style={{color: '#666'}}>
              📸 Upload 4 clear face photos (front, left, right, far). Max 5MB each.
            </small>
          </div>

          {(imagePreviews.front || imagePreviews.left || imagePreviews.right || imagePreviews.far) && (
            <div style={{marginBottom: '15px', textAlign: 'center'}}>
              <p style={{fontWeight: 'bold', marginBottom: '10px'}}>Preview:</p>
              <div style={{display: 'flex', gap: '10px', justifyContent: 'center', flexWrap: 'wrap'}}>
                {[
                  { key: 'front', label: 'Front' },
                  { key: 'left', label: 'Left' },
                  { key: 'right', label: 'Right' },
                  { key: 'far', label: 'Far' }
                ].map((item) => (
                  imagePreviews[item.key] ? (
                    <div key={item.key} style={{textAlign: 'center'}}>
                      <img
                        src={imagePreviews[item.key]}
                        alt={`${item.label} preview`}
                        style={{
                          width: '90px',
                          height: '90px',
                          border: '2px solid #007bff',
                          borderRadius: '8px',
                          objectFit: 'cover'
                        }}
                      />
                      <div style={{fontSize: '12px', color: '#666', marginTop: '4px'}}>{item.label}</div>
                    </div>
                  ) : null
                ))}
              </div>
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
                {(student.image_url || (student.image_urls && student.image_urls.length > 0)) ? (
                  <img 
                    src={student.image_url || student.image_urls[0]} 
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
