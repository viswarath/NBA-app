
import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Button, Stack, TextField, Paper, Alert, Skeleton } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';


interface SpecializedPlayerData {
  player_id: number;
  team_id: string;
  name: string;
  age: number;
  position: string;
  games_started: number;
  total_points?: number;      
  AST?: number;     
  FT_Perc?: number;      
}

export const SpecializedPlayerTable: React.FC = () => {
  const [filterType, setFilterType] = useState<'Points per Game' | 'Assists per Game' | 'Free Throw Percentage' | null>(null);
  const [statValue, setStatValue] = useState<number | null>(null);

  const { isLoading, isError, data, error } = useQuery<SpecializedPlayerData[], Error>({
    queryKey: ['players', filterType, statValue],
    queryFn: async () => {
      if (!statValue) return []; 
      let url = '';
      switch (filterType) {
        case 'Points per Game':
          url = `http://0.0.0.0:8000/playerPoints?points=${statValue}`;
          break;
        case 'Assists per Game':
          url = `http://0.0.0.0:8000/playerAssists?assists=${statValue}`;
          break;
        case 'Free Throw Percentage':
          url = `http://0.0.0.0:8000/playerFTPerc?FTPerc=${statValue/100}`;
          break;
        default:
          throw new Error('Invalid filter type');
      }
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Error fetching data');
      }
      return response.json();
    },
    retry: 1, 
    enabled: filterType !== null && statValue !== null, 
  });

  const handleStatChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setStatValue(Number(event.target.value)); 
  };

  const handleFilterClick = (type: 'Points per Game' | 'Assists per Game' | 'Free Throw Percentage') => {
    setFilterType(type);
    setStatValue(null); // Reset stat value when a new filter is clicked
  };

  // Dynamic column definition based on filter type
  const columns: GridColDef[] = [
    { field: 'player_id', headerName: 'Player ID', width: 150 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'team_id', headerName: 'Team', width: 150 },
    { field: 'position', headerName: 'Position', width: 150 },
    { field: 'age', headerName: 'Age', width: 100 },
    { field: 'games_started', headerName: 'Games Started', width: 180 },
    {
      field: 'special_stat',
      headerName: filterType ? `${filterType.charAt(0).toUpperCase() + filterType.slice(1)}` : 'Special Stat',
      width: 150,
    },
  ];

  console.log(data)
  // Dynamic row mapping based on filterType
  const rows = data?.map((player) => ({
    id: player.player_id,
    player_id: player.player_id,
    name: player.name,
    team_id: player.team_id,
    position: player.position,
    age: player.age,
    games_started: player.games_started,
    special_stat: 
      filterType === 'Points per Game' ? player.total_points :
      filterType === 'Assists per Game' ? player.AST :
      filterType === 'Free Throw Percentage' ? (player.FT_Perc ?? 0) * 100 + "%" : null,
  })) || [];

  return (
    <Stack spacing={2}>
      <Stack 
        direction="row" 
        spacing={2} 
        sx={{
         justifyContent: "center",
         alignItems: "center",
      }}>
        <Button variant="contained" onClick={() => handleFilterClick('Points per Game')}>Points</Button>
        <Button variant="contained" onClick={() => handleFilterClick('Assists per Game')}>Assists</Button>
        <Button variant="contained" onClick={() => handleFilterClick('Free Throw Percentage')}>Free Throw %</Button>
      </Stack>

      <TextField 
        id="stat-value" 
        label={filterType ? `Enter ${filterType ? filterType.charAt(0).toUpperCase() + filterType.slice(1) : ''}` : `Select Filter Type`}
        variant="standard"
        fullWidth
        type="number"
        value={statValue ?? ''}
        onChange={handleStatChange}
        disabled={filterType === null}
      />
      
      {isError && <Alert severity="error">Error: {error?.message}</Alert>}
      
      <Paper sx={{ height: 400, width: '100%' }}>
        {isLoading ? (
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {[...Array(5)].map((_, index) => (
              <Skeleton key={index} variant="rectangular" height={40} sx={{ margin: '5px 0' }} />
            ))}
          </div>
        ) : (
          <DataGrid
            rows={rows}
            columns={columns}
            loading={isLoading}
            getRowId={(row) => row.id} 
          />
        )}
      </Paper>
    </Stack>
  );
}



