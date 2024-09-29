'use client';
import { Box, Typography } from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";

const ReviewSummary = ({productId}) => {
    const [reviewSummary, setReviewSummary] = useState('');

    useEffect(() => {
        fetchReviewSummary();
    }, []);

    const fetchReviewSummary = async () => {
        try {
            const response = await axios.get(''); // Add API URL here
            setReviewSummary(response.data);
        } catch (error) {
            console.error("Error fetching review summary:", error);
        }
    };

    return (
        <Box
            sx={{
                p: 3,
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
                backgroundColor: '#fafafa',
                maxWidth: 600,
                margin: '20px auto'
            }}
        >
            <Typography
                variant="h5"
                component="div"
                sx={{ fontWeight: 'bold', mb: 2, textAlign: 'center', color: '#333' }}
            >
                What Customers are Saying...
            </Typography>

            <Typography
                variant="body1"
                component="p"
                sx={{ fontSize: '1.2rem', lineHeight: 1.6, textAlign: 'justify', color: '#555' }}
            >
                {reviewSummary || "Loading summary..."} {/* Display a placeholder if data is not yet loaded */}
            </Typography>
        </Box>
    );
}

export default ReviewSummary;
