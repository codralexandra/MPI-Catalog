import Login from './Components/Login';
import StudentPage from './Components/StudentPage';
import TeacherPage from './Components/TeacherPage';
import ResetPassword from './Components/ResetPassword';
import { BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/login" element={<Login />} />
        <Route path="/home" element={<StudentPage />} />
        <Route path="/home-admin" element={<TeacherPage />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
