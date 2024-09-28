'use client';
import { Box } from "@mui/material";
import React from "react";
import BidList from "./BidList";

export default function ProductBid() {

    return (
        <Box sx={{ padding: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>

                <BidList>

                </BidList>
            </Box>
        </Box >
    )
}
