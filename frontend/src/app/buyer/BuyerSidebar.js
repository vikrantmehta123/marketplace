'use client';
import React, { useState } from 'react';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { Box, Typography, TextField, Divider } from '@mui/material';

const drawerWidth = 240;

export default function BuyerSidebar({ categories, handleOnCategoryChange, selectedCategory }) {
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredCategories, setFilteredCategories] = useState(categories);

    const handleCategoryClick = (category) => {
        if (selectedCategory?.category_id !== category.category_id) {
            handleOnCategoryChange(category);
        }
    };

    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        const filtered = categories.filter((category) =>
            category.category_name.toLowerCase().includes(value.toLowerCase())
        );
        setFilteredCategories(filtered);
    };

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
                backgroundColor: '#f8f9fa',
            }}
        >
            <Toolbar />
            <Box sx={{ p: 2 }}>
                <Typography variant="body1" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
                    Categories
                </Typography>
                <TextField
                    variant="outlined"
                    placeholder="Search categories..."
                    value={searchTerm}
                    onChange={handleSearchChange}
                    size="small"
                    fullWidth
                    sx={{
                        marginBottom: 0.5,
                        '& .MuiOutlinedInput-root': {
                            borderRadius: '8px',
                            backgroundColor: '#fff',
                        },
                    }}
                />
            </Box>
            <Divider />
            <List>
                {filteredCategories && filteredCategories.length > 0 ? (
                    filteredCategories.map((category, idx) => (
                        <ListItem key={idx} disablePadding>
                            <ListItemButton
                                onClick={() => handleCategoryClick(category)}
                                sx={{
                                    justifyContent: 'flex-start',
                                    width: '100%',
                                    backgroundColor:
                                        selectedCategory?.category_id === category.category_id
                                            ? 'rgba(0, 123, 255, 0.1)' // Light blue background for selected category
                                            : 'transparent',
                                    color:
                                        selectedCategory?.category_id === category.category_id
                                            ? '#007bff' // Primary color text for selected
                                            : 'inherit',
                                    transition: 'background-color 0.3s, color 0.3s',
                                    '&:hover': {
                                        backgroundColor: 'rgba(0, 123, 255, 0.1)', // Slight blue on hover
                                    },
                                    '&:focus': {
                                        backgroundColor: 'rgba(0, 123, 255, 0.25)',
                                    },
                                    borderRadius: '4px',
                                    mx: 1, // Horizontal margin
                                }}
                            >
                                <ListItemText
                                    primary={category.category_name}
                                    primaryTypographyProps={{
                                        fontWeight:
                                            selectedCategory?.category_id === category.category_id
                                                ? 'bold'
                                                : 'normal',
                                    }}
                                />
                            </ListItemButton>
                        </ListItem>
                    ))
                ) : (
                    <Typography sx={{ textAlign: 'center', mt: 2, color: '#6c757d' }}>
                        No categories found
                    </Typography>
                )}
            </List>
        </Drawer>
    );
}
