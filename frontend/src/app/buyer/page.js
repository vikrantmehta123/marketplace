import { Box } from "@mui/material";
import React from "react";
import BuyerSidebar from "./BuyerSidebar";
import ProductList from "./ProductList";

const BuyerHomePage = () => {
    return (
        <Box sx={{ display: 'flex' }}>
            <BuyerSidebar />
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    bgcolor: 'background.default',
                    p: 3, // Padding for main content
                    mt: 8, // Adjust margin-top to account for the Navbar height if needed
                }}
            >
                <ProductList />
            </Box>
        </Box>
    )
}

export default BuyerHomePage;