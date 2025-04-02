import '../Stylesheets/HomePages.css';
import { Course } from '../Models/Course';
import { Student } from '../Models/Student';
import { Assignment } from '../Models/Assignment';

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

const GET_STUDENT_COURSES_URL = '/course/student/get';
const GET_STUDENT_ASSIGNMENTS_URL = '/course/student/get-course-assignments';

function StudentPage() {
  const location = useLocation();
  const email = location.state?.email;
  const student_id = location.state?.student_id;
  const [selectedCourse, setSelectedCourse] = useState(null);

  const [courses, setCourses] = useState([]);

  const handleCourseClick = async (course) => {
    setSelectedCourse(course); 
  
    const updatedCourse = { ...course, assignments: [] };
  
    try {
      const formData = new URLSearchParams();
      formData.append('student_id', student_id);
      formData.append('course_id', course.id);
  
      const response = await axiosClient.post(GET_STUDENT_ASSIGNMENTS_URL, formData);
      const assignmentData = response.data;
  
      updatedCourse.assignments = assignmentData.map(
        a => new Assignment(a.assignment_id, a.assignment_name, a.assignment_start_date, a.assignment_due_date, a.score, a.grade_date)
      );
    } catch (error) {
      console.error(`Error fetching assignments for course ${course.id}`, error);
      updatedCourse.assignments = [];
    }
  
    setCourses(prevCourses =>
      prevCourses.map(c => (c.id === updatedCourse.id ? updatedCourse : c))
    );
  
    setSelectedCourse(updatedCourse);
  };
  

  useEffect(() => {
    const loadCourses = async () => {
      if(!student_id) return;

      try{
        const formData = new URLSearchParams();
        formData.append('student_id', student_id);
        const response = await axiosClient.post(GET_STUDENT_COURSES_URL, formData);
        const data = response.data;

        const courseList = data.map((courseData) => {
          const course = new Course(courseData.course_id, courseData.course_name, [], [], courseData.avg_score);
          return course;
        });

        setCourses(courseList);
      }
      catch(error)
      {
        console.error('Error fetching courses:', error);
        alert('Error fetching courses. Please try again.');
      }

    };
    loadCourses();
  }, [student_id]);

  return (
    <div>
       <div className="app-bar">{email}</div>

       <div className="data-wrapper">
         {/* COURSES */}
          <div className="data-individual-wrapper">
            <h2>Courses</h2>
            <div className="data-container" style={{ position: 'static' }}>
            {courses.length === 0 ? 
                (<p>No courses found</p> )
                : (
                courses.map((course, index) => (
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
                      {course.name}
                      <br></br> 
                      <div className="data-button-subtext">
                        Average Score: {course.avg}
                      </div>
                    </button>
                  ))
                )}
            </div>

          </div>

          {/* ASSIGNMENTS */}
          {selectedCourse && selectedCourse.assignments?.length >= 0 && (
              <div className="data-individual-wrapper">
                <h2>Assignments</h2>
                <div className="data-container" style={{ position: 'static' }}>
                  {selectedCourse.assignments.length === 0 ? (
                    <p>No assignments for this course.</p>
                  ) : (
                    selectedCourse.assignments.map((assignment, index) => (
                      <div key={assignment.id || index} className="data-button" style={{ margin: '10px 0' }}>
                        <strong>{assignment.name}</strong>
                        <br />
                        <div className="data-button-subtext">
                          Grade: {assignment.score} '[' added on {assignment.score_date} ']'
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
       </div>

    </div>
  );
}

export default StudentPage;