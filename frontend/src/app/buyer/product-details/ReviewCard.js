import React from 'react';
import { Card, CardContent, CardActions, Typography, IconButton, Box } from '@mui/material';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import Rating from '@mui/material/Rating';
import Stack from '@mui/material/Stack';

const ReviewCard = ({ review, handleUpvote, handleDownvote }) => {

    return (
        <Card sx={{ boxShadow: 3, borderRadius: 3, padding: 2, backgroundColor: '#f9f9f9' }}>
            <CardContent sx={{ paddingBottom: 0 }}>
                {/* Username */}
                <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', marginBottom: 1 }}>
                    {review.user.username}
                </Typography>

                {/* Rating (Stars) */}
                <Stack spacing={1} direction="row" alignItems="center" sx={{ marginBottom: 1 }}>
                    <Rating name='review-rating' precision={0.5} size='small' value={review.rating} readOnly />
                    <Typography variant="body2" color="text.secondary">
                        {review.rating.toFixed(1)} / 5
                    </Typography>
                </Stack>

                {/* Review Comment */}
                <Typography variant="body2" color="text.secondary" sx={{ marginBottom: 2 }}>
                    {review.comment}
                </Typography>
            </CardContent>

            {/* Action Buttons */}
            <CardActions sx={{ justifyContent: 'flex-left', paddingTop: 0 }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <IconButton
                        aria-label="upvote"
                        onClick={handleUpvote}
                        size="small"
                        sx={{ marginRight: 1, color: '#4caf50' }}
                    >
                        <ThumbUpIcon fontSize="small" />
                    </IconButton>
                    <IconButton
                        aria-label="downvote"
                        onClick={handleDownvote}
                        size="small"
                        sx={{ color: '#f44336' }}
                    >
                        <ThumbDownIcon fontSize="small" />
                    </IconButton>
                </Box>
            </CardActions>
        </Card>
    );
};

export default ReviewCard;
