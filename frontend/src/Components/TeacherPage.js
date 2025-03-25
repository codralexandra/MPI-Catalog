import '../Stylesheets/HomePages.css';
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

function TeacherPage() {
  const location = useLocation();
  const email = location.state?.email;
  const teacher_id = location.state?.teacher_id;

    return (
      <div>
        <div className="app-bar">{email}</div>
      </div>
    );
  }
  
  export default TeacherPage;