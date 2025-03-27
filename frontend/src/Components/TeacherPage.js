import '../Stylesheets/HomePages.css';
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

const COURSES_FOR_TEACHER_URL = "/course/teacher/get";

function TeacherPage() {
  const location = useLocation();
  const email = location.state?.email;
  const teacher_id = location.state?.teacher_id;

  const [courses, setCourses] = useState([]);

  const loadCourses = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('teacher_id', teacher_id);
      const response = await axiosClient.get(COURSES_FOR_TEACHER_URL, formData);
      
      const data = response.data;
      const loadedCourses = data.map(course => {
        const [id, name] = Object.entries(course)[0];
        return { id, name };
      });

      setCourses(loadedCourses);
    } catch (error) {
      console.error('Error while fetching courses:', error);
      alert('Something went wrong. Please try again.');
    }
  };

  useEffect(() => {
    if (teacher_id) {
      loadCourses();
    }
  }, [teacher_id]);

    return (
      <div>

        <div className="app-bar">{email}</div>

        <div className="data-container" style={{ position: 'static' }}>
          <h2>Courses</h2>
          {courses.map((course) => (
            <button key={course.id} className="data-button"> {course.name} </button>
          ))}
        </div>

      </div>
    );
  }
  
  export default TeacherPage;