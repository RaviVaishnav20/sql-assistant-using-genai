//// src/components/Settings.js
//
//import React, { useState } from 'react';
//import axios from 'axios';
//
//function Settings({ onSettingsUpdate }) {
//  const [settings, setSettings] = useState({
//    DB_TYPE: '',
//    DB_HOST: '',
//    DB_PORT: '',
//    DB_NAME: '',
//    DB_USER: '',
//    DB_PASSWORD: '',
//  });
//
//  const [error, setError] = useState('');
//  const [file, setFile] = useState(null);
//
//  const handleChange = (e) => {
//    setSettings({ ...settings, [e.target.name]: e.target.value });
//    setError('');
//  };
//
//  const handleFileChange = (e) => {
//    setFile(e.target.files[0]);
//  };
//
//  const handleSubmit = async (e) => {
//    e.preventDefault();
//
//    const emptyFields = Object.keys(settings).filter(key => !settings[key]);
//    if (emptyFields.length > 0) {
//      setError(`Please fill in all fields. Missing: ${emptyFields.join(', ')}`);
//      return;
//    }
//
//    try {
//      const response = await axios.post('http://localhost:8000/update_settings', settings);
//      alert(response.data.message);
//
//      // If a file is selected, upload it after settings update
//      if (file) {
//        const formData = new FormData();
//        formData.append('database', file);
//
//        try {
//          await axios.post('http://localhost:8000/upload_database', formData, {
//            headers: {
//              'Content-Type': 'multipart/form-data'
//            }
//          });
//          alert('Database uploaded successfully');
//        } catch (error) {
//          console.error('Error uploading database:', error);
//          alert('Failed to upload database');
//        }
//      }
//
//      // Callback to inform parent component (App.js) that settings are updated
//      if (onSettingsUpdate) {
//        onSettingsUpdate(settings);
//      }
//    } catch (error) {
//      console.error('Error updating settings:', error);
//      alert(error.response?.data?.error || 'Failed to update settings');
//    }
//  };
//
//  return (
//    <form onSubmit={handleSubmit} className="settings-form">
//      <div>
//        <label htmlFor="DB_TYPE">Database Type:</label>
//        <select
//          id="DB_TYPE"
//          name="DB_TYPE"
//          value={settings.DB_TYPE}
//          onChange={handleChange}
//          required
//        >
//          <option value="">Select Database Type</option>
//          <option value="SQL">SQL (PostgreSQL)</option>
//          <option value="NoSQL">NoSQL (MongoDB)</option>
//        </select>
//      </div>
//      {Object.keys(settings).filter(key => key !== 'DB_TYPE').map(key => (
//        <div key={key}>
//          <label htmlFor={key}>{key}:</label>
//          <input
//            id={key}
//            type={key.includes('PASSWORD') ? 'password' : 'text'}
//            name={key}
//            value={settings[key]}
//            onChange={handleChange}
//            required
//          />
//        </div>
//      ))}
//      <div className="database-upload">
//        <label htmlFor="file-upload">
//          Choose Database File (Optional)
//        </label>
//        <input
//          id="file-upload"
//          type="file"
//          onChange={handleFileChange}
//          accept=".db,.sqlite,.csv,.xls,.xlsx,.json"
//        />
//        {file && <p>Selected file: {file.name}</p>}
//      </div>
//      {error && <p className="error-message">{error}</p>}
//      <button type="submit">Update Settings</button>
//    </form>
//  );
//}
//
//export default Settings;
// src/components/Settings.js

