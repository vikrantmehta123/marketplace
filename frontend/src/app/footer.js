'use client';
import React, { useEffect, useState } from 'react';
import { Box, Typography, CssBaseline } from '@mui/material';
import Link from 'next/link';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        width: '100%',
        backgroundColor: '#1c1c1c',
        color: '#fff',
        position:'fixed',
        bottom: 0,
        left: 0,
        padding: '8px 0', // Reduced padding
        textAlign: 'center',
        zIndex: (theme) => theme.zIndex.drawer + 1
      }}
    >
      <Box>
        <Typography variant="body2" component="p" sx={{ lineHeight: '1.5' }}>
          &copy; {new Date().getFullYear()} ShopSphere. All rights reserved.
        </Typography>
        <Link href="/about" style={{ margin: '4px', color: 'inherit' }}>
          <Typography component="span" sx={{ "&:hover": { textDecoration: 'underline' } }}>
            About
          </Typography>
        </Link>
        <Link href="/contact" style={{ margin: '4px', color: 'inherit' }}>
          <Typography component="span" sx={{ "&:hover": { textDecoration: 'underline' } }}>
            Contact
          </Typography>
        </Link>
        <Link href="/privacy" style={{ margin: '4px', color: 'inherit' }}>
          <Typography component="span" sx={{ "&:hover": { textDecoration: 'underline' } }}>
            Privacy Policy
          </Typography>
        </Link>
        <Link href="/terms" style={{ margin: '4px', color: 'inherit' }}>
          <Typography component="span" sx={{ "&:hover": { textDecoration: 'underline' } }}>
            Terms of Service
          </Typography>
        </Link>

      </Box>
    </Box>
  );
};

export default Footer;
