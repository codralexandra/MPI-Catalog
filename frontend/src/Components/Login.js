import '../Stylesheets/FormPages.css';
import { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

const LOGIN_URL = "/login";
const STUDENT_URL = "/home";
const TEACHER_URL = "/home-admin";
const RESET_PASSWORD_URL = "/reset-password";

function Login() {

    const loginRef = useRef();

    const [login, setLogin] = useState("");
    const [pwd, setPwd] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const emailRegex = /^[a-zA-Z.]+@unitbv\.ro$/;

    useEffect(() => {
        loginRef.current.focus();
    }, []);

    useEffect(() =>{
        setLogin(login);
        setPwd(pwd);
    },[login,pwd])


    const handleLogin = async (e) => {
        e.preventDefault();

        if(!emailRegex.test(login)){
            setError("Please enter a valid email address.");
            return;
        }

        setError("");

        try {
            const formData = new URLSearchParams();
            formData.append('login', login);
            formData.append('pwd', pwd);

            const response = await axiosClient.post(LOGIN_URL,formData);
            
            const data = response.data;
            const role = data.role;
            
            if (role === 'student') {
                navigate(STUDENT_URL);
            } else if (role === 'teacher') {
                navigate(TEACHER_URL);
            } else {
                alert("Unknown role");
            }
            
        } catch (error) {
            console.error('Error during login:', error);
            alert('Something went wrong. Please try again.');
        }
    };

    const resetPassword = () => {
        navigate(RESET_PASSWORD_URL);
    }

    return (
        <section>
            <h1 className="heading">Gradebook: Login</h1>
            <section className="form-container">
            <form onSubmit={handleLogin} className="form">
                <div className="input-group">
                    <label htmlFor="login">Email:</label>
                    <input
                        type="text"
                        id="login"
                        ref={loginRef}
                        autoComplete="off"
                        onChange={(e) => setLogin(e.target.value)}
                        value={login}
                        required
                    />
                </div>

                {error && <div className="error-message">{error}</div>}

                <div className="input-group">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        onChange={(e) => setPwd(e.target.value)}
                        value={pwd}
                        required
                    />
                </div>
                <button onClick={resetPassword}className="reset-button">Forgot password?</button>
                <br></br>
                <button className="form-button">Login</button>
            </form>
        </section>
        </section>
    );
  }
  
  export default Login;