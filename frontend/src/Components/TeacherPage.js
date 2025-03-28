import '../Stylesheets/HomePages.css';
import { Course } from '../Models/Course';
import { Student } from '../Models/Student';
import { Assignment } from '../Models/Assignment';

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

const COURSES_FOR_TEACHER_URL = "/course/teacher/get";
const ASSIGNMENTS_FOR_COURSE_URL = "/course/teacher/get-assignments";

function TeacherPage() {
  const location = useLocation();
  const email = location.state?.email;
  const teacher_id = location.state?.teacher_id;
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [coursesLoaded, setCoursesLoaded] = useState(false);

  const [courses, setCourses] = useState([]);

  const loadCourses = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('teacher_id', teacher_id);
      const response = await axiosClient.post(COURSES_FOR_TEACHER_URL, formData);
      
      const data = response.data;
  
      const loadedCourses = data.map(course => 
        new Course(course.id, course.course_name, [], [])
      );
      
      setCourses(loadedCourses);
      setCoursesLoaded(true); 
    } catch (error) {
      console.error('Error while fetching courses:', error);
      alert('Something went wrong. Please try again.');
    }
  };  

  const loadAssignments = async () => {
    try {
      const updatedCourses = await Promise.all(
        courses.map(async (course) => {
          const formData = new URLSearchParams();
          formData.append('course_id', course.id);
  
          const response = await axiosClient.post(
            ASSIGNMENTS_FOR_COURSE_URL, formData
          );
  
          const data = response.data;
          console.log(`Assignments for ${course.id}:`, data);
  
          const loadedAssignments = data.map((assignment) =>
            new Assignment(assignment._id, assignment.title)
          );
  
          course.assignments = loadedAssignments;

          for(let i = 0; i < course.assignments.length; i++) {
            console.log("Assignment:", course.assignments[i].name);
          }

          return course;
        })
      );
  
      setCourses(updatedCourses);
    } catch (error) {
      console.error('Error while fetching assignments:', error);
      alert('Something went wrong while loading assignments.');
    }
  };  
  
  useEffect(() => {
    const loadData = async () => {
      if (!teacher_id) return;
  
      try {
        // Step 1: load courses
        const formData = new URLSearchParams();
        formData.append('teacher_id', teacher_id);
        const response = await axiosClient.post(COURSES_FOR_TEACHER_URL, formData);
        const data = response.data;
  
        const loadedCourses = data.map(course =>
          new Course(course.id, course.course_name, [], [])
        );
  
        // Step 2: now fetch assignments for each course
        const updatedCourses = await Promise.all(
          loadedCourses.map(async (course) => {
            try {
              const assignmentForm = new URLSearchParams();
              assignmentForm.append('course_id', course.id);
  
              const res = await axiosClient.post(ASSIGNMENTS_FOR_COURSE_URL, assignmentForm);
              const assignmentsData = res.data;
  
              course.assignments = assignmentsData.map(a =>
                new Assignment(a._id, a.title)
              );
  
              return course;
            } catch (err) {
              console.error(`Error loading assignments for course ${course.id}`, err);
              course.assignments = []; // fallback to empty array
              return course;
            }
          })
        );
  
        setCourses(updatedCourses);
  
      } catch (error) {
        console.error('Error loading courses and assignments:', error);
        alert('Something went wrong while loading your data.');
      }
    };
  
    loadData();
  }, [teacher_id]);
  
  
  const handleCourseClick = (course) => {
    setSelectedCourse(course);
  };  

    return (
      <div>

        <div className="app-bar">{email}</div>

        <div className="data-wrapper">
          {/* COURSES */}
          <div className="data-container" style={{ position: 'static' }}>
            <h2>Courses</h2>
            {courses.map((course, index) => {
                return (
                  <button 
                    key={course?.id || index} 
                    className="data-button"
                    style={{
                      margin: '10px 0',
                      backgroundColor:
                        selectedCourse?.id === course.id
                          ? 'var(--container-button-selected)'
                          : 'var(--container-button)',
                    }}
                    onClick={() => handleCourseClick(course)}
                  >
                    {course.id}
                  </button>
                );
              })}
          </div>

           {/* ASSIGNMENTS */}
           {selectedCourse && Array.isArray(selectedCourse.assignments) && (
            <div className="data-container" style={{ position: 'static' }}>
              <h2>Assignments</h2>
              
              {selectedCourse.assignments.length === 0 ? (
                <p>No assignments yet.</p>
              ) : (
                selectedCourse.assignments.map((assignment) => (
                  <button
                    key={assignment.id}
                    className="data-button"
                  >
                    {assignment.name}
                  </button>
                ))
              )}
            </div>
          )}



        </div>
        

      </div>
    );
  }
  
  export default TeacherPage;