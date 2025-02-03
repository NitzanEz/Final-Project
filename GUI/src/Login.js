import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import Logo from "./logo1.png";

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [doctors, setDoctors] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetch('/doctors.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch doctors data');
                }
                return response.json();
            })
            .then(data => setDoctors(data))
            .catch(error => {
                console.error('Error loading doctor data:', error);
                setError('Error loading doctor data');
            });
    }, []);

    const handleLogin = (e) => {
        e.preventDefault();

        const doctor = doctors.find(doc => doc.username === username && doc.password === password);

        if (doctor) {
            setError('');
            //alert('Login successful!');
            navigate('/patient-classification'); // Navigate to PatientClassification
        } else {
            setError('Invalid credentials');
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <img src={Logo} alt="ScanMed Logo" className="logo-image"/>
                <div className="login-card-header">
                    <h2>ScanMed - Login</h2>
                </div>
                <div className="login-card-body">
                    <form onSubmit={handleLogin}>
                        <div className="mb-3">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input
                                type="text"
                                className="form-control"
                                id="username"
                                placeholder="Enter your username"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                required
                            />
                        </div>
                        <div className="mb-4">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input
                                type="password"
                                className="form-control"
                                id="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" className="btn-primary">Login</button>
                        {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
