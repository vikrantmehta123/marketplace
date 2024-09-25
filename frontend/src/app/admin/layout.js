// AdminLayout.js
import React from "react";
import Sidebar from "./Sidebar";
import { Box, Toolbar, CssBaseline } from "@mui/material";

export default function AdminLayout({ children }) {
    return (
        <Box sx={{ display: 'flex' }}>

            <Sidebar />
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
