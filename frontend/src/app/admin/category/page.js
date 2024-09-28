'use client';
import React, { useEffect, useState } from 'react';
import {
    Box,
    Typography,
    Divider,
    Tooltip,
    List,
    IconButton,
    Toolbar,
    TextField,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CategoryItem from './CategoryItem';
import CategoryForm from './CategoryForm';
import ConfirmationDialog from './ConfirmationDialog';
import axios from 'axios';

const CategoryList = () => {
    const [categories, setCategories] = useState([]);
    const [filteredCategories, setFilteredCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [isFormOpen, setFormOpen] = useState(false);
    const [isConfirmOpen, setConfirmOpen] = useState(false);
    const [categoryToDelete, setCategoryToDelete] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        const response = await axios.get('http://127.0.0.1:5000/api/v1/category');
        setCategories(response.data);
        setFilteredCategories(response.data); // Initialize filtered categories
    };

    const handleEdit = (category) => {
        setSelectedCategory(category);
        setFormOpen(true);
    };

    const handleDelete = (category) => {
        setCategoryToDelete(category);
        setConfirmOpen(true);
    };

    const handleCreate = () => {
        setSelectedCategory(null);
        setFormOpen(true);
    };

    const handleFormSubmit = async (category) => {
        const response = selectedCategory
            ? await fetch(`/api/categories/${selectedCategory.category_id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(category),
            })
            : await fetch('/api/categories', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(category),
            });

        await fetchCategories(); // Update the list
        setFormOpen(false);
    };

    const handleDeleteConfirm = async () => {
        await fetch(`/api/categories/${categoryToDelete.category_id}`, { method: 'DELETE' });
        await fetchCategories(); // Update the list
        setConfirmOpen(false);
    };

    // Search handler
    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        // Filter categories based on the search term
        const filtered = categories.filter((category) =>
            category.category_name.toLowerCase().includes(value.toLowerCase())
        );
        setFilteredCategories(filtered);
    };

    return (
        <Box sx={{ padding: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
                <Typography variant="h4">Categories</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <TextField
                        variant="outlined"
                        placeholder="Search categories..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                        size="small"
                        sx={{ marginRight: 2 }}
                    />
                    <Tooltip title="Can't find the category? Create one">
                        <IconButton color="primary" onClick={handleCreate}>
                            <AddIcon />
                        </IconButton>
                    </Tooltip>
                </Box>
            </Box>
            <Divider/>
            <List>
                {filteredCategories.map((category) => (
                    <CategoryItem
                        key={category.category_id}
                        category={category}
                        onEdit={handleEdit}
                        onDelete={handleDelete}
                    />
                ))}
            </List>
            {isFormOpen && (
                <CategoryForm
                    category={selectedCategory}
                    onSubmit={handleFormSubmit}
                    onClose={() => setFormOpen(false)}
                />
            )}
            {isConfirmOpen && (
                <ConfirmationDialog
                    message={`Are you sure you want to delete "${categoryToDelete.category_name}"?`}
                    onConfirm={handleDeleteConfirm}
                    onCancel={() => setConfirmOpen(false)}
                />
            )}
        </Box>
    );
};

export default CategoryList;
