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
import MenuItem from '@mui/material/MenuItem';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

const COURSES_FOR_TEACHER_URL = "/course/teacher/get";
const ASSIGNMENTS_FOR_COURSE_URL = "/course/teacher/get-assignments";
const STUDENTS_FOR_COURSE_URL = "/course/teacher/get-students";
const ADD_STUDENT_TO_COURSE_URL = "/course/teacher/add-student";
const REMOVE_STUDENT_FROM_COURSE_URL = "/course/teacher/remove-student";
const ADD_ASSIGNMENT_TO_COURSE_URL = "/course/teacher/add-assignment";
const REMOVE_ASSIGNMENT_FROM_COURSE_URL = "/course/teacher/remove-assignment";

function TeacherPage() {
  const location = useLocation();
  const email = location.state?.email;
  const teacher_id = location.state?.teacher_id;
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [selectedAssignmentId, setSelectedAssignmentId] = useState(null);

  const [courses, setCourses] = useState([]);

  const [assignmentDialogOpen, setAssignmentDialogOpen] = useState(false);
  const [assignmentTitle, setAssignmentTitle] = useState('');
  const [assignmentStartDate, setAssignmentStartDate] = useState(null);
  const [assignmentEndDate, setAssignmentEndDate] = useState(null);

  const [studentDialogOpen, setStudentDialogOpen] = useState(false);
  const [studentFirstName, setStudentFirstName] = useState('');
  const [studentLastName, setStudentLastName] = useState('');

  const [gradeDialogOpen, setGradeDialogOpen] = useState(false);
  const [gradeAssignmentId, setGradeAssignmentId] = useState(null);
  const [gradeStudentId, setGradeStudentId] = useState(null);
  const [gradeValue, setGradeValue] = useState('');
  const GradeValues = ["None", ...Array.from({ length: 10 }, (_, i) => (i + 1).toString())];
  
  {/*HANDLE ASSIGNMENT DATA*/}
  const handleAssignmentDialogOpen = () => {
    setAssignmentDialogOpen(true);
  }

  const handleAssignmentDialogClose = () => {
    setAssignmentDialogOpen(false);
    setAssignmentTitle('');
    setAssignmentStartDate(null);
    setAssignmentEndDate(null);
  };

  const handleAssignmentFormSubmit = (event) => {
    event.preventDefault();
    if (!selectedCourse || !assignmentTitle.trim() || !assignmentStartDate || !assignmentEndDate) return;

    const addAssignment = async () => {
      try{
        const formattedStartDate = dayjs(assignmentStartDate).format('DD.MM.YYYY');
        const formattedEndDate = dayjs(assignmentEndDate).format('DD.MM.YYYY');

        const addAssignmentForm = new URLSearchParams();
        addAssignmentForm.append('course_id', selectedCourse.id);
        addAssignmentForm.append('title', assignmentTitle);
        addAssignmentForm.append('date_start', formattedStartDate);
        addAssignmentForm.append('date_end', formattedEndDate);
        const assignmentRes = await axiosClient.post(ADD_ASSIGNMENT_TO_COURSE_URL, addAssignmentForm);

        const assignmentData = assignmentRes.data;  
        const newAssignment = new Assignment(assignmentData.id, assignmentTitle, formattedStartDate, formattedEndDate);
        setSelectedCourse((prevCourse) => ({
          ...prevCourse,
          assignments: [...prevCourse.assignments, newAssignment],
        }));

      }
      catch(error){
        console.error('Error adding assignment:', error);
        alert('Something went wrong while adding the assignment.');
      }
    }
    addAssignment();
    handleAssignmentDialogClose();
  }

  const handleAssignmentClick = (assignment) => {
    setSelectedAssignmentId(assignment.id);
  };

  const handleRemoveAssignment = () => {
    const removeAssignment = async () => {
      try{
        const removeAssignmentForm = new URLSearchParams();
        removeAssignmentForm.append('course_id', selectedCourse.id);
        removeAssignmentForm.append('assignment_id', selectedAssignmentId);
        const assignmentRes = await axiosClient.post(REMOVE_ASSIGNMENT_FROM_COURSE_URL, removeAssignmentForm);

        setSelectedCourse((prevCourse) => ({
          ...prevCourse,
          assignments: prevCourse.assignments.filter((a) => a.id !== selectedAssignmentId),
        }));
      }
      catch(error){
        console.error('Error removing assignment:', error);
        alert('Something went wrong while removing the assignment.');
      }
    }
    removeAssignment();
  }

  {/*HANDLE STUDENT DATA*/}
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

    const addStudent = async () => {
      try {
        const addStudentForm = new URLSearchParams();
        addStudentForm.append('course_id', selectedCourse.id);
        addStudentForm.append('last_name', studentLastName);
        addStudentForm.append('first_name', studentFirstName);
        const studentRes = await axiosClient.post(ADD_STUDENT_TO_COURSE_URL, addStudentForm);
      
        const studentData = studentRes.data;
        const newStudent = new Student(studentData.id, studentFirstName, studentLastName);
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

  const handleStudentClick = (student) => {
    setSelectedStudentId(student.id);
  };

  const handleRemoveStudent = () => {
    const removeStudent = async () => {
      try {
        const removeStudentForm = new URLSearchParams();
        removeStudentForm.append('course_id', selectedCourse.id);
        removeStudentForm.append('student_id', selectedStudentId);
        const studentRes = await axiosClient.post(REMOVE_STUDENT_FROM_COURSE_URL, removeStudentForm);
  
        setSelectedCourse((prevCourse) => ({
          ...prevCourse,
          students: prevCourse.students.filter((s) => s.id !== selectedStudentId)
        }));
        
      }
      catch (error) {
        console.error('Error removing student:', error);
        alert('Something went wrong while removing the student.');
      }
    }
    removeStudent();
  }

  {/*HANDLE GRADE DATA*/}

  const handleGradeDialogOpen = () => {  
    setGradeDialogOpen(true);
  }

  const handleGradeDialogClose = () => {
    setGradeDialogOpen(false);
    setGradeAssignmentId(null);
    setGradeStudentId(null);
    setGradeValue('');
  }

  const handleGradeFormSubmit = (event) => {
    event.preventDefault();
    
    handleGradeDialogClose();
  }


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

    {/*GET ASSIGNMENTS FOR SELECTED COURSE*/}
    try {
      const assignmentForm = new URLSearchParams();
      assignmentForm.append('course_id', course.id);
      const assignmentRes = await axiosClient.post(ASSIGNMENTS_FOR_COURSE_URL, assignmentForm);
  
      const assignmentData = assignmentRes.data;
      updatedCourse.assignments = assignmentData.map(
        (a) => new Assignment(a.id, a.title, a.date_start, a.date_end)
      );

    } catch (error) {
      console.error(`Failed to load assignments for course ${course.id}`, error);
      updatedCourse.assignments = [];
    }
    {/*GET STUDENTS FOR SELECTED COURSE*/}
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
    setSelectedAssignmentId(null);
  };  

  return (
    <div>
      <div className="app-bar">{email}</div>

      <div className="data-wrapper">
        {/* COURSES */}
        <div className="data-individual-wrapper">
          <h2>Courses</h2>
            <div className="data-container" style={{ position: 'static' }}>
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
              <div style={{ display: 'flex', gap: '30px', marginTop: '10px' }}>
                  <button className="add-button"  onClick={handleStudentDialogOpen}>+ Add Student to {selectedCourse.name}</button>
                  <button className="grade-add-button" onClick={handleGradeDialogOpen}>MANAGE GRADES for {selectedCourse.name} </button>
              </div>
            )}


        </div>
        

        {/* ASSIGNMENTS */}
        {selectedCourse && Array.isArray(selectedCourse.assignments) && (
          <div className="data-individual-wrapper">
            <h2>Assignments</h2>
            <div className="data-container" style={{ position: 'static' }}>
                {selectedCourse.assignments.length === 0 ? (
                  <p>No assignments yet.</p>
                ) : (
                  selectedCourse.assignments.map((assignment) => (
                    <button
                      key={assignment.id}
                      className="data-button"
                      style={{
                        margin: '10px 0',
                        backgroundColor:
                          selectedAssignmentId === assignment.id
                            ? 'var(--container-button-selected)'
                            : 'var(--container-button)',
                      }}
                      onClick={() => handleAssignmentClick(assignment)}
                    >
                      {assignment.title} <br></br> 
                      <div className="data-button-subtext">
                        Opens on: {assignment.start_date}<br></br> 
                        Due date: {assignment.end_date}
                      </div>
                    </button>
                  ))
                )}
              </div>

              <div style={{ display: 'flex', gap: '30px', marginTop: '10px' }}>
                <button className="add-button" onClick={handleAssignmentDialogOpen}>+ Add Assignment</button>
                {selectedAssignmentId && (
                <button className="add-button" onClick={handleRemoveAssignment}>Delete</button>
                )}
              </div>

          </div>
          
        )}

        {/* STUDENTS */}
        {selectedCourse && Array.isArray(selectedCourse.students) && (
          <div className="data-individual-wrapper">
              <h2>Students</h2>
              <div className="data-container" style={{ position: 'static' }}>
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
                  <button className="add-button" onClick={handleRemoveStudent}>Remove Student</button>
                </>
              )}

          </div>
        )}
      </div>

      {/* STUDENTS FORM */}
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
              readOnly
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

      {/* ASSIGNMENT FORM */}
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <Dialog
          open={assignmentDialogOpen}
          onClose={handleAssignmentDialogClose}
          slotProps={{
            paper: {
              component: 'form',
              onSubmit: handleAssignmentFormSubmit,
              className: 'custom-dialog'
            },
          }}
        >
          <DialogTitle>Add Assignment</DialogTitle>
          <DialogContent>
            <TextField
              margin="dense"
              label="Course"
              fullWidth
              variant="standard"
              value={selectedCourse?.name || ''}
              readOnly
            />

            <TextField
              autoFocus
              required
              margin="dense"
              label="Assignment Title"
              fullWidth
              variant="standard"
              value={assignmentTitle}
              onChange={(e) => setAssignmentTitle(e.target.value)}
            />

            <DatePicker
              label="Start Date"
              value={assignmentStartDate}
              onChange={(newValue) => setAssignmentStartDate(newValue)}
              slotProps={{
                textField: {
                  margin: 'dense',
                  variant: 'standard',
                  fullWidth: true,
                  required: true,
                  inputProps: {
                    readOnly: true
                  },
                },
              }}
            />

            <DatePicker
              label="Due Date"
              value={assignmentEndDate}
              onChange={(newValue) => setAssignmentEndDate(newValue)}
              slotProps={{
                textField: {
                  margin: 'dense',
                  variant: 'standard',
                  fullWidth: true,
                  required: true,
                  inputProps: {
                    readOnly: true
                  },
                },
              }}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleAssignmentDialogClose}>Cancel</Button>
            <Button type="submit">Add</Button>
          </DialogActions>
        </Dialog>
      </LocalizationProvider>

      {/* GRADE MANAGEMENT FORM */}
      <Dialog
        open={gradeDialogOpen}
        onClose={handleGradeDialogClose}
        slotProps={{
          paper:{
          component: 'form',
          onSubmit: handleGradeFormSubmit,
          className: 'custom-dialog',
          },
        }}
       >
        <DialogTitle>Manage Grades for {selectedCourse?.name}</DialogTitle>
        <DialogContent>
          {/* Assignment Dropdown */}
          <FormControl fullWidth margin="dense" variant="standard">
            <InputLabel id="assignment-label">Assignment</InputLabel>
            <Select
              labelId="assignment-label"
              value={gradeAssignmentId || ''}
              onChange={(e) => setGradeAssignmentId(e.target.value)}
              required
            >
              {selectedCourse?.assignments?.map((assignment) => (
                <MenuItem key={assignment.id} value={assignment.id}>
                  {assignment.title}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Student Dropdown */}
          <FormControl fullWidth margin="dense" variant="standard">
            <InputLabel id="student-label">Student</InputLabel>
            <Select
              labelId="student-label"
              value={gradeStudentId || ''}
              onChange={(e) => setGradeStudentId(e.target.value)}
              required
            >
              {selectedCourse?.students?.map((student) => (
                <MenuItem key={student.id} value={student.id}>
                  {student.first_name} {student.last_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Grade Dropdown */}
          <FormControl fullWidth margin="dense" variant="standard">
            <InputLabel id="grade-label">Grade</InputLabel>
            <Select
              labelId="grade-label"
              value={gradeValue}
              onChange={(e) => setGradeValue(e.target.value)}
              required
            >
              {GradeValues.map((val) => (
                <MenuItem key={val} value={val}>
                  {val}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>

        <DialogActions>
          <Button onClick={handleGradeDialogClose}>Cancel</Button>
          <Button type="submit">Save</Button>
        </DialogActions>
      </Dialog>


    </div>
  );
}

export default TeacherPage;