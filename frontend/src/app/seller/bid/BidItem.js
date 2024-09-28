import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const BidItem = ({ productBid, onEdit, onDelete }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 1,
        borderBottom: '1px solid #ccc', // Add this line for the bottom border
      }}
    >
      <Box>
        <Typography variant="body1">{productBid.product.product_name}</Typography>
        <Typography variant="body2" color="textSecondary">
          {productBid.product.description}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          {productBid.price}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          {productBid.stock}
        </Typography>
      </Box>
      <Box>
        <Button variant="contained" onClick={() => onEdit(productBid)}>
          Edit
        </Button>
        <Button
          variant="contained"
          color="error"
          onClick={() => onDelete(productBid)}
          sx={{ marginLeft: 1 }}
        >
          Delete
        </Button>
      </Box>
    </Box>
  );
};

export default BidItem;
