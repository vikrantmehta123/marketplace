import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Link from 'next/link';
const drawerWidth = 240;

export default function SellerSidebar() {
    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: { width: drawerWidth },
            }}
        >
            <Toolbar />
            <List>
                {[
                    { text: 'Dashboard', path: '/seller/dashboard' },
                    { text: 'Product Bids', path: '/seller/bid' },
                    { text: 'Create New Product', path: '/seller/new-product' }, 
                    { text: 'Pending Orders', path: '/seller/pending-orders' }

                ].map(({ text, path }) => (
                    <ListItem key={text} disablePadding>
                        <Link href={path}
                            style={{
                                justifyContent: 'flex-start', // Align text to the left
                                width: '100%', // Make button full width
                            }}
                        >
                            <ListItemButton >
                                <ListItemText primary={text} />
                            </ListItemButton>
                        </Link>
                    </ListItem>
                ))}
            </List>
            <Divider />
        </Drawer>
    );
}
