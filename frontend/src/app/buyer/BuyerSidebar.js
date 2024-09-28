import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Link from 'next/link';
const drawerWidth = 240;

export default function BuyerSidebar({categories, handleOnCategoryChange}) {
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
                {categories.map(({ cateory, idx }) => (
                    <ListItem key={idx} disablePadding>
                        <Link href={path}
                            style={{
                                justifyContent: 'flex-start', // Align text to the left
                                width: '100%', // Make button full width
                            }}
                        >
                            <ListItemButton >
                                <ListItemText primary={Category.category_name} />
                            </ListItemButton>
                        </Link>
                    </ListItem>
                ))}
            </List>
        </Drawer>
    );
}
