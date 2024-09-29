// A component that is displayed when the user wants to purchase the product and 
// wants to see the lowest offers

'use client';
import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, TextField, Modal, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import { AddShoppingCart, Favorite } from '@mui/icons-material';
import axios from 'axios';

// Modal style
const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 500,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

const ProductDetail = ({ productId }) => {
    const [quantity, setQuantity] = useState(1);
    const [openModal, setOpenModal] = useState(false);
    const [selectedSeller, setSelectedSeller] = useState(null); // Track the selected seller
    const [sellers, setSellers] = useState([]);
    const [topSeller, setTopSeller] = useState(null);
    const [product, setProduct] = useState(null);

    useEffect(() => {
        fetchSellers();
    }, []);

    useEffect(() => {
        fetchProduct();
    }, []);


    const fetchSellers = async () => {
        if (!productId) { return; }

        const response = await axios.get(`http://127.0.0.1:5000/api/v1/products/${productId}/sellers`);
        setSellers(response.data);
    }

    const fetchProduct = async () => {
        if (!productId) { return; }

        const response = await axios.get(`http://127.0.0.1:5000/api/v1/products/${productId}`);
        setProduct(response.data);
    }

    const handleAddToCart = () => {
        console.log(`Added ${quantity} of ${product.product_name} to cart.`);
    };

    const handleAddToWishlist = () => {
        console.log(`${product.name} added to wishlist.`);
    };

    const handleModalOpen = () => setOpenModal(true);
    const handleModalClose = () => setOpenModal(false);

    const handleSelectSeller = (seller) => {
        setSelectedSeller(seller);
        handleModalClose();
        // Here you can handle ordering from the selected seller
        console.log(`Ordering from seller: ${seller.username}`);
    };

    return (
        <Box sx={{ p: 3, border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
            {/* Product Description */}

            {product &&
                <Box>
                    <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 2 }}>{product.product_name}</Typography>
                    <Typography variant="body1" sx={{ mb: 3 }}>{product.description}</Typography>

                </Box>
            }


            {/* Quantity Input */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TextField
                    label="Quantity"
                    type="number"
                    variant="outlined"
                    size="small"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    sx={{ width: '80px', mr: 2 }}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleAddToCart}
                    startIcon={<AddShoppingCart />}
                    sx={{ mr: 2 }}
                >
                    Add to Cart
                </Button>
                <Button
                    variant="outlined"
                    color="secondary"
                    onClick={handleAddToWishlist}
                    startIcon={<Favorite />}
                >
                    Add to Wishlist
                </Button>
            </Box>

            {/* Seller Contact Info */}
            {
                topSeller && 
                <Typography variant="body2" sx={{ mt: 2 }}>
                    Top Seller Contact: {topSeller.contact}
                </Typography>
            }


            {/* Modal Trigger */}
            <Button variant="outlined" sx={{ mt: 2 }} onClick={handleModalOpen}>
                View Seller Details
            </Button>

            {/* Modal for Sellers */}
            <Modal open={openModal} onClose={handleModalClose} aria-labelledby="sellers-modal">
                <Box sx={modalStyle}>
                    <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
                        Sellers
                    </Typography>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Username</TableCell>
                                <TableCell>Contact</TableCell>
                                <TableCell>Bid</TableCell>
                                <TableCell>Stock</TableCell>
                                <TableCell>Action</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {sellers && sellers.map((seller, index) => (
                                <TableRow key={index}>
                                    <TableCell>{seller.seller.username}</TableCell>
                                    <TableCell>{seller.seller.contact}</TableCell>
                                    <TableCell>{seller.price.toFixed(2)}</TableCell>
                                    <TableCell>{seller.stock}</TableCell>
                                    <TableCell>
                                        <Button
                                            variant="contained"
                                            size="small"
                                            onClick={() => handleSelectSeller(seller)}
                                        >
                                            Select
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    <Button onClick={handleModalClose} variant="contained" color="primary" sx={{ mt: 2 }}>
                        Close
                    </Button>
                </Box>
            </Modal>

            {/* Display selected seller (optional) */}
            {selectedSeller && (
                <Box sx={{ mt: 2, p: 2, backgroundColor: '#f0f0f0', borderRadius: '4px' }}>
                    <Typography variant="body2">
                        Ordering from: {selectedSeller.username} ({selectedSeller.contact})
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

export default ProductDetail;