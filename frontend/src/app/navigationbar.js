'use client';

import React, { useState } from 'react';
import MenuIcon from '@mui/icons-material/Menu';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import Link from 'next/link';
import {
  Box, Button, Divider,
  TextField, Menu, MenuItem, Badge, Toolbar, AppBar, IconButton, CssBaseline
} from '@mui/material';
import ShopSphereLogo from './ShopSphereLogo';

const NavigationBar = () => {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="fixed" sx={{ backgroundColor: '#1c1c1c', zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* Positioning the logo to the left */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <ShopSphereLogo />
        </Box>

        {/* Centered Search Bar */}
        <TextField
          variant="outlined"
          size="small"
          placeholder="Search..."
          sx={{ width: '60%', backgroundColor: '#fff' }} // Set width to 60%
        />

        {/* Icons to the right of the Search Bar */}
        <Box sx={{ display: 'flex', alignItems: 'center', marginLeft: 1 }}>
          <IconButton color="inherit">
            <Badge badgeContent={4} color="error">
              <ShoppingCartIcon />
            </Badge>
          </IconButton>

          {/* Menu for Links */}
          <IconButton color="inherit" onClick={handleMenuClick}>
            <MenuIcon />
          </IconButton>
        </Box>

        {/* Menu Component */}
        <Menu
          id="account-menu"
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleClose}
          slotProps={{
            paper: {
              elevation: 0,
              sx: {
                overflow: 'visible',
                filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                mt: 1.5,
                '&::before': {
                  content: '""',
                  display: 'block',
                  position: 'absolute',
                  top: 0,
                  right: 14,
                  width: 10,
                  height: 10,
                  bgcolor: 'background.paper',
                  transform: 'translateY(-50%) rotate(45deg)',
                  zIndex: 0,
                },
              },
            },
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <Box sx={{ padding: 2, display: 'flex', justifyContent: 'center' }}>
            <Button size='medium' variant='contained' color='warning' href='/auth/register'>
              Sign Up
            </Button>
          </Box>

          <Divider />
          <MenuItem onClick={handleClose}>
            <Link href="/settings" style={{ textDecoration: 'none', color: 'black' }}>
              Settings
            </Link>
          </MenuItem>
          <MenuItem onClick={handleClose}>
            <Link href="/login" style={{ textDecoration: 'none', color: 'black' }}>
              Login
            </Link>
          </MenuItem>
          <MenuItem onClick={handleClose}>
            <Link href="/orders" style={{ textDecoration: 'none', color: 'black' }}>
              Orders
            </Link>
          </MenuItem>
          <MenuItem onClick={handleClose}>
            <Link href="/wishlist" style={{ textDecoration: 'none', color: 'black' }}>
              Wishlist
            </Link>
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default NavigationBar;
