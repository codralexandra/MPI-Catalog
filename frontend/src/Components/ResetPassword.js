import '../Stylesheets/FormPages.css';
import { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import axiosClient from '../API/axiosClient';

const LOGIN_URL = "/login";
const RESET_PASSWORD_URL = "/reset-password";

function ResetPassword() {

    const loginRef = useRef();

    const [login, setLogin] = useState("");
    const [oldPwd, setOldPwd] = useState("");
    const [newPwd, setNewPwd] = useState("");
    const [confirmNewPwd, setConfirmPwd] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        loginRef.current.focus();
    }, []);

    useEffect(() =>{
        setLogin(login);
        setOldPwd(oldPwd);
        setNewPwd(newPwd);
        setConfirmPwd(confirmNewPwd);
    },[login,oldPwd,newPwd,confirmNewPwd])


    const handlePasswordChange = async (e) => {
        e.preventDefault();
    
        if (newPwd !== confirmNewPwd) {
            setError("Passwords do not match.");
            alert("Passwords do not match.");
            return;
        }
    
        try {
            const formData = new URLSearchParams();
            formData.append('login', login);
            formData.append('old_pwd', oldPwd);
            formData.append('new_pwd', newPwd);
    
            const response = await axiosClient.post(RESET_PASSWORD_URL, formData);
            setError(response.data.message);
            navigate(LOGIN_URL);

        } catch (error) {
            console.error('Error during login:', error);
            alert('Something went wrong. Please try again.');
        }
    };    

    return (
        <section>
            <h1 className="heading">Reset Password</h1>
            <section className="form-container">
            <form onSubmit={handlePasswordChange} className="form">

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
                    <label htmlFor="old_pwd">Old password:</label>
                    <input
                        type="password"
                        id="old_pwd"
                        onChange={(e) => setOldPwd(e.target.value)}
                        value={oldPwd}
                        required
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="new_pwd">New Password:</label>
                    <input
                        type="password"
                        id="new_pwd"
                        onChange={(e) => setNewPwd(e.target.value)}
                        value={newPwd}
                        required
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="confirm_pwd">Confirm New Password:</label>
                    <input
                        type="password"
                        id="confirm_pwd"
                        onChange={(e) => setConfirmPwd(e.target.value)}
                        value={confirmNewPwd}
                        required
                    />
                </div>
                <br></br>
                <br></br>
                <button className="form-button">Reset</button>
            </form>
        </section>
        </section>
    );
  }
  
  export default ResetPassword;