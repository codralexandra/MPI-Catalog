import '../Stylesheets/LoginRegister.css';
import { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

const LOGIN_URL = "/login";

function Login() {

    const loginRef = useRef();

    const [login, setLogin] = useState("");
    const [pwd, setPwd] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        loginRef.current.focus();
    }, []);

    useEffect(() =>{
        setLogin(login);
        console.log("Email", login);
        setPwd(pwd);
        console.log("Password", pwd);
    },[login,pwd])


    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const formData = new URLSearchParams();
            formData.append('login', login);
            formData.append('pwd', pwd);

            const response = await axiosClient.post(LOGIN_URL,formData);
            
            const data = response.data;
            const role = data.role;
            
            if (role === 'student') {
                navigate('/home');
            } else if (role === 'teacher') {
                navigate('/home-admin');
            } else {
                alert("Unknown role");
            }
            
        } catch (error) {
            console.error('Error during login:', error);
            alert('Something went wrong. Please try again.');
        }
    };

    return (
        <section>
            <h1 className="login-heading">Gradebook: Login</h1>
            <section className="login-container">
            <form onSubmit={handleLogin} className="login-form">
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
                <br></br>
                <br></br>
                <button className="form-button">Login</button>
            </form>
        </section>
        </section>
    );
  }
  
  export default Login;