import '../Stylesheets/HomePages.css';
import { Course } from '../Models/Course';
import { Student } from '../Models/Student';
import { Assignment } from '../Models/Assignment';

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const COURSES_FOR_TEACHER_URL = "/course/teacher/get";
const ASSIGNMENTS_FOR_COURSE_URL = "/course/teacher/get-assignments";
const STUDENTS_FOR_COURSE_URL = "/course/teacher/get-students";
const ADD_STUDENT_TO_COURSE_URL = "/course/teacher/add-student";

function TeacherPage() {
  const location = useLocation();
  const email = location.state?.email;
  const teacher_id = location.state?.teacher_id;
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [selectedStudentId, setSelectedStudentId] = useState(null);

  const [courses, setCourses] = useState([]);
  const [studentDialogOpen, setStudentDialogOpen] = useState(false);
  const [studentFirstName, setStudentFirstName] = useState('');
  const [studentLastName, setStudentLastName] = useState('');

  const handleStudentDialogOpen = () => {
    setStudentDialogOpen(true);
  }

  const handleStudentDialogClose = () => {
    setStudentDialogOpen(false);
    setStudentFirstName('');
    setStudentLastName('');
  };

  const handleStudentFormSubmit = (event) => {
    event.preventDefault();
    if (!selectedCourse || !studentFirstName.trim() || !studentLastName.trim()) return;
    //course_id, last_name, first_name: IN FORM

    const addStudent = async () => {
      try {
        const addStudentForm = new URLSearchParams();
        addStudentForm.append('course_id', selectedCourse.id);
        addStudentForm.append('last_name', studentLastName);
        addStudentForm.append('first_name', studentFirstName);
        const studentRes = await axiosClient.post(ADD_STUDENT_TO_COURSE_URL, addStudentForm);
      
        const studentData = studentRes.data;
        const newStudent = new Student(studentData.id, studentData.first_name, studentData.last_name);
        setSelectedCourse((prevCourse) => ({
          ...prevCourse,
          students: [...prevCourse.students, newStudent],
        }));
        
      }
      catch (error) {
        console.error('Error adding student:', error);
        alert('Something went wrong while adding the student.');
      }
    };
    addStudent();
    handleStudentDialogClose();
  };

  useEffect(() => {
    const loadCourses = async () => {
      if (!teacher_id) return;

      try {
        const formData = new URLSearchParams();
        formData.append('teacher_id', teacher_id);
        const response = await axiosClient.post(COURSES_FOR_TEACHER_URL, formData);
        const data = response.data;

        const loadedCourses = data.map(course =>
          new Course(course.id, course.course_name, [], [])
        );

        setCourses(loadedCourses);
      } catch (error) {
        console.error('Error loading courses:', error);
        alert('Something went wrong while loading your courses.');
      }
    };

    loadCourses();
  }, [teacher_id]);

  const handleCourseClick = async (course) => {
    setSelectedCourse(course);
    
    const updatedCourse = { ...course, assignments: [], students: [] };
  
    try {
      const assignmentForm = new URLSearchParams();
      assignmentForm.append('course_id', course.id);
      const assignmentRes = await axiosClient.post(ASSIGNMENTS_FOR_COURSE_URL, assignmentForm);
  
      const assignmentData = assignmentRes.data;
      updatedCourse.assignments = assignmentData.map(
        (a) => new Assignment(a.id, a.title)
      );

    } catch (error) {
      console.error(`Failed to load assignments for course ${course.id}`, error);
      updatedCourse.assignments = [];
    }
  
    try {
      const studentForm = new URLSearchParams();
      studentForm.append('course_id', course.id);
      const studentRes = await axiosClient.post(STUDENTS_FOR_COURSE_URL, studentForm);
  
      const studentData = studentRes.data;
      updatedCourse.students = studentData.map(
        (s) => new Student(s.id, s.first_name, s.last_name)
      );

    } catch (error) {
      console.error(`Failed to load students for course ${course.id}`, error);
      updatedCourse.students = [];
    }
  
    setCourses((prevCourses) =>
      prevCourses.map((c) => (c.id === updatedCourse.id ? updatedCourse : c))
    );
  
    setSelectedCourse(updatedCourse);
    setSelectedStudentId(null);
  };  

  const handleStudentClick = (student) => {
    console.log('Selected student:', student);
    setSelectedStudentId(student.id);
  };

  return (
    <div>
      <div className="app-bar">{email}</div>

      <div className="data-wrapper">
        {/* COURSES */}
        <div className="data-individual-wrapper">
            <div className="data-container" style={{ position: 'static' }}>
              <h2>Courses</h2>
              {courses.map((course, index) => (
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
                </button>
              ))}
            </div>
              
            {selectedCourse && (
              <button className="add-button"  onClick={handleStudentDialogOpen}>+ Add Student</button>
            )}

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

        {/* STUDENTS */}
        {selectedCourse && Array.isArray(selectedCourse.students) && (
          <div className="data-individual-wrapper">
              <div className="data-container" style={{ position: 'static' }}>
                <h2>Students</h2>

                {selectedCourse.students.length === 0 ? (
                  <p>No students enrolled yet.</p>
                ) : (
                  selectedCourse?.students.map((student) => (
                    <button
                      key={student.id}
                      className="data-button"
                      style={{
                        margin: '10px 0',
                        backgroundColor:
                          selectedStudentId === student.id
                            ? 'var(--container-button-selected)'
                            : 'var(--container-button)',
                      }}
                      onClick={() => handleStudentClick(student)}
                    >
                      {student.first_name} {student.last_name}
                    </button>
                  ))
                )}
              </div>

              {selectedStudentId && (
                <>
                  <button className="add-button">Remove Student</button>
                </>
              )}

          </div>
        )}
      </div>

      <Dialog
          open={studentDialogOpen}
          onClose={handleStudentDialogClose}
          slotProps={{
            paper: {
              component: 'form',
              onSubmit: handleStudentFormSubmit,
              className: 'custom-dialog'
            },
          }}
        >
          <DialogTitle>Add Student</DialogTitle>
          <DialogContent>
            <TextField
              margin="dense"
              label="Course"
              fullWidth
              variant="standard"
              value={selectedCourse?.name || ''}
            />
            <TextField
              autoFocus
              required
              margin="dense"
              label="Student First Name"
              fullWidth
              variant="standard"
              value={studentFirstName}
              onChange={(e) => setStudentFirstName(e.target.value)}
            />
            <TextField
              autoFocus
              required
              margin="dense"
              label="Student Last Name"
              fullWidth
              variant="standard"
              value={studentLastName}
              onChange={(e) => setStudentLastName(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleStudentDialogClose}>Cancel</Button>
            <Button type="submit">Add</Button>
          </DialogActions>
        </Dialog>
    </div>
  );
}

export default TeacherPage;