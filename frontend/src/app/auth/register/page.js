'use client';

import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Dialog, DialogContent, CircularProgress, DialogTitle, DialogActions, Toolbar } from '@mui/material';
import axios from 'axios';

const RegistrationForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        contact: '',
        address: '',
        roles: [3]
    });

    const [openProgressModal, setOpenProgressModal] = useState(false); // For progress dialog
    const [openSuccessModal, setOpenSuccessModal] = useState(false);   // For success dialog
    const [error, setError] = useState('');
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        setOpenProgressModal(true); // Show progress modal
        setError('');  // Reset any previous error

        try {
            // Make API request to the backend
            const response = await axios.post('http://localhost:5000/api/v1/users', formData);

            // Close progress modal and show success modal
            setOpenProgressModal(false);
            setOpenSuccessModal(true);

        } catch (error) {
            setError(error.response.data.error);
            setOpenProgressModal(false);  // Close progress modal in case of error
        }
    };

    const handleCloseSuccessModal = () => {
        setOpenSuccessModal(false);  // Close the success modal when "OK" is clicked
    };

    return (
        <Box>
            <Toolbar />

            <Box
                component="form"
                sx={{ maxWidth: '400px', margin: 'auto', mt: 5, display: 'flex', flexDirection: 'column', gap: 2 }}
                onSubmit={handleSubmit}
            >
                <Typography variant="h5" align="left">Create Account</Typography>

                <TextField
                    label="Username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    fullWidth
                    size='small'
                />

                <TextField
                    label="Email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    fullWidth
                    size='small'
                />

                <TextField
                    label="Password"
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    fullWidth
                    size='small'
                />

                <TextField
                    label="Contact"
                    name="contact"
                    value={formData.contact}
                    onChange={handleChange}
                    required
                    fullWidth
                    size='small'
                />

                <TextField
                    label="Address"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    fullWidth
                    multiline
                    size='small'
                />

                {error && <Typography color="error">{error}</Typography>}

                <Box display="flex" justifyContent="center">
                    <Button variant="contained" type="submit" sx={{
                        width: '75%', backgroundColor: '#f0c14b', color: 'black', '&:hover': {
                            backgroundColor: '#E4B747' // Optional: Change color on hover
                        }
                    }}>
                        Register
                    </Button>
                </Box>
                <Dialog open={openProgressModal}>
                    <DialogContent style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        <CircularProgress /> {/* Show a spinner */}
                        <p style={{ marginLeft: '10px' }}>Submitting, please wait...</p>
                    </DialogContent>
                </Dialog>

                {/* Success Modal */}
                <Dialog open={openSuccessModal} onClose={handleCloseSuccessModal}>
                    <DialogTitle>Success</DialogTitle>
                    <DialogContent>
                        <p>Registration was successful!</p>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseSuccessModal}>OK</Button>
                    </DialogActions>
                </Dialog>
            </Box>
        </Box>

    );
};

export default RegistrationForm;
