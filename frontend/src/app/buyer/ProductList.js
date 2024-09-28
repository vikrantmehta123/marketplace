'use client';
import { Box, List, ListItem, Typography, TextField } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import BuyerSidebar from "./BuyerSidebar";
import ProductCard from "./ProductCard";

const ProductList = () => {
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [products, setProducts] = useState([]);
    const [filteredProducts, setFilteredProducts] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        const response = await axios.get('http://127.0.0.1:5000/api/v1/category');
        setCategories(response.data);
        setSelectedCategory(response.data[0]);
        console.log(response.data);
    };

    const handleOnCategoryChange = async (category) => {
        setSelectedCategory(category);
        const response = await axios.get(`http://127.0.0.1:5000/api/v1/products/category/${category.category_id}`);
        setProducts(response.data);
        setFilteredProducts(response.data);
    }

    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        const filtered = products.filter((product) =>
            product.product_name.toLowerCase().includes(value.toLowerCase()) ||
            product.description.toLowerCase().includes(value.toLowerCase())
        );
        setFilteredCategories(filtered);
    };

    return (
        <Box>
            {categories.length > 0 && (
                <BuyerSidebar
                    categories={categories}
                    handleOnCategoryChange={handleOnCategoryChange}
                    selectedCategory={selectedCategory}  // Pass down the selected category
                />
            )}

            <Box sx={{ display: 'flex', alignItems: 'center', p: 2 }}>
                <Typography variant="body1" component="div" sx={{ fontWeight: 'bold', marginRight: 2 }}>
                    Search Products
                </Typography>
                <TextField
                    variant="outlined"
                    placeholder="Search products..."
                    value={searchTerm}
                    onChange={handleSearchChange}
                    size="small"
                    sx={{
                        '& .MuiOutlinedInput-root': {
                            borderRadius: '8px',
                            backgroundColor: '#fff',
                            width: '100%',
                        },
                    }}
                />
            </Box>

            <List>
                {filteredProducts.map((product, idx) => (
                    <ListItem key={idx} disablePadding>

                        <ProductCard product={product} />

                    </ListItem>
                ))}
            </List>
        </Box>
    )
}

export default ProductList;