// AdminLayout.js
import React from "react";
import { Box } from "@mui/material";
import SellerSidebar from "./SellerSidebar";


export default function SellerLayout({ children }) {
    return (
        <Box sx={{ display: 'flex' }}>
            <SellerSidebar />
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    bgcolor: 'background.default',
                    p: 3, // Padding for main content
                    mt: 8, // Adjust margin-top to account for the Navbar height if needed
                }}
            >
                {children}
            </Box>
        </Box>
    );
}
