'use client';
import React from "react";
import { Box, Button, TableRow, TableCell } from "@mui/material";

const PendingOrderItem = ({ pendingOrder, onMarkAsCompleted }) => {

    return (


        <TableRow>
            <TableCell>{pendingOrder.product.product_name}</TableCell>
            <TableCell>${pendingOrder.price.toFixed(2)}</TableCell>
            <TableCell>{pendingOrder.quantity}</TableCell>
            <TableCell>{pendingOrder.order.buyer.address}</TableCell>
            <TableCell>{pendingOrder.order.buyer.username}</TableCell>
            <TableCell>
                <Button
                    variant="contained"
                    sx={{
                        backgroundColor: '#f0c14b',
                        color: 'black',
                        '&:hover': {
                            backgroundColor: '#E4B747',
                        },
                        width: '100%'
                    }}
                    onClick={() => onMarkAsCompleted(pendingOrder)}
                >
                    Mark As Completed
                </Button>
            </TableCell>
        </TableRow>

    )

}

export default PendingOrderItem;