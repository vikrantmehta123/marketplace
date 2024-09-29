import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function ProductCard({product}) {
  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardMedia
        component="img"
        alt="green iguana"
        height="140"
      />
      <CardContent>
        <Typography gutterBottom variant="body1" component="div">
          {product.product_name}
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
          {product.description}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={() => window.open(`/buyer/product-details?productId=${product.product_id}`, '_blank')}>View Details</Button>
      </CardActions>
    </Card>
  );
}
