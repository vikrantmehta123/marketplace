import React from 'react';
import { Card, CardContent, CardActions, Typography, Button, Box } from '@mui/material';

const BidItem = ({ productBid, onEdit, onDelete }) => {
  return (
    <Card
      sx={{
        marginBottom: 2, // Add some spacing between cards
        padding: 1,
        boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)', // Add a subtle shadow for elevation
        borderRadius: '8px', // Optional: Make the card corners rounded
      }}
    >
      {/* Card Content */}
      <CardContent>
        <Typography variant="h6" component="div">
          {productBid.product.product_name}
        </Typography>
        <Typography variant="body2" color="textSecondary" mt={2} mb={1}>
          {productBid.product.description}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Price: ${productBid.price.toFixed(2)}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Stock: {productBid.stock}
        </Typography>
      </CardContent>

      {/* Card Actions */}
      <CardActions
        sx={{
          display: 'flex',
          justifyContent: 'flex-end', 
        }}
      >
        <Button
          variant="contained"
          size="small"
          onClick={() => onEdit(productBid)}
        >
          Edit
        </Button>
        <Button
          variant="contained"
          color="error"
          size="small"
          sx={{ marginLeft: 1 }}
          onClick={() => onDelete(productBid)}
        >
          Delete
        </Button>
      </CardActions>
    </Card>
  );
};

export default BidItem;
