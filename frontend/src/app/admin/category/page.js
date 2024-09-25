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
        // const response = await fetch('/api/categories'); // Your API endpoint
        // const data = await response.json();
        const data = [
            {
                'name': 'Books',
                'description': 'Collection of books of all genres'
            },
            {
                'name': 'Apparel',
                'description': 'Fashion for the nation'
            }
        ]
        setCategories(data);
        setFilteredCategories(data); // Initialize filtered categories
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
            ? await fetch(`/api/categories/${selectedCategory.id}`, {
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
        await fetch(`/api/categories/${categoryToDelete.id}`, { method: 'DELETE' });
        await fetchCategories(); // Update the list
        setConfirmOpen(false);
    };

    // Search handler
    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        // Filter categories based on the search term
        const filtered = categories.filter((category) =>
            category.name.toLowerCase().includes(value.toLowerCase()) || category.description.toLowerCase().includes(value.toLowerCase())
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
                        key={category.id}
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
                    message={`Are you sure you want to delete "${categoryToDelete.name}"?`}
                    onConfirm={handleDeleteConfirm}
                    onCancel={() => setConfirmOpen(false)}
                />
            )}
        </Box>
    );
};

export default CategoryList;
