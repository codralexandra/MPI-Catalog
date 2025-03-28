import { Student } from './Student';
import { Assignment } from './Assignment';

export class Course {
  constructor(id, name, students = [], assignments = []) {
    this.id = id;
    this.name = name;
    this.students = students.map(
      (s) => (s instanceof Student ? s : new Student(s.id, s.name))
    );
    this.assignments = assignments.map(
      (a) => (a instanceof Assignment ? a : new Assignment(a.id, a.name))
    );
  }

  addStudent(student) {
    this.students.push(student);
  }

  addAssignment(assignment) {
    this.assignments.push(assignment);
  }

  removeStudentById(id) {
    this.students = this.students.filter((s) => s.id !== id);
  }

  removeAssignmentById(id) {
    this.assignments = this.assignments.filter((a) => a.id !== id);
  }
}