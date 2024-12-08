import { useMutation } from '@tanstack/react-query';
import React, { useState } from 'react';
import { Box, Tabs, Tab, CircularProgress } from '@mui/material';
import PlayerPage  from './PlayerPage';
import TeamPage  from './TeamPage';
import GamePage from './GamePage';
import TradePage from './TradePage';
import EditPage from './EditPage';

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
        <Tab label="Trade Page" />
        <Tab label="Edit Page" />
      </Tabs>

      {isPending ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
          <CircularProgress size={100} />
        </Box>
      ) : (
        <Box sx={{ p: 3 }}>
          {value === 0 && <PlayerPage/>}
          {value === 1 && <TeamPage/>}
          {value === 2 && <GamePage/>}
          {value === 3 && <TradePage/>}
          {value === 4 && <EditPage />}
        </Box>
      )}
    </Box>
  );
};
