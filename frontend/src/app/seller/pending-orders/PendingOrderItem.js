'use client';
import React from "react";
import { Box } from "@mui/material";

const PendingOrderItem = ({ pendingOrder, onMarkAsCompleted }) => {
    <Box
        sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: 1,
            borderBottom: '1px solid #ccc',
        }}
    >
        <Box>
            <Typography variant="body1">{pendingOrder}</Typography>
        </Box>
        <Box>
            <Button variant="contained" sx={{
                width: '50%', backgroundColor: '#f0c14b', color: 'black', '&:hover': {
                    backgroundColor: '#E4B747' // Optional: Change color on hover
                }
            }} onClick={() => onMarkAsCompleted(pendingOrder)}
            >
                Mark As Completed
            </Button>
        </Box>
    </Box>
}

export default PendingOrderItem;