import { Box, List, Typography } from "@mui/material";
import React, { useState, useEffect } from "react";
import ReviewCard from "./ReviewCard";
import axios from "axios";

// product_id will be passed as a URL Parameter
const ReviewList = ({ productId }) => {
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        fetchReviews();
    }, []);

    const fetchReviews = async () => {
        const response = await axios.get(`http://127.0.0.1:5000/api/v1/products/${productId}/reviews`);
        console.log(response.data);
        setReviews(response.data);
    };

    const handleUpvote = async (selectedReview) => {

    }

    const handleDownvote = async (selectedReview) => {

    }


    return (
        <Box sx={{ padding: 2 }}>
            {/* Gemini Generated summary of top 100 reviews */}
            <Typography variant="h6" sx={{ marginBottom: 3 }}>
                Customer Reviews
            </Typography>
            <List sx={{ paddingBottom: 4 }}>
                {reviews.map((review, idx) => (
                    <Box key={idx} sx={{ marginBottom: 3 }}>
                        <ReviewCard
                            review={review}
                            onUpvote={handleUpvote}
                            onDownvote={handleDownvote}
                            sx={{ width: '60%' }}
                        />
                    </Box>
                ))}
            </List>
        </Box>
    )
}

export default ReviewList;