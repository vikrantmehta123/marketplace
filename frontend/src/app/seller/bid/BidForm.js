'use client';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    TextField,
    Button,
    Select,
    MenuItem,
    InputLabel,
    FormControl,
    Typography,
    Box,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
} from '@mui/material';

export default function BidForm ({ open, onClose }){
    const [categories, setCategories] = useState([]);
    const [products, setProducts] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedProduct, setSelectedProduct] = useState('');
    const [price, setPrice] = useState('');
    const [stock, setStock] = useState('');

    // Fetch categories when the component mounts
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/v1/category');
                setCategories(response.data);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };

        fetchCategories();
    }, []);

    // Fetch products when a category is selected
    const handleCategoryChange = async (event) => {
        const category = event.target.value;
        setSelectedCategory(category);

        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/v1/products/${category.category_id}`);
            setProducts(response.data);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    // Submit bid form
    const handleSubmit = async (event) => {
        event.preventDefault();

        const bidData = {
            product: selectedProduct,
            price: parseFloat(price),
            stock: parseInt(stock),
        };

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/v1/product-sellers', bidData); // Update the endpoint to match your API
            console.log('Bid submitted successfully:', response.data);
            onClose(); // Close modal after submission
        } catch (error) {
            console.error('Error submitting bid:', error);
        }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>Submit a Bid</DialogTitle>
            <DialogContent>
                <Box component="form" onSubmit={handleSubmit}>
                    {/* Category Selection */}
                    <FormControl fullWidth margin="normal" size='small'>
                        <InputLabel>Category</InputLabel>
                        <Select
                            value={selectedCategory}
                            onChange={handleCategoryChange}
                            label="Category"
                        >
                            {categories.map((category) => (
                                <MenuItem key={category.category_id} value={category}>
                                    {category.category_name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/* Product Selection */}
                    <FormControl fullWidth margin="normal" size='small' disabled={!selectedCategory}>
                        <InputLabel>Product</InputLabel>
                        <Select
                            value={selectedProduct}
                            onChange={(e) => setSelectedProduct(e.target.value)}
                            label="Product"
                        >
                            {products.map((product) => (
                                <MenuItem key={product.product_id} value={product.product_name}>
                                    {product.product_name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/* Bid Price and Stock Fields */}
                    <TextField
                        label="Bid Price"
                        type="number"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        fullWidth
                        margin="normal"
                        size='small'
                        required
                    />
                    <TextField
                        label="Available Stock"
                        type="number"
                        value={stock}
                        onChange={(e) => setStock(e.target.value)}
                        fullWidth
                        margin="normal"
                        size='small'
                        required
                    />
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="secondary">Cancel</Button>
                <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={!selectedProduct || !price || !stock}
                >
                    Submit Bid
                </Button>
            </DialogActions>
        </Dialog>
    );
};