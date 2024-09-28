'use client';
import { Box } from "@mui/material";
import React from "react";
import { useState, useEffect } from "react";
import BidForm from "./BidForm";
import { Button } from "@mui/material";
import BidList from "./BidList";
import axios from "axios";

export default function ProductBid() {
    const [open, setOpen] = useState(false);
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                // TODO: You need to create an API in the backend to return a users bids
                const response = await axios.get('http://127.0.0.1:5000/api/v1/category');

                // Create an empty array to hold all the products
                let allProducts = [];

                // Iterate over each category and concatenate the products into the allProducts array
                response.data.forEach((category) => {
                    allProducts = [...allProducts, ...category.products];
                });

                // Set the products state with the concatenated array
                setProducts(allProducts);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };

        fetchCategories();
    }, []);

    const handleOpen = () => setOpen(true);

    const handleClose = () => setOpen(false);

    return (
        <Box sx={{ padding: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>

                <BidList products={products}>

                </BidList>
            </Box>
        </Box >
    )
}
