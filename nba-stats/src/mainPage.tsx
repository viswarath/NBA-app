import { useMutation } from '@tanstack/react-query';
import React, { useState } from 'react';
import { Box, Tabs, Tab, CircularProgress } from '@mui/material';
import PlayerDataTable from './dataTables/playerDataTable';

export const MainPage : React.FC = () => {
  const [value, setValue] = useState<number>(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const { mutate, isPending } = useMutation({
    mutationKey: ['initdb'],
    mutationFn: async () => {
      const response = await fetch('http://0.0.0.0:8000/initdb', {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('Failed to initialize database');
      }

      return response.json();
    },
  });

  React.useEffect(() => {
    mutate();
  }, [mutate]);


  return (
    <Box sx={{ width: '100%' }}>
      <Tabs value={value} onChange={handleChange} centered>
        <Tab label="Player Table" />
        <Tab label="Team Table" />
        <Tab label="Game Table" />
      </Tabs>

      {isPending ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
          <CircularProgress size={100} />
        </Box>
      ) : (
        <Box sx={{ p: 3 }}>
          {value === 0 && <PlayerDataTable/>}
          {value === 1 && <div>Content for View 2</div>}
          {value === 2 && <div>Content for View 3</div>}
        </Box>
      )}
    </Box>
  );
};
