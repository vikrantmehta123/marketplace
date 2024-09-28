import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';

const ConfirmationDialog = ({ message, onConfirm, onCancel }) => (
  <Dialog open onClose={onCancel}>
    <DialogTitle>Confirmation</DialogTitle>
    <DialogContent>
      <p>{message}</p>
    </DialogContent>
    <DialogActions>
      <Button onClick={onCancel} color="primary">
        No
      </Button>
      <Button onClick={onConfirm} color="primary">
        Yes
      </Button>
    </DialogActions>
  </Dialog>
);

export default ConfirmationDialog;
