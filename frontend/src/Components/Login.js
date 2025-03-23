import '../Stylesheets/LoginRegister.css';
import { useRef, useState, useEffect } from "react";

function Login() {

    const loginRef = useRef();

    const [login, setLogin] = useState("");
    const [pwd, setPwd] = useState("");

    useEffect(() => {
        loginRef.current.focus();
    }, []);

    useEffect(() =>{
        setLogin(login);
        console.log("Email", login);
        setPwd(pwd);
        console.log("Password", pwd);
    },[login,pwd])


    const handleLogin = (e) => {
        // Here data will be sent to backend for confirmation of credentials.
    }

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