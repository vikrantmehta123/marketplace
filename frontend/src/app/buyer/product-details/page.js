'use client';
import { Box, Toolbar, Grid2, Divider } from "@mui/material";
import React from "react";
import { useSearchParams } from 'next/navigation';
import ProductDetail from "./ProductDetail";
import ReviewList from "./ReviewList";
import ImageCarousel from "./ImageCarousel";

const ProductDetailsPage = () => {
    const searchParams = useSearchParams();
    const productId = searchParams.get('productId');  // Get the productId from the query string

    return (
        <Box sx={{ p: 2 }}>
            <Toolbar />
            {/* Grid layout for Image Carousel and Product Details */}
            <Grid2 container spacing={3} sx={{ display: 'flex', alignItems: 'stretch', justifyContent:'center' }}>
                {/* Image Carousel */}
                <Grid2 item xs={12} md={6} sx={{ display: 'flex', flexDirection: 'column' }}>
                    <Box sx={{ flexGrow: 1, p: 2, border: '1px solid #ccc', borderRadius: '8px' }}>
                        <ImageCarousel />
                    </Box>
                </Grid2>

                {/* Product Details */}
                <Grid2 item xs={12} md={6} sx={{ display: 'flex', flexDirection: 'column' }}>
                    <ProductDetail productId={productId} sx={{ flexGrow: 1 }} />
                </Grid2>
            </Grid2>

            {/* Divider to separate sections */}
            <Divider sx={{ my: 3 }} />

            {/* Review List - spans about 75% of width, left-aligned */}
            <Box sx={{ width: '75%', ml: 0 }}>
                <ReviewList productId={productId} />
            </Box>
        </Box>
    );
}

export default ProductDetailsPage;