//import React, { useState } from 'react';
//import axios from 'axios';
//import { TailSpin } from 'react-loader-spinner'; // Example loader
//
//function Settings({ onSettingsUpdate }) {
//  const [settings, setSettings] = useState({
//    DB_TYPE: '',
//    DB_HOST: '',
//    DB_PORT: '',
//    DB_NAME: '',
//    DB_USER: '',
//    DB_PASSWORD: '',
//  });
//
//  const [error, setError] = useState('');
//  const [file, setFile] = useState(null);
//  const [isUploading, setIsUploading] = useState(false);
//
//  const handleChange = (e) => {
//    setSettings({ ...settings, [e.target.name]: e.target.value });
//    setError('');
//  };
//
//  const handleFileChange = (e) => {
//    setFile(e.target.files[0]);
//  };
//
//  const handleSubmit = async (e) => {
//    e.preventDefault();
//
//    const emptyFields = Object.keys(settings).filter(key => !settings[key]);
//    if (emptyFields.length > 0) {
//      setError(`Please fill in all fields. Missing: ${emptyFields.join(', ')}`);
//      return;
//    }
//
//    setIsUploading(true); // Start loader
//
//    try {
//      // Upload the file first if it exists
//      if (file) {
//        const formData = new FormData();
//        formData.append('database', file);
//
//        await axios.post('http://localhost:8000/upload_database', formData, {
//          headers: {
//            'Content-Type': 'multipart/form-data'
//          }
//        });
//        console.log('Database file uploaded successfully.');
//      }
//
//      // Update settings
//      const response = await axios.post('http://localhost:8000/update_settings', settings);
//      alert(response.data.message);
//
//      // Callback to inform parent component (App.js) that settings are updated
//      if (onSettingsUpdate) {
//        onSettingsUpdate(settings);
//      }
//    } catch (error) {
//      console.error('Error during settings update or file upload:', error);
//      alert(error.response?.data?.error || 'Failed to update settings or upload database');
//    } finally {
//      setIsUploading(false); // Stop loader
//    }
//  };
//
//  return (
//    <form onSubmit={handleSubmit} className="settings-form">
//      <div>
//        <label htmlFor="DB_TYPE">Database Type:</label>
//        <select
//          id="DB_TYPE"
//          name="DB_TYPE"
//          value={settings.DB_TYPE}
//          onChange={handleChange}
//          required
//        >
//          <option value="">Select Database Type</option>
//          <option value="SQL">SQL (PostgreSQL)</option>
//          <option value="NoSQL">NoSQL (MongoDB)</option>
//        </select>
//      </div>
//      {Object.keys(settings).filter(key => key !== 'DB_TYPE').map(key => (
//        <div key={key}>
//          <label htmlFor={key}>{key}:</label>
//          <input
//            id={key}
//            type={key.includes('PASSWORD') ? 'password' : 'text'}
//            name={key}
//            value={settings[key]}
//            onChange={handleChange}
//            required
//          />
//        </div>
//      ))}
//      <div className="database-upload">
//        <label htmlFor="file-upload">
//          Choose Database File (Optional)
//        </label>
//        <input
//          id="file-upload"
//          type="file"
//          onChange={handleFileChange}
//          accept=".db,.sqlite,.csv,.xls,.xlsx,.json"
//        />
//        {file && <p>Selected file: {file.name}</p>}
//      </div>
//      {error && <p className="error-message">{error}</p>}
//      <button type="submit" disabled={isUploading}>
//        {isUploading ? 'Processing...' : 'Update Settings'}
//      </button>
//      {isUploading && (
//        <div className="loader">
//          <TailSpin
//            height="50"
//            width="50"
//            color="#4fa94d"
//            ariaLabel="tail-spin-loading"
//            radius="1"
//            visible={true}
//          />
//          <p>Uploading and setting up the database. Please wait...</p>
//        </div>
//      )}
//    </form>
//  );
//}
//
//export default Settings;

// src/components/Settings.js

import React, { useState } from 'react';
import axios from 'axios';
import { TailSpin } from 'react-loader-spinner'; // Example loader

function Settings({ onSettingsUpdate }) {
  const [settings, setSettings] = useState({
    DB_TYPE: '',
    DB_HOST: '',
    DB_PORT: '',
    DB_NAME: '',
    DB_USER: '',
    DB_PASSWORD: '',
  });

  const [error, setError] = useState('');
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleChange = (e) => {
    setSettings({ ...settings, [e.target.name]: e.target.value });
    setError('');
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const emptyFields = Object.keys(settings).filter(key => !settings[key]);
    if (emptyFields.length > 0) {
      setError(`Please fill in all fields. Missing: ${emptyFields.join(', ')}`);
      return;
    }

    setIsUploading(true); // Start loader

    try {
      // Upload the file first if it exists
      if (file) {
        const formData = new FormData();
        formData.append('database', file);

        await axios.post('http://localhost:8000/upload_database', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Database file uploaded successfully.');
      }

      // Update settings
      const response = await axios.post('http://localhost:8000/update_settings', settings);
      alert(response.data.message);

      // Callback to inform parent component (App.js) that settings are updated
      if (onSettingsUpdate) {
        onSettingsUpdate(settings);
      }
    } catch (error) {
      console.error('Error during settings update or file upload:', error);
      alert(error.response?.data?.error || 'Failed to update settings or upload database');
    } finally {
      setIsUploading(false); // Stop loader
    }
  };

  return (
    <form onSubmit={handleSubmit} className="settings-form">
      <div>
        <label htmlFor="DB_TYPE">Database Type:</label>
        <select
          id="DB_TYPE"
          name="DB_TYPE"
          value={settings.DB_TYPE}
          onChange={handleChange}
          required
        >
          <option value="">Select Database Type</option>
          <option value="SQL">SQL (PostgreSQL)</option>
          <option value="NoSQL">NoSQL (MongoDB)</option>
        </select>
      </div>
      {Object.keys(settings).filter(key => key !== 'DB_TYPE').map(key => (
        <div key={key}>
          <label htmlFor={key}>{key}:</label>
          <input
            id={key}
            type={key.includes('PASSWORD') ? 'password' : 'text'}
            name={key}
            value={settings[key]}
            onChange={handleChange}
            required
          />
        </div>
      ))}
      <div className="database-upload">
        <label htmlFor="file-upload">
          Choose Database File (Optional)
        </label>
        <input
          id="file-upload"
          type="file"
          onChange={handleFileChange}
          accept=".db,.sqlite,.csv,.xls,.xlsx,.json" // Exclude .asc
        />
        {file && <p>Selected file: {file.name}</p>}
      </div>
      {error && <p className="error-message">{error}</p>}
      <button type="submit" disabled={isUploading}>
        {isUploading ? 'Processing...' : 'Update Settings'}
      </button>
      {isUploading && (
        <div className="loader">
          <TailSpin
            height="50"
            width="50"
            color="#4fa94d"
            ariaLabel="tail-spin-loading"
            radius="1"
            visible={true}
          />
          <p>Uploading and setting up the database. Please wait...</p>
        </div>
      )}
    </form>
  );
}

export default Settings;

