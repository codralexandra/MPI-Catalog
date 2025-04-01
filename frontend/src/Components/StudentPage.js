import '../Stylesheets/HomePages.css';
import { Course } from '../Models/Course';
import { Student } from '../Models/Student';
import { Assignment } from '../Models/Assignment';

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

function StudentPage() {
  const location = useLocation();
  const email = location.state?.email;
  const student_id = location.state?.student_id;
  const [selectedCourseId, setSelectedCourseId] = useState(null);

  return (
    <div>
       <div className="app-bar">{email}</div>

       <div className="data-wrapper">
         {/* COURSES */}
          <div className="data-individual-wrapper">
            <h2>Courses</h2>
            <div className="data-container" style={{ position: 'static' }}>

            </div>

          </div>

          {/* ASSIGNMENTS */}
          {selectedCourseId && (
            <div className="data-individual-wrapper">
              <h2>Assignments</h2>
              <div className="data-container" style={{ position: 'static' }}>

              </div>

            </div>
          )}

       </div>

    </div>
  );
}

export default StudentPage;