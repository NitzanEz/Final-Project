import React, { useState, useEffect } from 'react';
import { Button, Form, Container, Spinner } from 'react-bootstrap';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './PatientClassification.css';
import Logo from "./logo1.png";

const PatientClassification = () => {
    const [patientId, setPatientId] = useState('');
    const [patients, setPatients] = useState([]);
    const [patientInfo, setPatientInfo] = useState(null);
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('');
    const [classificationResult, setClassificationResult] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [showErrorModal, setShowErrorModal] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    // Load patients.json from localStorage
    useEffect(() => {
        const storedPatients = localStorage.getItem('patients');
        if (storedPatients) {
            setPatients(JSON.parse(storedPatients));
        } else {
            fetch('/patients.json')
                .then(response => response.json())
                .then(data => {
                    setPatients(data);
                    localStorage.setItem('patients', JSON.stringify(data)); // Save to localStorage
                })
                .catch(error => console.error('Error loading patient data:', error));
        }
    }, []);

    // Search for patient details
    const handleSearchPatient = (e) => {
        e.preventDefault();
        const foundPatient = patients.find(patient => patient.id === patientId);
        if (foundPatient) {
            setPatientInfo(foundPatient);
            setStatus(foundPatient.hasBeenTested ? '' : 'Patient has not been tested yet.');
        } else {
            setPatientInfo(null);
            setStatus('Patient not found.');
        }
    };

    // Handle file selection
    const { getRootProps, getInputProps } = useDropzone({
        onDrop: acceptedFiles => {
            setFile(acceptedFiles[0]);
            setStatus('File uploaded successfully! Please proceed to classify.');
        }
    });

    // Upload and classify file
    const handleFileUpload = async () => {
        if (!patientId) {
            setErrorMessage("Please enter a Patient ID before uploading a file.");
            setShowErrorModal(true);
            return;
        }

        if (!file) {
            setErrorMessage("Please upload a file before starting classification.");
            setShowErrorModal(true);
            return;
        }

        if (!patientInfo) {
            setErrorMessage("Patient not found. Please enter a valid Patient ID.");
            setShowErrorModal(true);
            return;
        }

        setIsProcessing(true);
        setStatus('Uploading file...');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const updatedDiagnosis = response.data.diagnosis;
            const updatedConfidence = (response.data.best_result.confidence * 100);

            // Update patient details after classification
            const updatedPatientInfo = { ...patientInfo };
            updatedPatientInfo.hasBeenTested = true;
            updatedPatientInfo.autismChance = updatedDiagnosis;
            updatedPatientInfo.confidence = updatedConfidence;

            // Update patient in localStorage
            const updatedPatients = patients.map(patient =>
                patient.id === patientId ? updatedPatientInfo : patient
            );

            localStorage.setItem('patients', JSON.stringify(updatedPatients));
            setPatients(updatedPatients);
            setPatientInfo(updatedPatientInfo);
            setClassificationResult(response.data);
            setStatus('Classification complete.');
        } catch (error) {
            console.error('Error during classification:', error);
            setErrorMessage("Wrong file type please insert .nii file");
            setShowErrorModal(true);
            setStatus('');
        } finally {
            setIsProcessing(false);
        }
    };

    // Confirm before saving results
    const confirmSaveResults = () => {
        const userConfirmed = window.confirm("Are you sure you want to save these results?");
        if (userConfirmed) {
            handleSaveResults();
        }
    };

    // Save results to localStorage
    const handleSaveResults = () => {
        if (!classificationResult || !patientId) {
            alert("No classification results to save or Patient ID is missing.");
            return;
        }

        try {
            const storedPatients = localStorage.getItem('patients');
            if (!storedPatients) {
                alert("No patient records found.");
                return;
            }

            let patients = JSON.parse(storedPatients);

            const patientIndex = patients.findIndex(patient => patient.id === patientId);
            if (patientIndex === -1) {
                alert("Patient not found in records.");
                return;
            }

            patients[patientIndex] = {
                ...patients[patientIndex],
                autismChance: classificationResult.diagnosis,
                confidence: (classificationResult.best_result.confidence * 100).toFixed(2),
                hasBeenTested: true
            };

            localStorage.setItem('patients', JSON.stringify(patients));
            alert("Patient results updated successfully.");
        } catch (error) {
            console.error("Error updating patient:", error);
            alert("Failed to update patient records.");
        }
    };

    return (
        <Container className="patient-container">
            <div className="logo-container">
                <img src={Logo} alt="ScanMed Logo" className="logo-image" />
            </div>
            <div className="content-wrapper">
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
                    {patientInfo && (
                        <div>
                            <h4>Patient Details</h4>
                            <p><strong>Name:</strong> {patientInfo.firstName} {patientInfo.lastName}</p>
                            <p><strong>ID:</strong> {patientInfo.id}</p>
                            <p><strong>Autism Detection Chance:</strong> {patientInfo.autismChance || 'Not yet tested'}</p>
                            <p><strong>Confidence Score:</strong> {patientInfo.confidence ? `${patientInfo.confidence}%` : ''}</p>
                        </div>
                    )}
                </div>
                <div className="file-upload-wrapper">
                    <h2>Upload NII File</h2>
                    {!isProcessing ? (
                        <div className="file-upload" {...getRootProps()}>
                            <input {...getInputProps()} />
                            <p>Drag and drop files here, or click to select</p>
                        </div>
                    ) : (
                        <div className="loading-spinner">
                            <Spinner animation="border" className="spinner-border" />
                        </div>
                    )}
                    {file && !isProcessing && <p className="uploaded-file">Uploaded: {file.name}</p>}
                    {status && <p className="upload-status">{status}</p>}

                    <Button onClick={handleFileUpload} variant="success" disabled={isProcessing}>
                        {isProcessing ? "Processing..." : "Classify"}
                    </Button>
                </div>
            </div>
            <div className="results-container">
                <h2>Results</h2>
                {classificationResult && (
                    <div>
                        <p><strong>Prediction:</strong> {classificationResult.diagnosis}</p>
                        <p><strong>Confidence Score:</strong> {(classificationResult.best_result.confidence * 100).toFixed(2)}%</p>
                        <Button variant="primary" onClick={confirmSaveResults}>Save Results</Button>
                    </div>
                )}
            </div>

            {/* Error Modal Popup */}
            {showErrorModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>Error</h2>
                        <p>{errorMessage}</p>
                        <button className="close-button" onClick={() => setShowErrorModal(false)}>OK</button>
                    </div>
                </div>
            )}
        </Container>
    );
};

export default PatientClassification;
