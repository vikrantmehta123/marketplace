'use client';
import { Box, Typography, List, TextField, TableBody, TableRow, Table, TableHead, TableCell } from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";
import PendingOrderItem from "./PendingOrderItem";

const PendingOrderList = () => {
    const [filteredPendingOrders, setFilteredPendingOrders] = useState([]);
    const [pendingOrders, setPendingOrders] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedPendingOrder, setSelectedPendingOrder] = useState(null);

    useEffect(() => {
        fetchPendingOrders();
    }, []);

    const fetchPendingOrders = async () => {
        const response = await axios.get('http://127.0.0.1:5000/api/v1/orders/pending', {
            headers: {
                'User-Id': '3',
                'Authorization': 'Bearer your-token-here'
            }
        });
        console.log(response.data);
        setPendingOrders(response.data);
        setFilteredPendingOrders(response.data); // Initialize filtered pending orders
    }

    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        // Filter pending orders based on the search term
        const filtered = pendingOrders.filter((pendingOrder) =>
            pendingOrder.product.product_name.toLowerCase().includes(value.toLowerCase()) ||
            pendingOrder.order.buyer.username.toLowerCase().includes(value.toLowerCase()) ||
            pendingOrder.order.buyer.address.toLowerCase().includes(value.toLowerCase())
        );
        setFilteredPendingOrders(filtered);
    };

    const handleMarkAsCompleted = async (pendingOrder) => {
        try {

            // TODO: Make a PUT request to update the status of the selected order
            const response = await axios.put("http://127.0.0.1:5000/api/v1/orders/pending");
        }
        catch (err) {
            console.log(err);
        }

    }


    return (
        <Box sx={{ padding: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
                <Typography variant="h4">Pending Orders</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <TextField
                        variant="outlined"
                        placeholder="Search Pending Orders..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                        size="small"
                        sx={{ marginRight: 2 }}
                    />
                </Box>
            </Box>

            <Table sx={{ borderCollapse: 'collapse' }}>
                <TableHead>
                    <TableRow>
                        <TableCell>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Product Name
                            </Typography>
                        </TableCell>
                        <TableCell>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Price
                            </Typography>
                        </TableCell>
                        <TableCell>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Quantity
                            </Typography>
                        </TableCell>
                        <TableCell>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Buyer Address
                            </Typography>
                        </TableCell>
                        <TableCell>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Buyer Username
                            </Typography>
                        </TableCell>
                        <TableCell>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Action
                            </Typography>
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredPendingOrders.map((pendingOrder, idx) => (
                        <PendingOrderItem key={idx} pendingOrder={pendingOrder} onMarkAsCompleted={handleMarkAsCompleted} />
                    ))}
                </TableBody>
            </Table>
        </Box>
    )
}

export default PendingOrderList;