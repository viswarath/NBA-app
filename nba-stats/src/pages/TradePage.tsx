import { Stack, Button, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { TradeDataTable } from '../tables/trade_tables/TradeTable';

const fetchPlayers = async () => {
  const response = await fetch('http://0.0.0.0:8000/players');
  if (!response.ok) {
    throw new Error('Failed to fetch players');
  }
  return response.json();
};

const tradePlayers = async (tradeData: { player1_id: number, player2_id: number }) => {
  const response = await fetch('http://0.0.0.0:8000/tradePlayers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(tradeData),
  });
  
  if (!response.ok) {
    throw new Error('Trade failed');
  }
  
  return response.json();
};

const TradePage: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [player1Id, setPlayer1Id] = useState<number | string>('');
  const [player2Id, setPlayer2Id] = useState<number | string>('');
  const [refreshKey, setRefreshKey] = useState(0);

  const { data: players, isLoading, isError } = useQuery({
    queryKey: ['players'],
    queryFn: fetchPlayers,
  });

  const { mutate, isPending } = useMutation({
    mutationKey: ['tradePlayers'],
    mutationFn: async (tradeData: { player1_id: number, player2_id: number }) => {
      const response = await tradePlayers(tradeData);
      if (!response) {
        throw new Error('Trade failed');
      }
      return response;
    },
    onSuccess: () => {
      setPlayer1Id('');
      setPlayer2Id('');
      setOpen(false);
      setRefreshKey((prevKey) => prevKey + 1); 
    },
    onError: (error: any) => {
      console.error('Trade Error:', error.message);
    },
  });

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleTrade = () => {
    if (!player1Id || !player2Id) {
      console.error('Both players must be selected.');
      return;
    }
    const tradeData = {
      player1_id: Number(player1Id),
      player2_id: Number(player2Id), 
    };

    if (isNaN(tradeData.player1_id) || isNaN(tradeData.player2_id)) {
      console.error('Invalid player IDs.');
      return;
    }
    mutate(tradeData);
  };

  if (isLoading) {
    return <div>Loading players...</div>;
  }

  if (isError) {
    return <div>Error loading players.</div>;
  }

  return (
    <Stack spacing={3}>
      <TradeDataTable key={refreshKey} /> 
      <Button variant="contained" color="primary" onClick={handleClickOpen}>
        Initiate Trade
      </Button>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Select Players for Trade</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="normal">
            <InputLabel>Player 1</InputLabel>
            <Select
              value={player1Id}
              onChange={(e) => setPlayer1Id(e.target.value)}
              label="Player 1"
            >
              {players.map((player: any) => (
                <MenuItem key={player.player_id} value={player.player_id}>
                  {player.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth margin="normal">
            <InputLabel>Player 2</InputLabel>
            <Select
              value={player2Id}
              onChange={(e) => setPlayer2Id(e.target.value)}
              label="Player 2"
            >
              {players.map((player: any) => (
                <MenuItem key={player.player_id} value={player.player_id}>
                  {player.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="secondary">
            Cancel
          </Button>
          <Button onClick={handleTrade} color="primary" disabled={isPending}>
            {isPending ? 'Trading...' : 'Trade'}
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
};



export default TradePage;