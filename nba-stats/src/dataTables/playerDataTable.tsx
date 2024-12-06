import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Stack, TextField, Alert, Skeleton, Button } from '@mui/material';
import { useQuery } from '@tanstack/react-query';


interface PlayerData {
  player_id: number;
  team_id: string; 
  name: string;
  age: number;
  position: string;
  games_started: number;
}

const fetchPlayerData = async (name: string) => {
  const response = await fetch(`http://0.0.0.0:8000/players?name=${name}`);
  if (!response.ok) {
    throw new Error('Error fetching data');
  }
  return response.json();
};


const PlayerDataTable: React.FC = () => {
  const [name, setName] = React.useState<string>('');

  const { isLoading, isError, data, error } = useQuery<PlayerData[], Error>({
    queryKey: ['players', name],
    queryFn: () => fetchPlayerData(name),
    retry: 1, 
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value); 
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 150 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'team_id', headerName: 'Team', width: 150 },
    { field: 'position', headerName: 'Position', width: 150 },
    { field: 'age', headerName: 'Age', width: 100 },
    { field: 'gamesStarted', headerName: 'Games Started', width: 180 },
  ];

  const rows = data?.map((player) => ({
    id: player.player_id,
    name: player.name,
    team_id: player.team_id,
    position: player.position,
    age: player.age,
    gamesStarted: player.games_started,
  })) || [];

  return (
    <Stack spacing={2}>
      <TextField 
        id="player-name" 
        label="Player Name" 
        variant="standard"
        fullWidth
        value={name} 
        onChange={handleChange}
      />
      
      {isError && <Alert severity="error">Error: {error?.message}</Alert>}
      
      <Paper sx={{ height: 400, width: '100%' }}>
        {isLoading ? (
          // Skeleton loader for the table
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

export default PlayerDataTable;
