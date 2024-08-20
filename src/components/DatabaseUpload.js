//// DatabaseUpload.js
//import React, { useState } from 'react';
//import axios from 'axios';
//
//function DatabaseUpload() {
//  const [file, setFile] = useState(null);
//
//  const handleFileUpload = async (e) => {
//    const selectedFile = e.target.files[0];
//    setFile(selectedFile);
//
//    if (selectedFile) {
//      const formData = new FormData();
//      formData.append('database', selectedFile);
//
//      try {
//        const response = await axios.post('http://localhost:8000/upload_database', formData, {
//          headers: {
//            'Content-Type': 'multipart/form-data'
//          }
//        });
//        alert('Database uploaded successfully');
//      } catch (error) {
//        console.error('Error uploading database:', error);
//        alert('Failed to upload database');
//      }
//    }
//  };
//
//  return (
//    <div className="database-upload">
//      <label htmlFor="file-upload">
//        Choose Database File
//      </label>
//      <input
//        id="file-upload"
//        type="file"
//        onChange={handleFileUpload}
//        accept=".db,.sqlite,.csv,.xls,.xlsx,.json"
//      />
//      {file && <p>Selected file: {file.name}</p>}
//    </div>
//  );
//}
//
//export default DatabaseUpload;


// src/components/DatabaseUpload.js
import React, { useState } from 'react';
import axios from 'axios';

function DatabaseUpload() {
  const [file, setFile] = useState(null);

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    if (selectedFile) {
      const formData = new FormData();
      formData.append('database', selectedFile);

      try {
        const response = await axios.post('http://localhost:8000/upload_database', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        alert('Database uploaded successfully');
      } catch (error) {
        console.error('Error uploading database:', error);
        alert('Failed to upload database');
      }
    }
  };

  return (
    <div className="database-upload">
      <label htmlFor="file-upload">
        Choose Database File
      </label>
      <input
        id="file-upload"
        type="file"
        onChange={handleFileUpload}
        accept=".db,.sqlite,.csv,.xls,.xlsx,.json,.asc" // Exclude .asc
      />
      {file && <p>Selected file: {file.name}</p>}
    </div>
  );
}

export default DatabaseUpload;


