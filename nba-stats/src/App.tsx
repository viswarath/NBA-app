import React from 'react';
import { Typography, Stack } from '@mui/material';
import DataTable from './dataTable';




const App: React.FC = () => {
  return (
    <Stack>
        <Typography>Welcome Viswa</Typography>
        <DataTable/>
    </Stack>
  );
}

export default App;