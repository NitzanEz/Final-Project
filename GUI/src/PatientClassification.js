import React, { useState, useEffect } from 'react';
import { Button, Form, Container, Row, Col } from 'react-bootstrap';
import { useDropzone } from 'react-dropzone';
import axios from 'axios'; // Install axios for making requests
import './PatientClassification.css'; // Import the updated CSS
import Logo from "./logo1.png";

const PatientClassification = () => {
    const [patientId, setPatientId] = useState('');
    const [patients, setPatients] = useState([]);
    const [patientInfo, setPatientInfo] = useState(null);
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('');
    const [classificationResult, setClassificationResult] = useState(null);

    useEffect(() => {
        fetch('/patients.json')
            .then(response => response.json())
            .then(data => setPatients(data))
            .catch(error => console.error('Error loading patient data:', error));
    }, []);

    const handleSearchPatient = (e) => {
        e.preventDefault();
        const foundPatient = patients.find(patient => patient.id === patientId);
        if (foundPatient) {
            setPatientInfo(foundPatient);
            setStatus('');
        } else {
            setPatientInfo(null);
            setStatus('Patient not found');
        }
    };

    const { getRootProps, getInputProps } = useDropzone({
        onDrop: acceptedFiles => {
            setFile(acceptedFiles[0]);
            setStatus('File uploaded successfully!');
        }
    });

    const handleFileUpload = async () => {
        if (file) {
            setStatus('Classifying...');
            
            const formData = new FormData();
            formData.append('file', file);

            try {
                // Send the file to the backend
                const response = await axios.post('http://localhost:5000/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                });

                // Handle the classification result from the backend
                setClassificationResult(response.data.prediction);
                setStatus('');
            } catch (error) {
                console.error('Error during classification:', error);
                setStatus('Error during classification');
            }
        }
    };

    return (
        <Container className="patient-container">
            {/* Logo in Top-Left */}
            <div className="logo-container">
                <img src={Logo} alt="ScanMed Logo" className="logo-image" />
            </div>

            {/* Main Layout */}
            <div className="content-wrapper">
                {/* Search Patient - Left Side */}
                <div className="patient-search">
                    <h2>Search Patient</h2>
                    <Form onSubmit={handleSearchPatient}>
                        <Form.Group controlId="formPatientId">
                            <Form.Label>Patient ID</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Enter patient ID"
                                value={patientId}
                                onChange={e => setPatientId(e.target.value)}
                            />
                        </Form.Group>
                        <Button variant="primary" type="submit">Search</Button>
                    </Form>

                    {status && <p style={{ color: 'red' }}>{status}</p>}

                    {patientInfo && (
                        <div>
                            <h4>Patient Details</h4>
                            <p><strong>Name:</strong> {patientInfo.firstName} {patientInfo.lastName}</p>
                            <p><strong>ID:</strong> {patientInfo.id}</p>
                            <p><strong>Test History:</strong> {patientInfo.testHistory.join(', ')}</p>
                        </div>
                    )}
                </div>

                {/* Upload File - Right Side */}
                <div className="file-upload-wrapper">
                    <h2>Upload NII File</h2>
                    <div className="file-upload" {...getRootProps()}>
                        <input {...getInputProps()} />
                        <p>Drag 'n' drop files here, or click to select</p>
                    </div>
                    {file && <p className="uploaded-file">Uploaded: {file.name}</p>}
                </div>
            </div>

            {/* Classification Results - Below Upload */}
            <div className="results-container">
                <h2>Results</h2>
                <p>{classificationResult || 'Results will appear here after classification.'}</p>
            </div>

            {/* Button to trigger classification */}
            <Button onClick={handleFileUpload}>Classify MRI</Button>
        </Container>
    );
};

export default PatientClassification;
