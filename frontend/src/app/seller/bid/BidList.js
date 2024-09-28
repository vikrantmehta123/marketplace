'use client';
import React, { useState, useEffect } from "react";
import { Box, Typography, List } from "@mui/material";
import axios from "axios";

import BidItem from "./BidItem";
import ConfirmationDialog from "@/app/ConfirmationDialog";

const BidList = ({ products }) => {
    const [filteredProductBids, setFilteredProductBids] = useState([]);
    const [productBids, setProductBids] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedProductBid, setSelectedProductBid] = useState(null);
    const [isConfirmOpen, setConfirmOpen] = useState(false);
    const [isFormOpen, setFormOpen] = useState(false);

    useEffect(() => {
        fetchProductBids();
    }, []);

    const fetchProductBids = async () => {
        const response = await axios.get('http://127.0.0.1:5000/api/v1/product-sellers/bids');
        setPendingOrders(response.data);
        setFilteredPendingOrders(response.data);
    }

    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        // Filter bids based on the search term
        const filtered = productBids.filter((productBid) =>
            productBid.product.product_name.toLowerCase().includes(value.toLowerCase())
        );
        setFilteredProductBids(filtered);
    };

    const handleDelete = (productBid) => {
        setSelectedProductBid(productBid);
        setConfirmOpen(true);
    }

    const handleEdit = (productBid) => {
        setSelectedProductBid(productBid);
    }

    const handleDeleteConfirm = async () => {
        // TODO: Make the API call to delete a Bid
        // If successful, just remove that Product Bid from the product bids list
        setConfirmOpen(false);
    };

    return (
        <Box sx={{ padding: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
                <Typography variant="h4">Your Product Bids</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <TextField
                        variant="outlined"
                        placeholder="Search categories..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                        size="small"
                        sx={{ marginRight: 2 }}
                    />

                    {/* Instead of opening a modal, create a new window / redirect to page for new product */}
                    <Tooltip title="Can't find the category? Create one">
                        <IconButton color="primary" onClick={handleCreate}>
                            <AddIcon />
                        </IconButton>
                    </Tooltip>
                </Box>
            </Box>
            <List>
                {filteredProductBids.map((productBid, idx) => (
                    <BidItem key={idx} productBid={productBid} onEdit={handleEdit} onDelete={handleDelete} />
                ))}

            </List>
            
            {/* TODO: Handle Form Modals Here */}
            {isConfirmOpen && (
                <ConfirmationDialog
                    message={`Are you sure you want to delete bid for ${selectedProductBid.product.product_name}?`}
                    onConfirm={handleDeleteConfirm}
                    onCancel={() => setConfirmOpen(false)}
                />
            )}
        </Box>
    )
}

export default BidList;