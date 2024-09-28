import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const CategoryItem = ({ category, onEdit, onDelete }) => {
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
        <Typography variant="body1">{category.category_name}</Typography>
      </Box>
      <Box>
        <Button variant="contained" onClick={() => onEdit(category)}>
          Edit
        </Button>
        <Button
          variant="contained"
          color="error"
          onClick={() => onDelete(category)}
          sx={{ marginLeft: 1 }}
        >
          Delete
        </Button>
      </Box>
    </Box>
  );
};

export default CategoryItem;
